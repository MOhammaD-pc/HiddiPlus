#!/usr/bin/env python3
"""
ابزار خط فرمانی مدیریت و بازیابی پین‌کد ترمینال و ربات مدیریت
CLI tool to view, set, or reset the Terminal and Admin Bot PIN
"""

import sys
import os

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from utils import to_english_digits

def show_pin():
    raw_pin = db.get_setting("terminal_pin")
    pin = to_english_digits(str(raw_pin or "").strip())
    if pin:
        print("==================================================")
        print(f"🔑 پین‌کد فعلی ترمینال و ربات مدیریت: [ {pin} ]")
        print(f"Current PIN: {pin}")
        print("==================================================")
    else:
        print("==================================================")
        print("⚠️ پین‌کدی برای سیستم تنظیم نشده است (خالی).")
        print("No PIN is currently configured.")
        print("==================================================")

def set_pin(new_pin: str):
    clean_pin = to_english_digits(str(new_pin).strip())
    if not clean_pin or len(clean_pin) < 4:
        print("❌ خطا: پین‌کد باید حداقل ۴ رقم/کاراکتر باشد.")
        print("Error: PIN must be at least 4 characters/digits.")
        sys.exit(1)
    
    db.set_setting("terminal_pin", clean_pin)
    print("==================================================")
    print(f"✅ پین‌کد جدید با موفقیت تنظیم شد: [ {clean_pin} ]")
    print(f"PIN successfully updated to: {clean_pin}")
    print("این پین در خط فرمان پنل وب و ربات تلگرام اعمال شد.")
    print("==================================================")

def reset_pin():
    db.set_setting("terminal_pin", "")
    print("==================================================")
    print("✅ پین‌کد حذف شد. اکنون بدون پین است.")
    print("PIN has been cleared/reset.")
    print("==================================================")

def main():
    if len(sys.argv) < 2:
        print("\n🔧 ابزار مدیریت پین‌کد ترمینال و ربات مدیریت (TGBot PIN Manager)")
        show_pin()
        print("\nدستورات قابل استفاده (Usage):")
        print("  python manage_pin.py show          -> نمایش پین فعلی")
        print("  python manage_pin.py set <new_pin>  -> تنظیم پین جدید (مثال: python manage_pin.py set 1234)")
        print("  python manage_pin.py reset         -> حذف پین فعلی\n")
        return

    cmd = sys.argv[1].lower().strip()
    if cmd in ("show", "get", "status"):
        show_pin()
    elif cmd in ("set", "change", "update"):
        if len(sys.argv) < 3:
            print("❌ لطفاً پین جدید را مشخص کنید. مثال:")
            print("python manage_pin.py set 1234")
            sys.exit(1)
        set_pin(sys.argv[2])
    elif cmd in ("reset", "clear", "delete", "remove"):
        reset_pin()
    else:
        # If user passed a PIN directly like `python manage_pin.py 1234`
        clean = to_english_digits(str(cmd).strip())
        if len(clean) >= 4:
            set_pin(clean)
        else:
            print(f"❌ دستور نامعتبر: {cmd}")
            print("دستورات مجاز: show, set <pin>, reset")

if __name__ == "__main__":
    main()
