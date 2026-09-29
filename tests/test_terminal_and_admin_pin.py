#!/usr/bin/env python3
"""
تست جامع عملکرد پین‌کد ترمینال، ابزار مدیریت پین و گارد امنیتی ربات مدیریت
"""

import unittest
import time
from database import db
from utils import to_english_digits
from admin_pin_guard import (
    is_admin_session_unlocked,
    lock_admin_session,
    build_pin_prompt_text,
    get_pin_keypad_markup,
    ADMIN_SESSION_LIFETIME,
    MAX_PIN_FAILS,
)

class MockContext:
    def __init__(self):
        self.user_data = {}

class TestTerminalAndAdminPIN(unittest.TestCase):
    def setUp(self):
        # ذخیره پین قبلی جهت بازگردانی پس از تست
        self.original_pin = db.get_setting("terminal_pin")

    def tearDown(self):
        # بازگردانی پین
        db.set_setting("terminal_pin", self.original_pin or "")

    def test_pin_normalization(self):
        """تست تبدیل ارقام فارسی و عربی به انگلیسی"""
        persian_pin = "۱۲۳۴"
        arabic_pin = "١٢٣٤"
        english_pin = "1234"
        
        self.assertEqual(to_english_digits(persian_pin), "1234")
        self.assertEqual(to_english_digits(arabic_pin), "1234")
        self.assertEqual(to_english_digits(english_pin), "1234")

    def test_database_integer_handling(self):
        """تست اطمینان از برابری حتی در صورتی که دیتابیس عدد صحیح بازگرداند"""
        db.set_setting("terminal_pin", "9876")
        raw = db.get_setting("terminal_pin")
        
        # ممکن است json.loads آن را int کند یا str بماند
        saved_str = to_english_digits(str(raw or "").strip())
        input_persian = to_english_digits(str("۹۸۷۶").strip())
        
        self.assertEqual(saved_str, "9876")
        self.assertEqual(input_persian, saved_str)

    def test_admin_pin_guard_session(self):
        """تست آنلاک بودن و قفل شدن سشن مدیریت"""
        ctx = MockContext()
        
        # در ابتدا سشن قفل است
        self.assertFalse(is_admin_session_unlocked(ctx))
        
        # پس از ورود صحیح
        ctx.user_data["admin_session_unlocked"] = True
        ctx.user_data["admin_session_unlocked_at"] = time.time()
        self.assertTrue(is_admin_session_unlocked(ctx))
        
        # قفل کردن دستی
        lock_admin_session(ctx)
        self.assertFalse(is_admin_session_unlocked(ctx))

    def test_admin_pin_guard_prompt_dots(self):
        """تست نمایش نقاط ورودی پین کد (Masking dots)"""
        db.set_setting("terminal_pin", "1234")
        
        # ورودی خالی
        prompt_empty = build_pin_prompt_text("")
        self.assertIn("○ ○ ○ ○", prompt_empty)
        
        # دو رقم وارد شده
        prompt_two = build_pin_prompt_text("12")
        self.assertIn("● ● ○ ○", prompt_two)
        
        # چهار رقم کامل
        prompt_full = build_pin_prompt_text("1234")
        self.assertIn("● ● ● ●", prompt_full)

    def test_keypad_markup_buttons(self):
        """تست دکمه‌های کیبورد شیشه‌ای"""
        markup = get_pin_keypad_markup()
        # باید حداقل ۵ سطر دکمه داشته باشد (۳ سطر ارقام، ۱ سطر حذف/۰/تایید، ۱ سطر انصراف)
        self.assertEqual(len(markup.inline_keyboard), 5)
        # سطر اول باید ۱ و ۲ و ۳ باشد
        self.assertEqual(markup.inline_keyboard[0][0].callback_data, "adm_pin_1")
        self.assertEqual(markup.inline_keyboard[0][1].callback_data, "adm_pin_2")
        self.assertEqual(markup.inline_keyboard[0][2].callback_data, "adm_pin_3")
        # سطر آخر انصراف
        self.assertEqual(markup.inline_keyboard[4][0].callback_data, "adm_pin_cancel")

if __name__ == "__main__":
    unittest.main()
