# -*- coding: utf-8 -*-
"""
تست‌های اعتبارسنجی ماژول اختصاصی Xray-core و سابسکریپشن ترکیبی
"""

import unittest
import base64
import json
from unittest.mock import patch, MagicMock
from services.xray_service import XrayService, xray_service
import database
import dashboard


class TestXrayService(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        self.service = XrayService(self.db)
        self.app = dashboard.app
        self.client = self.app.test_client()

    def test_generate_x25519_keypair(self):
        """بررسی تولید جفت‌کلید رمزنگاری استاندارد X25519"""
        keys = self.service.generate_x25519_keypair()
        self.assertIn("private_key", keys)
        self.assertIn("public_key", keys)
        self.assertIn("short_id", keys)
        self.assertTrue(len(keys["private_key"]) > 20)
        self.assertTrue(len(keys["public_key"]) > 20)
        self.assertEqual(len(keys["short_id"]), 8)

    def test_ensure_reality_credentials(self):
        """بررسی ایجاد و ذخیره پایدار کلیدها در تنظیمات"""
        creds = self.service.ensure_reality_credentials()
        self.assertIsNotNone(creds.get("public_key"))
        self.assertIsNotNone(creds.get("private_key"))
        self.assertIsNotNone(creds.get("short_id"))

        # بررسی وجود در دیتابیس
        db_pub = self.db.get_setting("xray_reality_public_key")
        self.assertEqual(db_pub, creds["public_key"])

    def test_get_client_inbounds(self):
        """بررسی تولید لینک‌های استاندارد vless:// برای کلاینت"""
        self.db.set_setting("xray_reality_enabled", "1")
        self.db.set_setting("xray_ws_enabled", "1")
        self.db.set_setting("xray_reality_sni", "www.yahoo.com")
        self.db.set_setting("xray_direct_domain", "vpn.myserver.com")

        test_uuid = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        uris = self.service.get_client_inbounds(test_uuid, account_name="TestUser")

        self.assertGreaterEqual(len(uris), 1)
        # بررسی وجود پروتکل Reality
        reality_uris = [u for u in uris if "security=reality" in u]
        self.assertEqual(len(reality_uris), 1)
        self.assertIn(test_uuid, reality_uris[0])
        self.assertIn("sni=www.yahoo.com", reality_uris[0])
        self.assertIn("vpn.myserver.com", reality_uris[0])
        self.assertIn("TestUser ⚡ Reality Direct", reality_uris[0])

        # بررسی وجود پروتکل WebSocket
        ws_uris = [u for u in uris if "type=ws" in u]
        self.assertEqual(len(ws_uris), 1)
        self.assertIn("TestUser 🌐 Cloud CDN", ws_uris[0])

    def test_generate_full_xray_config(self):
        """بررسی ساختار استاندارد فایل config.json برای اجرای باینری Xray"""
        cfg = self.service.generate_full_xray_config()
        self.assertIn("inbounds", cfg)
        self.assertIn("outbounds", cfg)
        self.assertIn("routing", cfg)
        self.assertIn("api", cfg)
        self.assertIn("stats", cfg)

        tags = [inb.get("tag") for inb in cfg["inbounds"]]
        self.assertIn("api", tags)
        self.assertIn("inbound-reality", tags)
        self.assertIn("inbound-ws", tags)

    def test_parse_subscription_configs_plaintext_and_base64(self):
        """بررسی عملکرد تابع تفکیک‌کننده کانفیگ‌ها در حالت خام و Base64"""
        sample_configs = [
            "vless://uuid1@1.2.3.4:443?security=reality#Config1",
            "vmess://eyJ2IjoiMiIsInBzIjoiVGVzdCJ9#Config2"
        ]
        # تست با متن ساده چندخطی
        raw_text = "\n".join(sample_configs)
        parsed = dashboard._parse_subscription_configs(raw_text)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0], sample_configs[0])

        # تست با رشته Base64
        b64_text = base64.b64encode(raw_text.encode("utf-8")).decode("utf-8")
        parsed_b64 = dashboard._parse_subscription_configs(b64_text)
        self.assertEqual(len(parsed_b64), 2)
        self.assertEqual(parsed_b64[1], sample_configs[1])

    def test_smart_subscription_proxy_hybrid_merging(self):
        """بررسی ادغام هوشمند کانفیگ‌های هسته داخلی با کانفیگ‌های نود خارجی"""
        # ایجاد اشتراک آزمایشی فعال
        conn = self.db.get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO subscriptions 
            (id, hidify_uuid, telegram_id, plan_id, plan_name, account_name, data_limit, data_used, duration, status, is_deleted)
            VALUES (88881, 'uuid-hybrid-test-1234', 0, 'plan1', 'تست ترکیبی', 'HybridUser', 50.0, 5.0, 30, 'active', 0)
        """)
        conn.commit()
        conn.close()

        try:
            self.db.set_setting("xray_core_enabled", "1")
            self.db.set_setting("xray_include_external_node", "1")

            # شبیه‌سازی فراخوانی سابسکریپشن توسط کلاینت v2rayNG
            with self.client as client:
                res = client.get(
                    "/sub/uuid-hybrid-test-1234",
                    headers={"User-Agent": "v2rayNG/1.8.12"}
                )
                self.assertEqual(res.status_code, 200)
                self.assertIn("Subscription-Userinfo", res.headers)
                self.assertIn("Profile-Title", res.headers)

                # بازگشایی و دیکود محتوای Base64 برگشتی
                decoded = base64.b64decode(res.data).decode("utf-8")
                self.assertIn("vless://", decoded)
                self.assertIn("HybridUser ⚡ Reality Direct", decoded)
        finally:
            conn = self.db.get_connection()
            conn.execute("DELETE FROM subscriptions WHERE id=88881")
            conn.commit()
            conn.close()

    def test_api_client_config(self):
        """بررسی API اختصاصی برنامه ویندوز و اندروید"""
        conn = self.db.get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO subscriptions 
            (id, hidify_uuid, telegram_id, plan_id, plan_name, account_name, data_limit, data_used, duration, status, is_deleted)
            VALUES (88882, 'uuid-client-test-5678', 0, 'plan_vip', 'بسته طلایی', 'ClientUser', 100.0, 15.5, 30, 'active', 0)
        """)
        conn.commit()
        conn.close()

        try:
            self.db.set_setting("xray_core_enabled", "1")
            with self.client as client:
                res = client.get("/api/client/v1/config/uuid-client-test-5678")
                self.assertEqual(res.status_code, 200)
                data = res.get_json()
                self.assertTrue(data["success"])
                self.assertEqual(data["user"]["account_name"], "ClientUser")
                self.assertEqual(data["user"]["data_limit_gb"], 100.0)
                self.assertEqual(data["user"]["data_used_gb"], 15.5)
                self.assertIn("portal_url", data)
                self.assertIn("nodes", data)
        finally:
            conn = self.db.get_connection()
            conn.execute("DELETE FROM subscriptions WHERE id=88882")
            conn.commit()
            conn.close()

    def test_xray_domains_crud(self):
        """بررسی عملیات پایگاه داده برای افزودن، خواندن، ویرایش، تغییر وضعیت و حذف دامنه‌ها"""
        # ۱. افزودن دامنه
        add_res = self.db.add_xray_domain(
            domain="cdn1.testdomain.com",
            role="cdn",
            alias="کلودفلر ۱",
            sni="cdn1.testdomain.com",
            clean_ips="104.16.1.1, 104.16.2.2",
            port=443
        )
        self.assertTrue(add_res["success"])
        domain_id = add_res["id"]

        # ۲. خواندن
        domain = self.db.get_xray_domain(domain_id)
        self.assertIsNotNone(domain)
        self.assertEqual(domain["domain"], "cdn1.testdomain.com")
        self.assertEqual(domain["role"], "cdn")
        self.assertEqual(domain["alias"], "کلودفلر ۱")
        self.assertEqual(domain["clean_ips"], "104.16.1.1, 104.16.2.2")
        self.assertEqual(domain["is_active"], 1)

        # ۳. ویرایش
        upd_res = self.db.update_xray_domain(domain_id, alias="کلودفلر ویرایش‌شده", port=8443)
        self.assertTrue(upd_res["success"])
        updated = self.db.get_xray_domain(domain_id)
        self.assertEqual(updated["alias"], "کلودفلر ویرایش‌شده")
        self.assertEqual(updated["port"], 8443)

        # ۴. تغییر وضعیت
        tog_res = self.db.toggle_xray_domain(domain_id)
        self.assertTrue(tog_res["success"])
        self.assertEqual(tog_res["is_active"], 0)

        # ۵. حذف
        del_res = self.db.delete_xray_domain(domain_id)
        self.assertTrue(del_res)
        self.assertIsNone(self.db.get_xray_domain(domain_id))

    def test_multi_domain_subscription_matrix(self):
        """بررسی ساخت ماتریس ترکیبی کانفیگ‌ها با چندین دامنه CDN و Direct (مشابه هیدیفای)"""
        # پاکسازی موقت دامنه‌های قبلی
        conn = self.db.get_connection()
        conn.execute("DELETE FROM xray_domains")
        conn.commit()
        conn.close()

        # افزودن ۱ دامنه مستقیم و ۲ دامنه CDN
        d1 = self.db.add_xray_domain(domain="direct.test.com", role="direct", alias="سرور مستقیم", port=443)
        d2 = self.db.add_xray_domain(domain="cdn1.test.com", role="cdn", alias="کلودفلر ۱", port=8443)
        d3 = self.db.add_xray_domain(domain="cdn2.test.com", role="cdn", alias="کلودفلر ۲", port=8443)

        try:
            self.db.set_setting("xray_matrix_direct_reality_tcp", "1")
            self.db.set_setting("xray_matrix_cdn_vless_ws", "1")
            self.db.set_setting("xray_matrix_cdn_trojan_ws", "1")
            self.db.set_setting("xray_matrix_cdn_vless_grpc", "0")
            self.db.set_setting("xray_matrix_cdn_vmess_ws", "0")

            test_uuid = "11223344-5566-7788-99aa-bbccddeeff00"
            configs = self.service.generate_matrix_subscription(test_uuid, account_name="MultiUser")

            # باید ۱ کانفیگ برای دامنه مستقیم + ۲ کانفیگ برای هر دامنه CDN (جمعاً ۵ کانفیگ) تولید شود
            self.assertGreaterEqual(len(configs), 5)

            # بررسی دامنه مستقیم
            direct_configs = [c for c in configs if "direct.test.com" in c and "security=reality" in c]
            self.assertGreaterEqual(len(direct_configs), 1)

            # بررسی دامنه CDN 1
            cdn1_configs = [c for c in configs if "cdn1.test.com" in c]
            self.assertGreaterEqual(len(cdn1_configs), 2)  # VLESS-WS + Trojan-WS

            # بررسی دامنه CDN 2
            cdn2_configs = [c for c in configs if "cdn2.test.com" in c]
            self.assertGreaterEqual(len(cdn2_configs), 2)

        finally:
            conn = self.db.get_connection()
            conn.execute("DELETE FROM xray_domains WHERE id IN (?, ?, ?)", (d1["id"], d2["id"], d3["id"]))
            conn.commit()
            conn.close()

    def test_clean_ips_in_subscription_matrix(self):
        """بررسی اتصال به آی‌پی‌های تمیز کلودفلر همراه با هدر SNI دامنه"""
        conn = self.db.get_connection()
        conn.execute("DELETE FROM xray_domains")
        conn.commit()
        conn.close()

        d = self.db.add_xray_domain(
            domain="cdn.clean-test.com",
            role="cdn",
            alias="ایرانسل کلودفلر",
            clean_ips="162.159.192.1, 104.16.24.5",
            port=443
        )

        try:
            self.db.set_setting("xray_matrix_cdn_vless_ws", "1")
            self.db.set_setting("xray_matrix_cdn_trojan_ws", "0")
            self.db.set_setting("xray_matrix_cdn_vless_grpc", "0")

            test_uuid = "22334455-6677-8899-aabb-ccddeeff0011"
            configs = self.service.generate_matrix_subscription(test_uuid, account_name="CleanIpUser")

            # باید ۲ کانفیگ با هاست‌های مربوط به آی‌پی‌های تمیز تولید شود
            ip1_configs = [c for c in configs if "@162.159.192.1:443" in c and "sni=cdn.clean-test.com" in c]
            ip2_configs = [c for c in configs if "@104.16.24.5:443" in c and "sni=cdn.clean-test.com" in c]

            self.assertEqual(len(ip1_configs), 1)
            self.assertEqual(len(ip2_configs), 1)

        finally:
            conn = self.db.get_connection()
            conn.execute("DELETE FROM xray_domains WHERE id = ?", (d["id"],))
            conn.commit()
            conn.close()

    def test_admin_xray_core_page(self):
        """بررسی دسترسی و رندر صفحه مستقل هسته Xray در منوی شبکه"""
        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["role"] = "admin"
            sess["admin_role"] = "super_admin"

        resp = self.client.get("/admin/xray")
        self.assertEqual(resp.status_code, 200)
        content = resp.data.decode("utf-8")
        self.assertIn("هسته اختصاصی Xray و مدیریت پروتکل‌ها", content)
        self.assertIn("پروتکل‌ها و اینباندها", content)
        self.assertIn("دامنه‌ها و کلین آی‌پی اپراتورها", content)

    def test_shadowsocks_in_matrix(self):
        """بررسی تولید کانفیگ سبک Shadowsocks 2022 در صورت فعال‌سازی در ماتریس"""
        self.db.set_setting("xray_matrix_direct_shadowsocks", "1")
        self.db.set_setting("xray_direct_domain", "ss.server.com")
        self.db.set_setting("xray_ss_port", "1080")

        test_uuid = "33445566-7788-9900-aabb-ccddeeff0022"
        configs = self.service.generate_matrix_subscription(test_uuid, account_name="SSUser")

        ss_configs = [c for c in configs if c.startswith("ss://")]
        self.assertGreaterEqual(len(ss_configs), 1)
        self.assertIn("@ss.server.com:1080", ss_configs[0])
        self.assertIn("Shadowsocks 2022", ss_configs[0])

    def test_warp_and_routing_config(self):
        """بررسی تولید ساختار WARP و روتینگ ضداسپم در config.json هسته"""
        self.db.set_setting("xray_warp_enabled", "1")
        self.db.set_setting("xray_block_smtp", "1")
        self.db.set_setting("xray_warp_domains", "openai.com, chatgpt.com")

        cfg = self.service.generate_full_xray_config()

        # بررسی وجود اوت‌باند warp
        outbound_tags = [o.get("tag") for o in cfg["outbounds"]]
        self.assertIn("warp", outbound_tags)

        # بررسی وجود رول روتینگ برای وارپ
        rules = cfg["routing"]["rules"]
        warp_rules = [r for r in rules if r.get("outboundTag") == "warp"]
        self.assertEqual(len(warp_rules), 1)
        self.assertIn("domain:openai.com", warp_rules[0]["domain"])

        # بررسی رول بلاک اسپم SMTP
        block_rules = [r for r in rules if r.get("outboundTag") == "block" and "port" in r]
        self.assertEqual(len(block_rules), 1)
        self.assertIn("25", block_rules[0]["port"])

    def test_unified_subscription_url_generation(self):
        """بررسی اولویت‌بندی هوشمند تولید لینک سابسکریپشن بر اساس نقش‌های دامنه‌ها"""
        # ۱. تست با دامنه عمومی سیستم
        self.db.set_setting("custom_domain", "portal.mainsite.com")
        url = self.service.get_unified_subscription_url("test-token-1")
        self.assertIn("portal.mainsite.com/sub/test-token-1", url)

        # ۲. تست با ثبت دامنه cdn
        add_cdn = self.db.add_xray_domain(domain="cdn.subnode.com", role="cdn", port=443)
        cdn_id = add_cdn.get("id")
        url_cdn = self.service.get_unified_subscription_url("test-token-2")
        self.assertIn("cdn.subnode.com/sub/test-token-2", url_cdn)

        # ۳. تست با ثبت دامنه sub_only (اولویت بالاتر از cdn)
        add_sub = self.db.add_xray_domain(domain="sub.onlydomain.com", role="sub_only", port=443)
        sub_id = add_sub.get("id")
        url_sub = self.service.get_unified_subscription_url("test-token-3")
        self.assertIn("sub.onlydomain.com/sub/test-token-3", url_sub)

        # پاکسازی دامنه‌ها
        if sub_id:
            self.db.delete_xray_domain(sub_id)
        if cdn_id:
            self.db.delete_xray_domain(cdn_id)

    def test_parse_config_details(self):
        """بررسی تجزیه دقیق متادیتا و متغیرهای بصری کانفیگ‌های تولیدشده"""
        vless_reality = "vless://user1@direct.server.com:443?security=reality&sni=yahoo.com#VPN ⚡ Reality Direct"
        p_vr = self.service.parse_config_details(vless_reality)
        self.assertEqual(p_vr["protocol"], "VLESS")
        self.assertEqual(p_vr["transport"], "Reality Direct")
        self.assertEqual(p_vr["badge_color"], "success")
        self.assertEqual(p_vr["name"], "VPN ⚡ Reality Direct")

        vless_ws = "vless://user1@cdn.server.com:443?security=tls&type=ws&path=/tgbot-ws#VPN 🌐 Cloud CDN VLESS-WS"
        p_ws = self.service.parse_config_details(vless_ws)
        self.assertEqual(p_ws["protocol"], "VLESS")
        self.assertEqual(p_ws["transport"], "CDN WebSocket")
        self.assertEqual(p_ws["badge_color"], "info")

        trojan_ws = "trojan://user1@cdn.server.com:443?security=tls&type=ws&path=/tgbot-ws#VPN 🛡️ Trojan-WS"
        p_tr = self.service.parse_config_details(trojan_ws)
        self.assertEqual(p_tr["protocol"], "Trojan")
        self.assertEqual(p_tr["badge_color"], "warning")

        ss_aead = "ss://YWVzLTI1Ni1nY206cGFzc3dvcmQ=@ss.server.com:1080#VPN ⚡ Shadowsocks 2022"
        p_ss = self.service.parse_config_details(ss_aead)
        self.assertEqual(p_ss["protocol"], "Shadowsocks")
        self.assertEqual(p_ss["transport"], "2022 AEAD")
        self.assertEqual(p_ss["badge_color"], "danger")

    def test_smart_subscription_browser_portal_delivery(self):
        """تست جامع تفکیک هوشمند مرورگر وب (پرتال بنتو) از کلاینت‌های VPN (سابسکریپشن Base64)"""
        conn = self.db.get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO subscriptions 
            (id, hidify_uuid, telegram_id, plan_id, plan_name, account_name, data_limit, data_used, duration, status, is_deleted)
            VALUES (88889, 'uuid-portal-delivery-test', 0, 'plan_vip', 'بسته اختصاصی', 'DeliveryUser', 80.0, 10.0, 30, 'active', 0)
        """)
        conn.commit()
        conn.close()

        try:
            self.db.set_setting("xray_core_enabled", "1")
            self.db.set_setting("xray_matrix_direct_reality_tcp", "1")

            with self.client as client:
                # الف) درخواست مرورگر وب: باید پرتال بنتو با استاتوس 200 و فرمت HTML رندر شود
                res_browser = client.get(
                    "/sub/uuid-portal-delivery-test",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                    }
                )
                self.assertEqual(res_browser.status_code, 200)
                html_body = res_browser.data.decode("utf-8")
                self.assertIn("subConfigModal", html_body)
                self.assertIn("DeliveryUser", html_body)
                self.assertIn("tab-xray-pane", html_body)

                # ب) درخواست کلاینت VPN (مثلاً Streisand / Happ / v2rayNG): باید Base64 کانفیگ‌ها برگردد
                res_vpn = client.get(
                    "/sub/uuid-portal-delivery-test",
                    headers={"User-Agent": "Streisand/1.5.0"}
                )
                self.assertEqual(res_vpn.status_code, 200)
                self.assertIn("Subscription-Userinfo", res_vpn.headers)
                userinfo_val = res_vpn.headers["Subscription-Userinfo"]
                self.assertIn("expire=", userinfo_val)
                exp_ts_val = int(userinfo_val.split("expire=")[1].split(";")[0].strip())
                self.assertGreater(exp_ts_val, 0)
                decoded_configs = base64.b64decode(res_vpn.data).decode("utf-8")
                self.assertIn("vless://", decoded_configs)
                self.assertIn("DeliveryUser", decoded_configs)
        finally:
            conn = self.db.get_connection()
            conn.execute("DELETE FROM subscriptions WHERE id=88889")
            conn.commit()
            conn.close()

    def test_xray_traffic_worker_lifecycle(self):
        """تست چرخه حیات، شروع و توقف ورکر پس‌زمینه همگام‌سازی ترافیک هسته"""
        status_init = self.service.get_daemon_status()
        self.assertIn("is_running", status_init)
        self.assertIn("interval_seconds", status_init)

        # شروع ورکر
        res_start = self.service.start_traffic_worker(interval_seconds=15)
        self.assertTrue(res_start)
        status_running = self.service.get_daemon_status()
        self.assertTrue(status_running["is_running"])
        self.assertEqual(status_running["interval_seconds"], 15)

        # توقف ورکر
        res_stop = self.service.stop_traffic_worker()
        self.assertTrue(res_stop)
        status_stopped = self.service.get_daemon_status()
        self.assertFalse(status_stopped["is_running"])

    def test_admin_api_xray_install_script_endpoint(self):
        """تست دسترسی و احراز هویت اندپوینت دریافت اسکریپت نصب خودکار اوبونتو"""
        test_token = "secure_test_installer_token_123"
        self.db.set_setting("xray_installer_token", test_token)

        # ۱) دسترسی غیرمجاز بدون توکن و بدون نشست ادمین
        res_unauth = self.client.get("/admin/api/xray/install_script")
        self.assertEqual(res_unauth.status_code, 401)

        # ۲) دسترسی غیرمجاز با توکن نامعتبر
        res_bad_token = self.client.get("/admin/api/xray/install_script?token=invalid_token")
        self.assertEqual(res_bad_token.status_code, 401)

        # ۳) دسترسی مجاز با توکن صحیح
        res_auth_token = self.client.get(f"/admin/api/xray/install_script?token={test_token}")
        self.assertEqual(res_auth_token.status_code, 200)
        self.assertIn("text/plain", res_auth_token.content_type)
        script_text = res_auth_token.data.decode("utf-8")
        self.assertIn("Xray-core", script_text)
        self.assertIn("ufw allow 1080/tcp", script_text)
        self.assertIn("systemctl enable xray", script_text)

        # ۴) دسترسی مجاز از طریق سشن ادمین در مرورگر (بدون ارسال توکن در URL)
        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["role"] = "admin"
            sess["admin_role"] = "super_admin"

        res_auth_sess = self.client.get("/admin/api/xray/install_script")
        self.assertEqual(res_auth_sess.status_code, 200)
        self.assertIn("Xray-core", res_auth_sess.data.decode("utf-8"))

    def test_admin_api_xray_daemon_endpoints(self):
        """تست روت‌های API دریافت وضعیت و کنترل ورکر ترافیک"""
        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["role"] = "admin"
            sess["admin_role"] = "super_admin"

        # وضعیت فعلی ورکر
        res_status = self.client.get("/admin/api/xray/daemon_status")
        self.assertEqual(res_status.status_code, 200)
        json_status = json.loads(res_status.data)
        self.assertTrue(json_status["success"])
        self.assertIn("is_running", json_status["status"])

        # تغییر وضعیت ورکر (فعال‌سازی)
        res_toggle_on = self.client.post("/admin/api/xray/toggle_daemon", json={"enable": True, "interval": 45})
        self.assertEqual(res_toggle_on.status_code, 200)
        json_on = json.loads(res_toggle_on.data)
        self.assertTrue(json_on["success"])
        self.assertTrue(json_on["status"]["is_running"])
        self.assertEqual(json_on["status"]["interval_seconds"], 45)

        # تغییر وضعیت ورکر (توقف)
        res_toggle_off = self.client.post("/admin/api/xray/toggle_daemon", json={"enable": False})
        self.assertEqual(res_toggle_off.status_code, 200)
        json_off = json.loads(res_toggle_off.data)
        self.assertTrue(json_off["success"])
        self.assertFalse(json_off["status"]["is_running"])

    def test_reality_keypair_mathematical_correction(self):
        """بررسی تصحیح خودکار کلید عمومی در صورت مغایرت ریاضیاتی با کلید خصوصی"""
        from cryptography.hazmat.primitives.asymmetric import x25519
        priv = x25519.X25519PrivateKey.generate()
        real_pub = base64.urlsafe_b64encode(priv.public_key().public_bytes_raw()).decode("utf-8").rstrip("=")
        priv_b64 = base64.urlsafe_b64encode(priv.private_bytes_raw()).decode("utf-8").rstrip("=")

        # ذخیره کلید خصوصی سالم ولی کلید عمومی متناقض و ساختگی
        self.db.set_setting("xray_reality_private_key", priv_b64)
        self.db.set_setting("xray_reality_public_key", "mismatched_public_key_abcdef1234567890")
        self.db.set_setting("xray_reality_short_id", "12345678")

        creds = self.service.ensure_reality_credentials()
        self.assertEqual(creds["private_key"], priv_b64)
        self.assertEqual(creds["public_key"], real_pub)
        self.assertEqual(self.db.get_setting("xray_reality_public_key"), real_pub)

    def test_node_config_auto_registration(self):
        """بررسی ثبت خودکار آی‌پی نود و دامنه direct هنگام درخواست پیکربندی توسط اوبونتو"""
        self.db.set_setting("xray_installer_token", "test_auto_token_999")
        orig_ip = self.db.get_setting("xray_server_ip")
        self.db.set_setting("xray_server_ip", "")

        try:
            res = self.client.get("/admin/api/xray/node_config?token=test_auto_token_999&node_ip=198.51.100.77")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(self.db.get_setting("xray_server_ip"), "198.51.100.77")

            domains = self.db.get_xray_domains()
            matching = [d for d in domains if d.get("domain") == "198.51.100.77" and d.get("role") == "direct"]
            self.assertGreaterEqual(len(matching), 1)
        finally:
            self.db.set_setting("xray_server_ip", orig_ip or "")
            conn = self.db.get_connection()
            conn.execute("DELETE FROM xray_domains WHERE domain = '198.51.100.77'")
            conn.commit()
            conn.close()


if __name__ == "__main__":
    unittest.main()


