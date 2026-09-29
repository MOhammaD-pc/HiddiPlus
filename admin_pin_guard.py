#!/usr/bin/env python3
"""
ماژول احراز هویت امنیتی پنل مدیریت تلگرام با پین‌کد و کیبورد شیشه‌ای (Admin PIN Guard)
پین‌کد این بخش دقیقاً همان terminal_pin ذخیره شده در دیتابیس است.
"""

import time
import logging
from typing import Optional, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database import db
from utils import to_english_digits

logger = logging.getLogger("admin_pin_guard")

# مدت زمان اعتبار سشن مدیریت پس از تایید پین (۱۲ ساعت)
ADMIN_SESSION_LIFETIME = 12 * 3600  # 12 hours
MAX_PIN_FAILS = 5
BLOCK_DURATION_SECONDS = 300  # 5 minutes


def is_admin_session_unlocked(context: ContextTypes.DEFAULT_TYPE) -> bool:
    """بررسی اینکه آیا سشن ادمین در حال حاضر آنلاک و معتبر است یا خیر"""
    if not context or not hasattr(context, "user_data") or context.user_data is None:
        return False
        
    unlocked = context.user_data.get("admin_session_unlocked", False)
    unlocked_at = context.user_data.get("admin_session_unlocked_at", 0)
    
    if unlocked and (time.time() - unlocked_at < ADMIN_SESSION_LIFETIME):
        return True
    
    # اگر منقضی شده بود، ریست شود
    if unlocked:
        context.user_data["admin_session_unlocked"] = False
        context.user_data.pop("admin_session_unlocked_at", None)
    return False


def lock_admin_session(context: ContextTypes.DEFAULT_TYPE):
    """قفل کردن فوری سشن مدیریت"""
    if context and hasattr(context, "user_data") and context.user_data is not None:
        context.user_data["admin_session_unlocked"] = False
        context.user_data.pop("admin_session_unlocked_at", None)
        context.user_data.pop("admin_pin_buffer", None)


