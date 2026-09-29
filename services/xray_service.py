#!/usr/bin/env python3
"""
⚡ ماژول اختصاصی مدیریت هسته پروکسی Xray-core (Embedded Proxy Engine)
این سرویس امکان مدیریت بومی پروکسی‌های VLESS Reality و WebSocket را بدون وابستگی
به پنل‌های خارجی مستقیماً از داخل TGBot فراهم می‌کند.
- تولید کلیدهای رمزنگاری X25519 برای Reality
- تولید خودکار کانفیگ و لینک‌های سابسکریپشن کلاینت
- مدیریت کاربران در هسته Xray از طریق Xray API (gRPC / CLI)
- استعلام آمار مصرف ترافیک بلادرنگ
- پایش و همگام‌سازی نودهای شبکه
"""

import os
import sys
import time
import json
import shutil
import base64
import secrets
import logging
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("xray_service")
logger.setLevel(logging.INFO)

try:
    from cryptography.hazmat.primitives.asymmetric import x25519
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


class XrayService:
    """مدیریت هسته Xray-core و تولید پیکربندی‌ها و لینک‌های سابسکریپشن"""

    def __init__(self, db_instance=None):
        from database import db as default_db
        self.db = db_instance or default_db
        self._binary_path: Optional[str] = None
        self._detect_binary()
        # متغیرهای وضعیت ورکر مانیتورینگ مصرف ترافیک
        self._worker_thread: Optional[threading.Thread] = None
        self._worker_running: bool = False
        self._worker_interval: int = 60
        self._last_sync_time: float = 0.0
        self._last_sync_stats: Dict[str, Any] = {}

    def _detect_binary(self) -> Optional[str]:
        """یافتن مسیر فایل اجرایی Xray روی سرور"""
        candidates = [
            shutil.which("xray"),
            "/usr/local/bin/xray",
            "/usr/bin/xray",
            "/opt/xray/xray",
            "xray"
        ]
        for c in candidates:
            if c and Path(c).is_file() and os.access(c, os.X_OK):
                self._binary_path = c
                return c
        self._binary_path = None
        return None

    def is_installed(self) -> bool:
        """بررسی نصب بودن هسته Xray روی سرور"""
        if self._binary_path:
            return True
        return self._detect_binary() is not None

    def is_enabled(self) -> bool:
        """بررسی فعال بودن هسته داخلی در تنظیمات سیستم"""
        return self.db.is_setting_enabled("xray_core_enabled", default=False)

    def is_running(self) -> bool:
        """بررسی وضعیت فعال بودن پروسس هسته Xray"""
        if not self.is_installed():
            return False
        try:
            # بررسی وضعیت سرویس در لینوکس
            if os.name != "nt":
                res = subprocess.run(["systemctl", "is-active", "xray"], capture_output=True, text=True, timeout=3)
                if res.returncode == 0 and "active" in res.stdout:
                    return True
        except Exception:
            pass

        # تلاش برای بررسی پورت کنترل API
        try:
            api_port = int(self.db.get_setting("xray_api_port", 10085) or 10085)
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                return s.connect_ex(("127.0.0.1", api_port)) == 0
        except Exception:
            return False

    # ─── تولید کلیدهای رمزنگاری و هویت Reality ───

    def generate_x25519_keypair(self) -> Dict[str, str]:
        """تولید جفت‌کلید رمزنگاری X25519 استاندارد برای پروتکل Reality"""
        if HAS_CRYPTO:
            priv = x25519.X25519PrivateKey.generate()
            pub = priv.public_key()
            raw_priv = priv.private_bytes_raw()
            raw_pub = pub.public_bytes_raw()
            priv_b64 = base64.urlsafe_b64encode(raw_priv).decode("utf-8").rstrip("=")
            pub_b64 = base64.urlsafe_b64encode(raw_pub).decode("utf-8").rstrip("=")
            sid = secrets.token_hex(4)
            return {
                "private_key": priv_b64,
                "public_key": pub_b64,
                "short_id": sid
            }

        # فال‌بک با استفاده از خود باینری xray در صورت وجود
        if self.is_installed():
            try:
                res = subprocess.run([self._binary_path, "x25519"], capture_output=True, text=True, timeout=5)
                lines = res.stdout.strip().splitlines()
                priv_key = ""
                pub_key = ""
                for line in lines:
                    if "Private key:" in line or "Private key" in line:
                        priv_key = line.split(":", 1)[-1].strip()
                    elif "Public key:" in line or "Public key" in line:
                        pub_key = line.split(":", 1)[-1].strip()
                if priv_key and pub_key:
                    return {
                        "private_key": priv_key,
                        "public_key": pub_key,
                        "short_id": secrets.token_hex(4)
                    }
            except Exception as e:
                logger.error(f"Error running xray x25519: {e}")

        # فال‌بک رندوم
        dummy_priv = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
        dummy_pub = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
        return {
            "private_key": dummy_priv,
            "public_key": dummy_pub,
            "short_id": secrets.token_hex(4)
        }

    def ensure_reality_credentials(self) -> Dict[str, str]:
        """اطمینان از وجود کلیدهای Reality در تنظیمات، یا تولید و ذخیره خودکار آن‌ها"""
        priv = self.db.get_setting("xray_reality_private_key")
        pub = self.db.get_setting("xray_reality_public_key")
        sid = self.db.get_setting("xray_reality_short_id")

        if not priv or not pub or not sid:
            keys = self.generate_x25519_keypair()
            self.db.set_setting("xray_reality_private_key", keys["private_key"])
            self.db.set_setting("xray_reality_public_key", keys["public_key"])
            self.db.set_setting("xray_reality_short_id", keys["short_id"])
            logger.info("Generated and saved new X25519 Reality keypair in system settings.")
            return keys

        return {
            "private_key": priv,
            "public_key": pub,
            "short_id": sid
        }

    # ─── تولید لینک‌های کانفیگ اختصاصی مشتری (Config URIs) ───

    # ─── تولید لینک‌های کانفیگ اختصاصی مشتری (Config URIs) با ماتریس هوشمند ───

    def generate_matrix_subscription(self, uuid: str, account_name: str = "TGBot") -> List[str]:
        """
        تولید ماتریس کامل و پویای کانفیگ‌ها بر اساس:
        - دامنه‌های فعال و نقش‌های آنها (Direct, CDN, Clean IP)
        - ماتریس سوئیچ‌های پروتکل‌ها (VLESS Reality, VLESS-WS, Trojan-WS, VLESS-gRPC, VMess)
        """
        if not uuid:
            return []

        clean_uuid = str(uuid).strip()
        label_base = account_name or "VPN"
        configs = []

        credentials = self.ensure_reality_credentials()
        pub_key = credentials.get("public_key", "")
        short_id = credentials.get("short_id", "")

        # ماتریس سوئیچ‌ها
        # حالت Direct:
        sw_direct_reality_tcp = self.db.is_setting_enabled("xray_matrix_direct_reality_tcp", default=self.db.is_setting_enabled("xray_reality_enabled", default=True))
        sw_direct_reality_grpc = self.db.is_setting_enabled("xray_matrix_direct_reality_grpc", default=False)
        sw_direct_trojan = self.db.is_setting_enabled("xray_matrix_direct_trojan", default=False)
        sw_direct_shadowsocks = self.db.is_setting_enabled("xray_matrix_direct_shadowsocks", default=False)

        # حالت CDN:
        sw_cdn_vless_ws = self.db.is_setting_enabled("xray_matrix_cdn_vless_ws", default=self.db.is_setting_enabled("xray_ws_enabled", default=True))
        sw_cdn_trojan_ws = self.db.is_setting_enabled("xray_matrix_cdn_trojan_ws", default=False)
        sw_cdn_vless_grpc = self.db.is_setting_enabled("xray_matrix_cdn_vless_grpc", default=False)
        sw_cdn_vmess_ws = self.db.is_setting_enabled("xray_matrix_cdn_vmess_ws", default=False)

        # دریافت دامنه‌های ثبت‌شده در دیتابیس
        registered_domains = []
        try:
            registered_domains = self.db.get_xray_domains(active_only=True)
        except Exception as e:
            logger.warning(f"Could not load xray_domains: {e}")

        # اگر هیچ دامنه‌ای در جدول ثبت نشده باشد، از دامنه‌های پیش‌فرض تنظیمات استفاده می‌کنیم
        if not registered_domains:
            def_direct = (
                self.db.get_setting("xray_direct_domain")
                or self.db.get_setting("custom_domain")
                or os.getenv("PANEL_DOMAIN")
                or self.db.get_setting("xray_server_ip")
                or "127.0.0.1"
            ).strip().replace("https://", "").replace("http://", "").rstrip("/")

            def_cdn = (self.db.get_setting("xray_cdn_domain") or "").strip().replace("https://", "").replace("http://", "").rstrip("/")
            if not def_cdn and sw_cdn_vless_ws:
                def_cdn = (self.db.get_setting("custom_domain") or def_direct).strip().replace("https://", "").replace("http://", "").rstrip("/")

            if def_direct and (sw_direct_reality_tcp or sw_direct_reality_grpc or sw_direct_trojan or sw_direct_shadowsocks):
                registered_domains.append({
                    "domain": def_direct,
                    "role": "direct",
                    "alias": "",
                    "sni": self.db.get_setting("xray_reality_sni", "www.yahoo.com"),
                    "clean_ips": "",
                    "ws_path": "/tgbot-ws",
                    "grpc_service_name": "tgbot-grpc",
                    "port": int(self.db.get_setting("xray_reality_port", 443) or 443)
                })
            if def_cdn and (sw_cdn_vless_ws or sw_cdn_trojan_ws or sw_cdn_vless_grpc or sw_cdn_vmess_ws):
                registered_domains.append({
                    "domain": def_cdn,
                    "role": "cdn",
                    "alias": "",
                    "sni": def_cdn,
                    "clean_ips": "",
                    "ws_path": self.db.get_setting("xray_ws_path", "/tgbot-ws"),
                    "grpc_service_name": "tgbot-grpc",
                    "port": int(self.db.get_setting("xray_ws_port", 8443) or 8443)
                })

        # پردازش دامنه‌ها بر اساس نقش
        for item in registered_domains:
            role = item.get("role", "cdn").lower()
            dom = item.get("domain", "").strip()
            if not dom:
                continue
            alias = item.get("alias", "").strip()
            tag_alias = f" [{alias}]" if alias else ""
            sni = (item.get("sni", "") or dom).strip()
            port = int(item.get("port") or (443 if role == "direct" else 8443))
            ws_path = item.get("ws_path") or "/tgbot-ws"
            if not ws_path.startswith("/"):
                ws_path = "/" + ws_path
            grpc_srv = item.get("grpc_service_name") or "tgbot-grpc"
            clean_ips_str = item.get("clean_ips", "") or ""

            # ۱. نقش مستقیم (Direct)
            if role == "direct":
                # VLESS Reality TCP Vision
                if sw_direct_reality_tcp and pub_key:
                    reality_sni = str(self.db.get_setting("xray_reality_sni", "www.yahoo.com") or "www.yahoo.com").strip()
                    uri = (
                        f"vless://{clean_uuid}@{dom}:{port}"
                        f"?security=reality&encryption=none&pbk={pub_key}&headerType=none"
                        f"&fp=chrome&spx=%2F&type=tcp&flow=xtls-rprx-vision&sni={reality_sni}&sid={short_id}"
                        f"#{label_base} ⚡{tag_alias} Reality Direct"
                    )
                    configs.append(uri)

                # VLESS Reality gRPC
                if sw_direct_reality_grpc and pub_key:
                    reality_sni = str(self.db.get_setting("xray_reality_sni", "www.yahoo.com") or "www.yahoo.com").strip()
                    uri = (
                        f"vless://{clean_uuid}@{dom}:{port}"
                        f"?security=reality&encryption=none&pbk={pub_key}&headerType=none"
                        f"&fp=chrome&type=grpc&serviceName={grpc_srv}&sni={reality_sni}&sid={short_id}"
                        f"#{label_base} ⚡{tag_alias} Reality gRPC"
                    )
                    configs.append(uri)

                # Trojan Direct
                if sw_direct_trojan:
                    uri = (
                        f"trojan://{clean_uuid}@{dom}:{port}"
                        f"?security=tls&headerType=none&type=tcp&sni={sni}"
                        f"#{label_base} 🛡️{tag_alias} Trojan Direct"
                    )
                    configs.append(uri)

                # Shadowsocks 2022 AEAD
                if sw_direct_shadowsocks:
                    ss_method = "2022-blake3-aes-128-gcm"
                    ss_port = int(self.db.get_setting("xray_ss_port", 1080) or 1080)
                    raw_creds = f"{ss_method}:{clean_uuid[:16]}"
                    b64_creds = base64.b64encode(raw_creds.encode("utf-8")).decode("utf-8")
                    uri = f"ss://{b64_creds}@{dom}:{ss_port}#{label_base} 🕶️{tag_alias} Shadowsocks 2022"
                    configs.append(uri)

            # ۲. نقش CDN
            elif role == "cdn":
                clean_targets = []
                if clean_ips_str:
                    raw_ips = [ip.strip() for ip in clean_ips_str.replace("\n", ",").replace(";", ",").split(",") if ip.strip()]
                    clean_targets.extend(raw_ips)

                if not clean_targets:
                    clean_targets = [dom]

                for idx, target_host in enumerate(clean_targets):
                    isp_tag = f" #{idx+1}" if len(clean_targets) > 1 else ""

                    # VLESS WebSocket
                    if sw_cdn_vless_ws:
                        cdn_title = "Cloud CDN" if not alias else "VLESS-WS"
                        uri = (
                            f"vless://{clean_uuid}@{target_host}:{port}"
                            f"?security=tls&encryption=none&type=ws&path={ws_path}"
                            f"&host={dom}&sni={dom}"
                            f"#{label_base} 🌐{tag_alias}{isp_tag} {cdn_title}"
                        )
                        configs.append(uri)

                    # Trojan WebSocket
                    if sw_cdn_trojan_ws:
                        uri = (
                            f"trojan://{clean_uuid}@{target_host}:{port}"
                            f"?security=tls&type=ws&path={ws_path}"
                            f"&host={dom}&sni={dom}"
                            f"#{label_base} 🛡️{tag_alias}{isp_tag} Trojan-WS"
                        )
                        configs.append(uri)

                    # VLESS gRPC
                    if sw_cdn_vless_grpc:
                        uri = (
                            f"vless://{clean_uuid}@{target_host}:{port}"
                            f"?security=tls&encryption=none&type=grpc&serviceName={grpc_srv}&mode=gun"
                            f"&sni={dom}"
                            f"#{label_base} ⚡{tag_alias}{isp_tag} VLESS-gRPC"
                        )
                        configs.append(uri)

                    # VMess WebSocket
                    if sw_cdn_vmess_ws:
                        vmess_dict = {
                            "v": "2",
                            "ps": f"{label_base} 🚀{tag_alias}{isp_tag} VMess-WS",
                            "add": target_host,
                            "port": port,
                            "id": clean_uuid,
                            "aid": "0",
                            "scy": "auto",
                            "net": "ws",
                            "type": "none",
                            "host": dom,
                            "path": ws_path,
                            "tls": "tls",
                            "sni": dom
                        }
                        raw_json = json.dumps(vmess_dict, ensure_ascii=False)
                        b64_vmess = base64.b64encode(raw_json.encode("utf-8")).decode("utf-8")
                        configs.append(f"vmess://{b64_vmess}")

        return configs

    def get_client_inbounds(self, uuid: str, account_name: str = "TGBot") -> List[str]:
        """
        تولید لینک‌های استاندارد کلاینت با بهره‌گیری از ماتریس هوشمند پروتکل‌ها و چنددامنه‌ای
        """
        return self.generate_matrix_subscription(uuid, account_name)

    def parse_config_details(self, uri: str) -> Dict[str, Any]:
        """
        تجزیه و تحلیل لینک خام کانفیگ و استخراج متادیتا جهت نمایش زیبا در پرتال مشتری
        """
        clean_uri = str(uri or "").strip()
        protocol = "VLESS"
        badge_color = "primary"
        icon = "fas fa-shield-alt"
        transport = "Direct"
        name = "کانفیگ اختصاصی"

        if clean_uri.startswith("vless://"):
            protocol = "VLESS"
            if "security=reality" in clean_uri:
                transport = "Reality Direct"
                badge_color = "success"
                icon = "fas fa-bolt"
            elif "type=ws" in clean_uri:
                transport = "CDN WebSocket"
                badge_color = "info"
                icon = "fas fa-cloud"
            elif "type=grpc" in clean_uri:
                transport = "gRPC Gun"
                badge_color = "primary"
                icon = "fas fa-paper-plane"
            else:
                transport = "TCP Direct"
                badge_color = "secondary"
        elif clean_uri.startswith("trojan://"):
            protocol = "Trojan"
            icon = "fas fa-user-shield"
            if "type=ws" in clean_uri:
                transport = "CDN WebSocket"
                badge_color = "warning"
            else:
                transport = "Direct TLS"
                badge_color = "warning"
        elif clean_uri.startswith("ss://"):
            protocol = "Shadowsocks"
            transport = "2022 AEAD"
            badge_color = "danger"
            icon = "fas fa-key"
        elif clean_uri.startswith("vmess://"):
            protocol = "VMess"
            transport = "CDN WebSocket"
            badge_color = "secondary"
            icon = "fas fa-rocket"

        if "#" in clean_uri:
            try:
                import urllib.parse
                raw_name = clean_uri.split("#", 1)[-1]
                name = urllib.parse.unquote(raw_name)
            except Exception:
                name = clean_uri.split("#", 1)[-1]
        elif clean_uri.startswith("vmess://"):
            try:
                b64_part = clean_uri.replace("vmess://", "")
                missing_padding = len(b64_part) % 4
                if missing_padding:
                    b64_part += "=" * (4 - missing_padding)
                decoded = base64.b64decode(b64_part).decode("utf-8", errors="ignore")
                j = json.loads(decoded)
                name = j.get("ps", "VMess Config")
            except Exception:
                name = "VMess Config"

        return {
            "uri": clean_uri,
            "protocol": protocol,
            "transport": transport,
            "badge_color": badge_color,
            "icon": icon,
            "name": name
        }

    def get_unified_subscription_url(self, token: str, reseller_id: Optional[int] = None, request_host: Optional[str] = None) -> str:
        """
        تولید آدرس یکپارچه سابسکریپشن و پرتال مشتری (Unified Subscription Hub)
        اولویت‌بندی انتخاب دامنه:
        ۱. دامنه اختصاصی نماینده در صورت ثبت برای نماینده مربوطه
        ۲. دامنه‌های با نقش Sub-Only یا Sub در مدیریت دامنه‌های Xray
        ۳. دامنه‌های با نقش CDN در مدیریت دامنه‌های Xray
        ۴. دامنه‌های با نقش Direct در مدیریت دامنه‌های Xray
        ۵. دامنه عمومی سیستم (custom_domain یا panel_domain)
        ۶. دامنه میزبان درخواست (request_host یا request.host_url در صورت اجرای درون وب)
        ۷. آدرس پنل هیدیفای یا پیش‌فرض سیستم
        """
        clean_token = str(token or "").strip()
        if not clean_token:
            return ""

        chosen_domain = ""

        # ۱. دامنه اختصاصی نماینده
        if reseller_id and int(reseller_id) > 0:
            try:
                r_info = self.db.get_reseller(int(reseller_id))
                if r_info and r_info.get("custom_domain"):
                    chosen_domain = str(r_info["custom_domain"]).strip()
            except Exception as e:
                logger.warning(f"Error checking reseller domain for sub url: {e}")

        # ۲. دامنه‌های ثبت‌شده در xray_domains
        if not chosen_domain:
            try:
                x_domains = self.db.get_xray_domains(active_only=True)
                for d in x_domains:
                    if d.get("role", "").lower() in ("sub_only", "sub", "subscription"):
                        chosen_domain = str(d.get("domain", "")).strip()
                        break
                if not chosen_domain:
                    for d in x_domains:
                        if d.get("role", "").lower() == "cdn":
                            chosen_domain = str(d.get("domain", "")).strip()
                            break
                if not chosen_domain:
                    for d in x_domains:
                        if d.get("role", "").lower() == "direct":
                            chosen_domain = str(d.get("domain", "")).strip()
                            break
            except Exception as e:
                logger.warning(f"Error checking xray_domains for sub url: {e}")

        # ۳. تنظیمات عمومی پنل
        if not chosen_domain:
            try:
                chosen_domain = (self.db.get_setting("custom_domain") or self.db.get_setting("panel_domain") or "").strip()
            except Exception:
                pass

        # ۴. هاست ارسال‌شده یا Context جاری فلاسک
        if not chosen_domain and request_host:
            chosen_domain = str(request_host).strip()
        elif not chosen_domain:
            try:
                from flask import has_request_context, request as flask_req
                if has_request_context():
                    chosen_domain = flask_req.host_url.rstrip("/")
            except Exception:
                pass

        # ۵. بررسی آدرس پنل هیدیفای
        if not chosen_domain:
            try:
                h_url = self.db.get_setting("hiddify_url") or os.getenv("HIDIFY_PANEL_URL")
                if h_url:
                    chosen_domain = str(h_url).strip()
            except Exception:
                pass

        # ۶. پیش‌فرض سرور
        if not chosen_domain:
            chosen_domain = os.getenv("PANEL_DOMAIN", "http://localhost:8000").rstrip("/")

        clean_dom = chosen_domain.strip().rstrip("/")
        if not clean_dom.startswith("http://") and not clean_dom.startswith("https://"):
            clean_dom = f"https://{clean_dom}"

        return f"{clean_dom}/sub/{clean_token}"

    # ─── تولید ساختار کانفیگ رسمی هسته Xray (xray config.json) ───

    def generate_full_xray_config(self) -> Dict[str, Any]:
        """
        تولید فایل JSON کامل و استاندارد جهت راه‌اندازی هسته Xray روی سرور اوبونتو
        شامل پورت API داخلی، Reality Inbound، WS Inbound و قوانین مسیریابی بهینه
        """
        creds = self.ensure_reality_credentials()
        priv_key = creds.get("private_key", "")
        short_id = creds.get("short_id", "")

        api_port = int(self.db.get_setting("xray_api_port", 10085) or 10085)
        reality_port = int(self.db.get_setting("xray_reality_port", 443) or 443)
        reality_sni = str(self.db.get_setting("xray_reality_sni", "www.yahoo.com") or "www.yahoo.com").strip()
        ws_port = int(self.db.get_setting("xray_ws_port", 8443) or 8443)
        ws_path = str(self.db.get_setting("xray_ws_path", "/tgbot-ws") or "/tgbot-ws").strip()

        # استخراج کاربران فعال از دیتابیس
        active_clients = []
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hidify_uuid, account_name, telegram_id, id FROM subscriptions 
                WHERE status = 'active' AND (is_deleted = 0 OR is_deleted IS NULL)
            """)
            for row in cursor.fetchall():
                u_id = row["hidify_uuid"]
                if u_id:
                    email_tag = f"sub_{row['id']}@{u_id[:8]}"
                    active_clients.append({
                        "id": u_id,
                        "flow": "xtls-rprx-vision",
                        "email": email_tag
                    })
            conn.close()
        except Exception as e:
            logger.warning(f"Could not load active clients from database: {e}")

        # اینباند Reality با پشتیبانی از پروتکل Vision و X25519
        inbound_reality = {
            "tag": "inbound-reality",
            "port": reality_port,
            "protocol": "vless",
            "settings": {
                "clients": active_clients,
                "decryption": "none"
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                    "show": False,
                    "dest": f"{reality_sni}:443",
                    "xver": 0,
                    "serverNames": [reality_sni],
                    "privateKey": priv_key,
                    "shortIds": [short_id]
                }
            },
            "sniffing": {
                "enabled": True,
                "destOverride": ["http", "tls", "quic"]
            }
        }

        # اینباند WebSocket برای کلودفلر یا تانل
        ws_clients = [{"id": c["id"], "email": c["email"]} for c in active_clients]
        inbound_ws = {
            "tag": "inbound-ws",
            "port": ws_port,
            "protocol": "vless",
            "settings": {
                "clients": ws_clients,
                "decryption": "none"
            },
            "streamSettings": {
                "network": "ws",
                "security": "none",
                "wsSettings": {
                    "path": ws_path
                }
            },
            "sniffing": {
                "enabled": True,
                "destOverride": ["http", "tls"]
            }
        }

        # اینباند پورت کنترل API (gRPC)
        inbound_api = {
            "tag": "api",
            "listen": "127.0.0.1",
            "port": api_port,
            "protocol": "dokodemo-door",
            "settings": {
                "address": "127.0.0.1"
            }
        }

        # لیست اینباندها
        inbounds = [
            inbound_api,
            inbound_reality,
            inbound_ws
        ]

        # اینباند Shadowsocks در صورت فعال بودن
        if self.db.is_setting_enabled("xray_matrix_direct_shadowsocks", default=False):
            ss_port = int(self.db.get_setting("xray_ss_port", 1080) or 1080)
            inbound_ss = {
                "tag": "inbound-ss",
                "port": ss_port,
                "protocol": "shadowsocks",
                "settings": {
                    "method": "2022-blake3-aes-128-gcm",
                    "password": base64.b64encode(b"tgbotshadowsocks").decode("utf-8"),
                    "network": "tcp,udp"
                }
            }
            inbounds.append(inbound_ss)

        # لیست اوت‌باندها
        outbounds = [
            {
                "protocol": "freedom",
                "tag": "direct"
            },
            {
                "protocol": "blackhole",
                "tag": "block"
            }
        ]

        # اوت‌باند WARP در صورت فعال بودن
        if self.db.is_setting_enabled("xray_warp_enabled", default=False):
            outbounds.append({
                "protocol": "socks",
                "tag": "warp",
                "settings": {
                    "servers": [
                        {"address": "127.0.0.1", "port": 40000}
                    ]
                }
            })

        # قوانین روتینگ و ضداسپم
        routing_rules = [
            {
                "type": "field",
                "inboundTag": ["api"],
                "outboundTag": "api"
            }
        ]

        if self.db.is_setting_enabled("xray_block_smtp", default=True):
            routing_rules.append({
                "type": "field",
                "port": "25,465,587",
                "network": "tcp",
                "outboundTag": "block"
            })

        routing_rules.append({
            "type": "field",
            "ip": ["geoip:private"],
            "outboundTag": "block"
        })

        if self.db.is_setting_enabled("xray_block_iran", default=False):
            routing_rules.append({
                "type": "field",
                "ip": ["geoip:ir"],
                "outboundTag": "block"
            })

        if self.db.is_setting_enabled("xray_warp_enabled", default=False):
            raw_warp_domains = str(self.db.get_setting("xray_warp_domains", "openai.com, chatgpt.com, anthropic.com, claude.ai, spotify.com, netflix.com") or "")
            warp_domains = [f"domain:{d.strip()}" for d in raw_warp_domains.split(",") if d.strip()]
            if warp_domains:
                routing_rules.append({
                    "type": "field",
                    "domain": warp_domains,
                    "outboundTag": "warp"
                })

        config = {
            "log": {
                "loglevel": "warning"
            },
            "api": {
                "tag": "api",
                "services": [
                    "HandlerService",
                    "StatsService",
                    "LoggerService"
                ]
            },
            "stats": {},
            "policy": {
                "levels": {
                    "0": {
                        "statsUserUplink": True,
                        "statsUserDownlink": True
                    }
                },
                "system": {
                    "statsInboundUplink": True,
                    "statsInboundDownlink": True
                }
            },
            "inbounds": inbounds,
            "outbounds": outbounds,
            "routing": {
                "domainStrategy": "AsIs",
                "rules": routing_rules
            }
        }

        return config

    # ─── دستورات تعاملی Xray API (افزودن، حذف، آمار مصرف) ───

    def add_user_to_core(self, uuid: str, email: str) -> bool:
        """افزودن بلادرنگ کاربر به اینباندهای فعال در هسته Xray"""
        if not self.is_installed() or not self.is_running():
            return False

        api_port = int(self.db.get_setting("xray_api_port", 10085) or 10085)
        # دستور اضافه کردن کاربر به Reality
        cmd_reality = [
            self._binary_path, "api", "addu",
            f"--server=127.0.0.1:{api_port}",
            f"--inbound=inbound-reality",
            f"--email={email}",
            f"--uuid={uuid}",
            "--flow=xtls-rprx-vision"
        ]
        # دستور اضافه کردن به WebSocket
        cmd_ws = [
            self._binary_path, "api", "addu",
            f"--server=127.0.0.1:{api_port}",
            f"--inbound=inbound-ws",
            f"--email={email}",
            f"--uuid={uuid}"
        ]

        success = True
        for cmd in (cmd_reality, cmd_ws):
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if res.returncode != 0:
                    logger.warning(f"Xray addu warning: {res.stderr.strip() or res.stdout.strip()}")
            except Exception as e:
                logger.error(f"Error executing xray addu: {e}")
                success = False

        return success

    def remove_user_from_core(self, email: str) -> bool:
        """حذف بلادرنگ کاربر از هسته هنگام اتمام حجم یا انقضا"""
        if not self.is_installed() or not self.is_running():
            return False

        api_port = int(self.db.get_setting("xray_api_port", 10085) or 10085)
        success = True
        for inbound in ("inbound-reality", "inbound-ws"):
            cmd = [
                self._binary_path, "api", "rmu",
                f"--server=127.0.0.1:{api_port}",
                f"--inbound={inbound}",
                f"--email={email}"
            ]
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            except Exception as e:
                logger.error(f"Error executing xray rmu: {e}")
                success = False

        return success

    def query_all_users_traffic(self) -> Dict[str, Dict[str, int]]:
        """
        استعلام بلادرنگ ترافیک آپلینک و دانلینک کلیه کاربران از Xray API
        خروجی: {email: {"uplink": bytes, "downlink": bytes, "total": bytes}}
        """
        traffic_map: Dict[str, Dict[str, int]] = {}
        if not self.is_installed() or not self.is_running():
            return traffic_map

        api_port = int(self.db.get_setting("xray_api_port", 10085) or 10085)
        cmd = [
            self._binary_path, "api", "statsquery",
            f"--server=127.0.0.1:{api_port}",
            "--pattern=user>>>"
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
            if res.returncode == 0 and res.stdout:
                parsed = json.loads(res.stdout)
                stat_list = parsed.get("stat") or []
                for item in stat_list:
                    name = item.get("name", "")
                    value = int(item.get("value", 0))
                    # نام با الگو: user>>>{email}>>>traffic>>>{uplink/downlink}
                    parts = name.split(">>>")
                    if len(parts) >= 4 and parts[0] == "user" and parts[2] == "traffic":
                        user_email = parts[1]
                        dir_type = parts[3]
                        if user_email not in traffic_map:
                            traffic_map[user_email] = {"uplink": 0, "downlink": 0, "total": 0}
                        if dir_type == "uplink":
                            traffic_map[user_email]["uplink"] += value
                        elif dir_type == "downlink":
                            traffic_map[user_email]["downlink"] += value
                        traffic_map[user_email]["total"] = traffic_map[user_email]["uplink"] + traffic_map[user_email]["downlink"]

        except Exception as e:
            logger.error(f"Error querying Xray stats: {e}")

        return traffic_map

    def write_config_file(self, config_path: str = "/usr/local/etc/xray/config.json") -> bool:
        """ذخیره فایل پیکربندی کامل در مسیر سیستمی Xray"""
        try:
            config = self.generate_full_xray_config()
            target_path = Path(config_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved Xray config to {config_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing Xray config file: {e}")
            return False

    def restart_service(self) -> Tuple[bool, str]:
        """ری‌استارت کردن سرویس Xray از طریق systemctl"""
        if os.name == "nt":
            return False, "سرویس‌های systemd تنها در سیستم‌عامل‌های لینوکس در دسترس هستند."
        if not shutil.which("systemctl"):
            return False, "ابزار systemctl در این محیط یافت نشد (احتمالاً محیط کانتینری Docker/Railway است)."
        try:
            res = subprocess.run(["systemctl", "restart", "xray"], capture_output=True, text=True, timeout=8)
            if res.returncode == 0:
                return True, "سرویس Xray با موفقیت ری‌استارت شد."
            return False, res.stderr.strip() or res.stdout.strip() or "خطا در ری‌استارت سرویس"
        except Exception as e:
            return False, str(e)

    def get_service_status(self) -> Dict[str, Any]:
        """دریافت وضعیت کامل و جامع سرویس هسته Xray جهت نمایش در پنل وب"""
        installed = self.is_installed()
        running = self.is_running()
        enabled = self.is_enabled()

        # شمارش کاربران فعال سیستم
        active_count = 0
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM subscriptions WHERE status = 'active' AND (is_deleted = 0 OR is_deleted IS NULL)")
            row = cursor.fetchone()
            if row:
                active_count = row["cnt"]
            conn.close()
        except Exception:
            pass

        domain = (
            self.db.get_setting("xray_direct_domain")
            or self.db.get_setting("custom_domain")
            or os.getenv("PANEL_DOMAIN")
            or ""
        ).strip().replace("https://", "").replace("http://", "").rstrip("/")

        credentials = self.ensure_reality_credentials()

        domains = []
        try:
            domains = self.db.get_xray_domains()
        except Exception:
            pass

        return {
            "is_installed": installed,
            "binary_path": self._binary_path or "یافت نشد",
            "is_enabled": enabled,
            "is_running": running,
            "domains": domains,
            "domains_count": len(domains),
            # ماتریس سوئیچ‌ها
            "matrix_direct_reality_tcp": self.db.is_setting_enabled("xray_matrix_direct_reality_tcp", default=self.db.is_setting_enabled("xray_reality_enabled", default=True)),
            "matrix_direct_reality_grpc": self.db.is_setting_enabled("xray_matrix_direct_reality_grpc", default=False),
            "matrix_direct_trojan": self.db.is_setting_enabled("xray_matrix_direct_trojan", default=False),
            "matrix_cdn_vless_ws": self.db.is_setting_enabled("xray_matrix_cdn_vless_ws", default=self.db.is_setting_enabled("xray_ws_enabled", default=True)),
            "matrix_cdn_trojan_ws": self.db.is_setting_enabled("xray_matrix_cdn_trojan_ws", default=False),
            "matrix_cdn_vless_grpc": self.db.is_setting_enabled("xray_matrix_cdn_vless_grpc", default=False),
            "matrix_cdn_vmess_ws": self.db.is_setting_enabled("xray_matrix_cdn_vmess_ws", default=False),
            "matrix_direct_shadowsocks": self.db.is_setting_enabled("xray_matrix_direct_shadowsocks", default=False),
            "include_external_node": self.db.is_setting_enabled("xray_include_external_node", default=True),
            "reality_port": int(self.db.get_setting("xray_reality_port", 443) or 443),
            "reality_sni": str(self.db.get_setting("xray_reality_sni", "www.yahoo.com") or "www.yahoo.com").strip(),
            "reality_pub_key": credentials.get("public_key", ""),
            "reality_priv_key": credentials.get("private_key", ""),
            "reality_short_id": credentials.get("short_id", ""),
            "ws_port": int(self.db.get_setting("xray_ws_port", 8443) or 8443),
            "ws_path": str(self.db.get_setting("xray_ws_path", "/tgbot-ws") or "/tgbot-ws").strip(),
            "ss_port": int(self.db.get_setting("xray_ss_port", 1080) or 1080),
            "warp_enabled": self.db.is_setting_enabled("xray_warp_enabled", default=False),
            "warp_domains": str(self.db.get_setting("xray_warp_domains", "openai.com, chatgpt.com, anthropic.com, claude.ai, spotify.com, netflix.com") or "openai.com, chatgpt.com, anthropic.com, claude.ai, spotify.com, netflix.com"),
            "block_smtp": self.db.is_setting_enabled("xray_block_smtp", default=True),
            "block_iran": self.db.is_setting_enabled("xray_block_iran", default=False),
            "cdn_domain": self.db.get_setting("xray_cdn_domain") or "",
            "direct_domain": domain,
            "server_ip": self.db.get_setting("xray_server_ip") or "",
            "api_port": int(self.db.get_setting("xray_api_port", 10085) or 10085),
            "active_clients_count": active_count
        }

    def sync_traffic_with_database(self) -> Dict[str, Any]:
        """
        همگام‌سازی مصرف ترافیک بلادرنگ کاربران از هسته Xray به دیتابیس
        محاسبه میزان دلتای مصرفی و مسدودسازی خودکار کاربران تمام شده
        """
        if not self.is_installed() or not self.is_running():
            return {"synced": 0, "blocked": 0, "message": "Xray is not running"}

        stats = self.query_all_users_traffic()
        if not stats:
            return {"synced": 0, "blocked": 0, "message": "No traffic records returned"}

        synced_count = 0
        blocked_count = 0

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            for email, data in stats.items():
                total_bytes = data.get("total", 0)
                if total_bytes <= 0:
                    continue

                sub_id = None
                if email.startswith("sub_") and "@" in email:
                    try:
                        sub_id_part = email.split("@")[0].replace("sub_", "")
                        sub_id = int(sub_id_part)
                    except Exception:
                        pass

                sub_row = None
                if sub_id:
                    cursor.execute("SELECT id, hidify_uuid, data_limit, data_used, status FROM subscriptions WHERE id = ?", (sub_id,))
                    sub_row = cursor.fetchone()

                if not sub_row and "@" in email:
                    prefix = email.split("@")[1]
                    cursor.execute("SELECT id, hidify_uuid, data_limit, data_used, status FROM subscriptions WHERE hidify_uuid LIKE ?", (f"{prefix}%",))
                    sub_row = cursor.fetchone()

                if not sub_row:
                    continue

                actual_id = sub_row["id"]
                data_limit_gb = float(sub_row["data_limit"] or 0)
                curr_used_gb = float(sub_row["data_used"] or 0)

                xray_reported_gb = total_bytes / (1024 ** 3)

                if xray_reported_gb > curr_used_gb:
                    new_used = round(xray_reported_gb, 4)
                    cursor.execute("UPDATE subscriptions SET data_used = ?, updated_at = datetime('now') WHERE id = ?", (new_used, actual_id))
                    synced_count += 1

                    if data_limit_gb > 0 and new_used >= data_limit_gb:
                        cursor.execute("UPDATE subscriptions SET status = 'expired', updated_at = datetime('now') WHERE id = ?", (actual_id,))
                        self.remove_user_from_core(email)
                        blocked_count += 1
                        logger.info(f"User {email} (Sub ID {actual_id}) exceeded data limit ({new_used}/{data_limit_gb} GB) and was removed from Xray core.")
                        try:
                            tg_id = sub_row["telegram_id"] if "telegram_id" in sub_row.keys() else None
                            acc_n = sub_row["account_name"] if "account_name" in sub_row.keys() else "کاربر گرامی"
                            if tg_id and int(tg_id) > 0:
                                self._notify_user_limit_exceeded(int(tg_id), str(acc_n), new_used, data_limit_gb)
                        except Exception as e_nt:
                            logger.warning(f"Could not prepare limit notification: {e_nt}")

            conn.commit()
        except Exception as e:
            logger.error(f"Error syncing Xray traffic to database: {e}")
        finally:
            conn.close()

        return {"synced": synced_count, "blocked": blocked_count, "total_users": len(stats)}

    def _notify_user_limit_exceeded(self, telegram_id: int, account_name: str, used_gb: float, limit_gb: float) -> None:
        """ارسال اعلان اتمام حجم اشتراک به کاربر در تلگرام به صورت غیراستاتیک و ایمن"""
        try:
            from bot import bot
            import asyncio
            msg = (
                f"⚠️ **هشدار اتمام حجم اشتراک**\n\n"
                f"👤 نام اکانت: `{account_name}`\n"
                f"📊 مصرف نهایی: **{used_gb:.2f} گیگابایت** از سقف **{limit_gb:.2f} گیگابایت**\n\n"
                f"⛔️ حجم مجاز بسته شما به پایان رسید و اتصال به صورت خودکار قطع گردید.\n"
                f"🔄 جهت تمدید اشتراک و ادامه اتصال، از منوی ربات گزینه «🔄 تمدید اشتراک» را لمس فرمایید."
            )

            def _async_send():
                try:
                    asyncio.run(bot.send_message(chat_id=telegram_id, text=msg, parse_mode="Markdown"))
                except Exception as ex:
                    logger.warning(f"Could not deliver telegram limit notification to {telegram_id}: {ex}")

            threading.Thread(target=_async_send, daemon=True).start()
        except Exception as e:
            logger.warning(f"Error setting up limit notification for {telegram_id}: {e}")

    def start_traffic_worker(self, interval_seconds: int = 60) -> bool:
        """شروع مانیتورینگ دوره‌ای و خودکار مصرف ترافیک کاربران هسته Xray در پس‌زمینه"""
        if self._worker_running and self._worker_thread and self._worker_thread.is_alive():
            logger.info("Xray traffic sync worker is already running.")
            return True

        self._worker_interval = max(10, interval_seconds)
        self._worker_running = True
        self._worker_thread = threading.Thread(
            target=self._traffic_worker_loop,
            daemon=True,
            name="XrayTrafficSyncWorker"
        )
        self._worker_thread.start()
        logger.info(f"Started Xray traffic sync daemon (interval: {self._worker_interval}s)")
        return True

    def stop_traffic_worker(self) -> bool:
        """توقف ورکر پس‌زمینه مانیتورینگ ترافیک"""
        self._worker_running = False
        logger.info("Stopping Xray traffic sync daemon...")
        return True

    def _traffic_worker_loop(self) -> None:
        """حلقه اجرایی ورکر پس‌زمینه"""
        time.sleep(5)
        while self._worker_running:
            try:
                if self.is_enabled() and self.is_running():
                    res = self.sync_traffic_with_database()
                    self._last_sync_time = time.time()
                    self._last_sync_stats = res
                    if res.get("synced", 0) > 0 or res.get("blocked", 0) > 0:
                        logger.info(f"[XrayDaemon] Synced {res.get('synced', 0)} users, blocked {res.get('blocked', 0)} users.")
            except Exception as e:
                logger.error(f"Error in Xray traffic worker tick: {e}")

            for _ in range(self._worker_interval):
                if not self._worker_running:
                    break
                time.sleep(1)

    def get_daemon_status(self) -> Dict[str, Any]:
        """استعلام وضعیت کارکرد ورکر پس‌زمینه جهت نمایش در پنل مدیریت"""
        running = bool(self._worker_running and self._worker_thread and self._worker_thread.is_alive())
        now = time.time()
        time_ago_sec = int(now - self._last_sync_time) if self._last_sync_time > 0 else None
        
        last_sync_str = "هنوز انجام نشده"
        if self._last_sync_time > 0:
            if time_ago_sec < 60:
                last_sync_str = f"{time_ago_sec} ثانیه قبل"
            else:
                last_sync_str = f"{time_ago_sec // 60} دقیقه قبل"

        return {
            "is_running": running,
            "interval_seconds": self._worker_interval,
            "last_sync_time": self._last_sync_time,
            "last_sync_human": last_sync_str,
            "last_stats": self._last_sync_stats
        }


# نمونه یکتای ماژول
xray_service = XrayService()
get_unified_subscription_url = xray_service.get_unified_subscription_url
parse_config_details = xray_service.parse_config_details
start_traffic_worker = xray_service.start_traffic_worker
stop_traffic_worker = xray_service.stop_traffic_worker
get_daemon_status = xray_service.get_daemon_status

