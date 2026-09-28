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


if __name__ == "__main__":
    unittest.main()
