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
import json
import shutil
import base64
import secrets
import logging
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

    def get_client_inbounds(self, uuid: str, account_name: str = "TGBot") -> List[str]:
        """
        تولید لینک‌های استاندارد VLESS Reality و WebSocket برای قرارگیری در سابسکریپشن
        """
        if not uuid:
            return []

        clean_uuid = str(uuid).strip()
        label_base = account_name or "VPN"

        # ۱. مشخصات هاست و دامنه
        domain = (
            self.db.get_setting("xray_direct_domain")
            or self.db.get_setting("custom_domain")
            or os.getenv("PANEL_DOMAIN")
            or ""
        ).strip()
        # حذف پروتکل اگر اشتباها وارد شده باشد
        domain = domain.replace("https://", "").replace("http://", "").rstrip("/")

        # اگر دامنه‌ای وارد نشده بود، تلاش برای استخراج IP عمومی سرور
        if not domain:
            domain = self.db.get_setting("xray_server_ip") or "127.0.0.1"

        credentials = self.ensure_reality_credentials()
        pub_key = credentials.get("public_key", "")
        short_id = credentials.get("short_id", "")

        configs = []

        # ۱. کانفیگ VLESS + Reality (مستقیم با پینگ عالی و ضد فیلتر)
        reality_enabled = self.db.is_setting_enabled("xray_reality_enabled", default=True)
        if reality_enabled and pub_key:
            reality_port = int(self.db.get_setting("xray_reality_port", 443) or 443)
            sni = str(self.db.get_setting("xray_reality_sni", "www.yahoo.com") or "www.yahoo.com").strip()
            reality_uri = (
                f"vless://{clean_uuid}@{domain}:{reality_port}"
                f"?security=reality&encryption=none&pbk={pub_key}&headerType=none"
                f"&fp=chrome&spx=%2F&type=tcp&sni={sni}&sid={short_id}"
                f"#{label_base} ⚡ Reality Direct"
            )
            configs.append(reality_uri)

        # ۲. کانفیگ VLESS + WebSocket / CDN (مناسب برای شرایط اختلال شدید اینترنت)
        ws_enabled = self.db.is_setting_enabled("xray_ws_enabled", default=True)
        cdn_domain = str(self.db.get_setting("xray_cdn_domain") or domain).strip()
        if ws_enabled and cdn_domain:
            ws_port = int(self.db.get_setting("xray_ws_port", 8443) or 8443)
            ws_path = str(self.db.get_setting("xray_ws_path", "/tgbot-ws") or "/tgbot-ws").strip()
            if not ws_path.startswith("/"):
                ws_path = "/" + ws_path
            ws_uri = (
                f"vless://{clean_uuid}@{cdn_domain}:{ws_port}"
                f"?security=tls&encryption=none&type=ws&path={ws_path}"
                f"&host={cdn_domain}&sni={cdn_domain}"
                f"#{label_base} 🌐 Cloud CDN"
            )
            configs.append(ws_uri)

        return configs

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
            "inbounds": [
                inbound_api,
                inbound_reality,
                inbound_ws
            ],
            "outbounds": [
                {
                    "protocol": "freedom",
                    "tag": "direct"
                },
                {
                    "protocol": "blackhole",
                    "tag": "block"
                }
            ],
            "routing": {
                "domainStrategy": "AsIs",
                "rules": [
                    {
                        "type": "field",
                        "inboundTag": ["api"],
                        "outboundTag": "api"
                    },
                    {
                        "type": "field",
                        "ip": ["geoip:private"],
                        "outboundTag": "block"
                    }
                ]
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

        return {
            "is_installed": installed,
            "binary_path": self._binary_path or "یافت نشد",
            "is_enabled": enabled,
            "is_running": running,
            "reality_enabled": self.db.is_setting_enabled("xray_reality_enabled", default=True),
            "ws_enabled": self.db.is_setting_enabled("xray_ws_enabled", default=True),
            "include_external_node": self.db.is_setting_enabled("xray_include_external_node", default=True),
            "reality_port": int(self.db.get_setting("xray_reality_port", 443) or 443),
            "reality_sni": str(self.db.get_setting("xray_reality_sni", "www.yahoo.com") or "www.yahoo.com").strip(),
            "reality_pub_key": credentials.get("public_key", ""),
            "reality_priv_key": credentials.get("private_key", ""),
            "reality_short_id": credentials.get("short_id", ""),
            "ws_port": int(self.db.get_setting("xray_ws_port", 8443) or 8443),
            "ws_path": str(self.db.get_setting("xray_ws_path", "/tgbot-ws") or "/tgbot-ws").strip(),
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

            conn.commit()
        except Exception as e:
            logger.error(f"Error syncing Xray traffic to database: {e}")
        finally:
            conn.close()

        return {"synced": synced_count, "blocked": blocked_count, "total_users": len(stats)}


# نمونه یکتای ماژول
xray_service = XrayService()
