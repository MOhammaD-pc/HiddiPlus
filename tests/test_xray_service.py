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


if __name__ == "__main__":
    unittest.main()