def get_pin_keypad_markup() -> InlineKeyboardMarkup:
    """ساخت صفحه کلید شیشه‌ای ارقام برای ورود پین‌کد"""
    keyboard = [
        [
            InlineKeyboardButton("1️⃣", callback_data="adm_pin_1"),
            InlineKeyboardButton("2️⃣", callback_data="adm_pin_2"),
            InlineKeyboardButton("3️⃣", callback_data="adm_pin_3"),
        ],
        [
            InlineKeyboardButton("4️⃣", callback_data="adm_pin_4"),
            InlineKeyboardButton("5️⃣", callback_data="adm_pin_5"),
            InlineKeyboardButton("6️⃣", callback_data="adm_pin_6"),
        ],
        [
            InlineKeyboardButton("7️⃣", callback_data="adm_pin_7"),
            InlineKeyboardButton("8️⃣", callback_data="adm_pin_8"),
            InlineKeyboardButton("9️⃣", callback_data="adm_pin_9"),
        ],
        [
            InlineKeyboardButton("⌫ حذف", callback_data="adm_pin_back"),
            InlineKeyboardButton("0️⃣", callback_data="adm_pin_0"),
            InlineKeyboardButton("✅ ورود", callback_data="adm_pin_submit"),
        ],
        [
            InlineKeyboardButton("❌ انصراف", callback_data="adm_pin_cancel"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def build_pin_prompt_text(buffer: str = "", error_text: Optional[str] = None) -> str:
    """تولید متن پیام درخواست پین همراه با نقاط ورودی"""
    raw_saved = db.get_setting("terminal_pin")
    saved_pin = to_english_digits(str(raw_saved or "").strip())
    expected_len = len(saved_pin) if saved_pin else 4
    
    buf_len = len(buffer)
    # ساخت نقاط ورودی به سبک برنامه‌های بانکی
    dots = []
    total_dots = max(expected_len, buf_len)
    for i in range(total_dots):
        if i < buf_len:
            dots.append("●")
        else:
            dots.append("○")
    display_dots = " ".join(dots)
    
    text = (
        "🔐 **احراز هویت مدیریت سامانه**\n\n"
        "جهت دسترسی به پنل مدیریت، لطفاً پین‌کد امنیتی (پین خط فرمان) را با کلیدهای شیشه‌ای زیر وارد نمایید:\n\n"
        f"ورودی:  `{display_dots}`"
    )
    
    if error_text:
        text += f"\n\n⚠️ **{error_text}**"
        
    return text


async def show_admin_pin_prompt(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE, 
    error_text: Optional[str] = None
) -> int:
    """نمایش یا ویرایش پیام درخواست پین‌کد با صفحه کلید شیشه‌ای"""
    from bot import ADMIN_MENU, CHOOSING

    # بررسی بلاک بودن موقت به دلیل ۵ بار اشتباه
    blocked_until = context.user_data.get("admin_pin_blocked_until", 0)
    now = time.time()
    if now < blocked_until:
        rem_seconds = int(blocked_until - now)
        rem_minutes = max(1, rem_seconds // 60)
        msg_text = (
            f"⛔ **دسترسی موقتاً مسدود است!**\n\n"
            f"به دلیل ۵ بار تلاش ناموفق، ورود به پنل مدیریت به مدت {rem_minutes} دقیقه مسدود شده است.\n"
            f"لطفاً پس از اتمام زمان، مجدداً امتحان فرمایید."
        )
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_menu")]])
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(msg_text, reply_markup=markup, parse_mode="Markdown")
            except Exception:
                await update.callback_query.message.reply_text(msg_text, reply_markup=markup, parse_mode="Markdown")
        elif update.message:
            await update.message.reply_text(msg_text, reply_markup=markup, parse_mode="Markdown")
        return CHOOSING

    if error_text is None:
        context.user_data["admin_pin_buffer"] = ""

    buffer = context.user_data.get("admin_pin_buffer", "")
    text = build_pin_prompt_text(buffer, error_text)
    markup = get_pin_keypad_markup()

    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            if "not modified" not in str(e).lower():
                await update.callback_query.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")

    return ADMIN_MENU


async def handle_admin_pin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """پردازش کلیک روی دکمه‌های شیشه‌ای پین‌کد ادمین"""
    from bot import admin_panel, ADMIN_MENU, CHOOSING

    query = update.callback_query
    data = query.data
    
    # قفل پنل مدیریت
    if data == "adm_lock_panel":
        lock_admin_session(context)
        await query.answer("🔒 پنل مدیریت قفل شد.", show_alert=True)
        await query.edit_message_text(
            "🔒 **پنل مدیریت قفل شد.**\nجهت ورود مجدد باید پین‌کد امنیتی را وارد نمایید.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 ورود به پنل مدیریت", callback_data="adm_adv_menu")]])
        )
        return CHOOSING

    # انصراف
    if data == "adm_pin_cancel":
        context.user_data.pop("admin_pin_buffer", None)
        await query.answer("انصراف داده شد.")
        try:
            await query.edit_message_text("❌ ورود به پنل مدیریت لغو شد.")
        except Exception:
            pass
        return CHOOSING

    # بررسی بلاک بودن
    blocked_until = context.user_data.get("admin_pin_blocked_until", 0)
    now = time.time()
    if now < blocked_until:
        rem_sec = int(blocked_until - now)
        await query.answer(f"⛔ ورود به دلیل خطاهای مکرر تا {rem_sec} ثانیه دیگر مسدود است.", show_alert=True)
        return ADMIN_MENU

    buffer = context.user_data.get("admin_pin_buffer", "")
    raw_saved = db.get_setting("terminal_pin")
    saved_pin = to_english_digits(str(raw_saved or "").strip())

    # حذف آخرین رقم
    if data == "adm_pin_back":
        if buffer:
            buffer = buffer[:-1]
            context.user_data["admin_pin_buffer"] = buffer
        await query.answer()
        return await show_admin_pin_prompt(update, context)

    # فشردن رقم ۰ تا ۹
    if data.startswith("adm_pin_") and data[8:].isdigit():
        digit = data[8:]
        buffer += digit
        context.user_data["admin_pin_buffer"] = buffer

    # اگر طول پین به طول پین ذخیره‌شده رسید یا دکمه تایید زده شد
    should_verify = (data == "adm_pin_submit") or (saved_pin and len(buffer) >= len(saved_pin))

    if should_verify:
        if saved_pin and buffer == saved_pin:
            # تایید موفقیت‌آمیز
            context.user_data["admin_session_unlocked"] = True
            context.user_data["admin_session_unlocked_at"] = time.time()
            context.user_data.pop("admin_pin_buffer", None)
            context.user_data["admin_pin_fails"] = 0
            context.user_data.pop("admin_pin_blocked_until", None)
            await query.answer("✅ هویت شما تایید شد. خوش آمدید!", show_alert=False)
            
            # باز کردن مستقیم پنل ادمین
            return await admin_panel(update, context)
        else:
            # پین اشتباه
            fails = context.user_data.get("admin_pin_fails", 0) + 1
            context.user_data["admin_pin_fails"] = fails
            context.user_data["admin_pin_buffer"] = ""
            
            if fails >= MAX_PIN_FAILS:
                context.user_data["admin_pin_blocked_until"] = time.time() + BLOCK_DURATION_SECONDS
                await query.answer("⛔ ۵ بار اشتباه! ورود به مدت ۵ دقیقه مسدود شد.", show_alert=True)
                await query.edit_message_text(
                    "⛔ **دسترسی مسدود شد!**\nبه دلیل ۵ بار ورود پین‌کد اشتباه، ورود به پنل به مدت ۵ دقیقه مسدود گردید.",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 تلاش مجدد", callback_data="adm_adv_menu")]])
                )
                return CHOOSING
            else:
                rem_tries = MAX_PIN_FAILS - fails
                await query.answer(f"❌ پین‌کد اشتباه است! ({rem_tries} تلاش باقی‌مانده)", show_alert=True)
                return await show_admin_pin_prompt(
                    update, context, 
                    error_text=f"پین‌کد اشتباه است! ({rem_tries} تلاش باقی‌مانده)"
                )

    # در صورتی که هنوز به طول کامل نرسیده، آپدیت نمایشگر نقاط
    await query.answer()
    return await show_admin_pin_prompt(update, context)
