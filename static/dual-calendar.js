/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  تقویم پیشرفته دوگانه شمسی و میلادی (Dual Shamsi & Gregorian Calendar)
 * ═══════════════════════════════════════════════════════════════════════════
 *  - تقویم اصلی: هجری شمسی (اعداد فارسی بزرگ، پررنگ و برجسته)
 *  - تقویم فرعی: میلادی (اعداد کوچک و ریز در زیر هر روز)
 *  - ناوبری کامل: سلکتورهای ماه و سال، دکمه‌های ماه قبل و بعد، نشانگر بازه میلادی
 *  - کلیدهای میانبر سریع (امروز، فردا، ۳ روز بعد، ۱ هفته بعد، ۱ ماه بعد، پایان ماه)
 *  - انتخاب‌گر زمان (ساعت و دقیقه با پیش‌تنظیم‌های ۰۰:۰۰، ۱۲:۰۰، ۱۸:۰۰، ۲۳:۵۹) در حالت datetime
 *  - خلاصه زنده و شمارش معکوس زمان باقی‌مانده
 *  - سازگار با حالت روشن و تیره (Light / Dark mode)
 *  - هماهنگی کامل دوطرفه با فیلدهای فرم و مقادیر استاندارد ISO (YYYY-MM-DD و YYYY-MM-DDTHH:MM)
 */

(function(global) {
    'use strict';

    // ─── جدول روزهای ماه‌ها ──────────────────────────────────────────────
    const G_DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    const J_DAYS_IN_MONTH = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29];

    const SHAMSI_MONTHS = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ];
    const GREGORIAN_MONTHS = [
        'ژانویه', 'فوریه', 'مارس', 'آوریل', 'مه', 'ژوئن',
        'ژوئیه', 'اوت', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر'
    ];
    const GREGORIAN_MONTHS_SHORT = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    const SHAMSI_WEEK_DAYS = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'];
    const GREGORIAN_WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // ─── توابع تبدیل دقیق (مطابق ۱۰۰٪ با پایتون jdatetime) ─────────────
    function gregorianToJalali(gyear, gmonth, gday) {
        const gy = gyear - 1600;
        const gm = gmonth - 1;
        let j_day_no = 365 * gy + Math.floor((gy + 3) / 4) - Math.floor((gy + 99) / 100) + Math.floor((gy + 399) / 400) + gday - 1 - 79;
        for (let i = 0; i < gm; i++) {
            j_day_no += G_DAYS_IN_MONTH[i];
        }
        if (gm > 1 && ((gy % 4 === 0 && gy % 100 !== 0) || (gy % 400 === 0))) {
            j_day_no += 1;
        }
        const j_np = Math.floor(j_day_no / 12053);
        j_day_no %= 12053;
        let jy = 979 + 33 * j_np + 4 * Math.floor(j_day_no / 1461);
        j_day_no %= 1461;
        if (j_day_no >= 366) {
            j_day_no -= 1;
            jy += Math.floor(j_day_no / 365);
            j_day_no %= 365;
        }
        let i = 0;
        for (i = 0; i < 11; i++) {
            if (j_day_no < J_DAYS_IN_MONTH[i]) {
                break;
            }
            j_day_no -= J_DAYS_IN_MONTH[i];
        }
        return { jy, jm: i + 1, jd: j_day_no + 1 };
    }

    function jalaliToGregorian(jyear, jmonth, jday) {
        const jy = jyear - 979;
        let g_day_no = 365 * jy + Math.floor(jy / 33) * 8 + Math.floor((jy % 33 + 3) / 4) + jday - 1 + 79;
        for (let i = 0; i < jmonth - 1; i++) {
            g_day_no += J_DAYS_IN_MONTH[i];
        }
        let gy = 1600 + 400 * Math.floor(g_day_no / 146097);
        g_day_no %= 146097;
        let leap = 1;
        if (g_day_no >= 36525) {
            g_day_no -= 1;
            gy += 100 * Math.floor(g_day_no / 36524);
            g_day_no %= 36524;
            if (g_day_no >= 365) {
                g_day_no += 1;
            } else {
                leap = 0;
            }
        }
        gy += 4 * Math.floor(g_day_no / 1461);
        g_day_no %= 1461;
        if (g_day_no >= 366) {
            leap = 0;
            g_day_no -= 1;
            gy += Math.floor(g_day_no / 365);
            g_day_no %= 365;
        }
        let i = 0;
        while (g_day_no >= G_DAYS_IN_MONTH[i] + (i === 1 && leap ? 1 : 0)) {
            g_day_no -= G_DAYS_IN_MONTH[i] + (i === 1 && leap ? 1 : 0);
            i++;
        }
        return { gy, gm: i + 1, gd: g_day_no + 1 };
    }

    function isJalaliLeapYear(jy) {
        return [1, 5, 9, 13, 17, 22, 26, 30].includes(jy % 33);
    }

    function getDaysInJalaliMonth(jy, jm) {
        if (jm <= 6) return 31;
        if (jm <= 11) return 30;
        return isJalaliLeapYear(jy) ? 30 : 29;
    }

    function toPersianDigits(n) {
        if (n === null || n === undefined) return '';
        const fa = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
        return String(n).replace(/[0-9]/g, w => fa[+w]);
    }

    function parseIsoString(str) {
        if (!str || typeof str !== 'string') return null;
        const s = str.trim();
        // فرمت YYYY-MM-DD یا YYYY-MM-DDTHH:MM یا YYYY-MM-DD HH:MM
        const m = s.match(/^(\d{4})-(\d{2})-(\d{2})(?:[T\s](\d{2}):(\d{2})(?::(\d{2}))?)?/);
        if (!m) return null;
        return {
            gy: parseInt(m[1], 10),
            gm: parseInt(m[2], 10),
            gd: parseInt(m[3], 10),
            hour: m[4] !== undefined ? parseInt(m[4], 10) : 0,
            minute: m[5] !== undefined ? parseInt(m[5], 10) : 0
        };
    }

    let instanceCounter = 0;

    // ─── کلاس تقویم دوگانه (DualDatePicker) ──────────────────────────────
    class DualDatePicker {
        constructor(inputEl, options = {}) {
            if (typeof inputEl === 'string') {
                inputEl = document.querySelector(inputEl);
            }
            if (!inputEl) {
                throw new Error('DualDatePicker: Target input element not found.');
            }

            this.input = inputEl;
            this.input.__dualDatePicker = this;
            this.id = 'dualPicker_' + (++instanceCounter);

            // گزینه‌ها
            this.mode = options.mode || (inputEl.type === 'datetime-local' ? 'datetime' : (inputEl.dataset.dualPicker || 'date'));
            this.inline = options.inline || false;
            this.placeholder = options.placeholder || (this.mode === 'datetime' ? 'انتخاب تاریخ و ساعت (شمسی / میلادی)...' : 'انتخاب تاریخ (شمسی / میلادی)...');
            this.allowClear = options.allowClear !== undefined ? options.allowClear : !inputEl.required;
            this.minYear = options.minYear || 1400;
            this.maxYear = options.maxYear || 1410;
            this.onChange = options.onChange || null;

            // وضعیت جاری
            const now = new Date();
            const todayJ = gregorianToJalali(now.getFullYear(), now.getMonth() + 1, now.getDate());
            this.todayJ = todayJ;

            this.selectedJy = null;
            this.selectedJm = null;
            this.selectedJd = null;
            this.selectedHour = 12;
            this.selectedMinute = 0;

            this.viewJy = todayJ.jy;
            this.viewJm = todayJ.jm;
            this.isOpen = false;

            this.buildDOM();
            this.readInitialValue();
            this.bindEvents();
            this.render();
        }

        buildDOM() {
            // پنهان کردن اینپوت اصلی با حفظ نام و مقدار آن
            this.input.style.display = 'none';

            // ایجاد محفظه اصلی
            this.container = document.createElement('div');
            this.container.className = 'dual-picker-wrapper' + (this.inline ? ' is-inline' : '');
            this.container.id = this.id;

            // باکس تریگر (نمایشگر دکمه‌ای)
            this.triggerBox = document.createElement('div');
            this.triggerBox.className = 'dual-picker-trigger form-control d-flex align-items-center justify-content-between cursor-pointer';
            this.triggerBox.setAttribute('role', 'button');
            this.triggerBox.setAttribute('tabindex', '0');

            // پنل تقویم (بازشونده یا اینلاین)
            this.panel = document.createElement('div');
            this.panel.className = 'dual-picker-panel' + (this.inline ? ' is-inline-panel' : ' d-none');

            this.panel.innerHTML = `
                <!-- هدر ناوبری -->
                <div class="dual-picker-header p-2.5 border-bottom d-flex align-items-center justify-content-between gap-2 flex-wrap">
                    <div class="d-flex align-items-center gap-1.5 flex-grow-1">
                        <select class="form-select form-select-sm fw-bold dual-month-select" style="min-width: 115px;"></select>
                        <select class="form-select form-select-sm fw-bold dual-year-select font-monospace" style="min-width: 95px;"></select>
                    </div>
                    <div class="d-flex align-items-center gap-1">
                        <button type="button" class="btn btn-sm btn-outline-secondary py-1 px-2.5 dual-btn-next" title="ماه بعد">
                            <i class="fas fa-chevron-right"></i>
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-primary py-1 px-2.5 dual-btn-today" title="برو به امروز">
                            امروز
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-secondary py-1 px-2.5 dual-btn-prev" title="ماه قبل">
                            <i class="fas fa-chevron-left"></i>
                        </button>
                    </div>
                </div>

                <!-- نشانگر بازه معادل میلادی این ماه شمسی -->
                <div class="px-3 py-1.5 bg-light-subtle border-bottom d-flex align-items-center justify-content-between small">
                    <div class="dual-gregorian-range-badge text-muted" style="font-size: 0.76rem;"></div>
                    <div class="text-secondary" style="font-size: 0.72rem;">تقویم خورشیدی / میلادی</div>
                </div>

                <!-- میانبرهای زمانی سریع -->
                <div class="px-2.5 py-1.5 border-bottom d-flex align-items-center gap-1 flex-wrap bg-light-subtle">
                    <button type="button" class="btn btn-xs btn-outline-secondary dual-preset-btn" data-days="0">امروز</button>
                    <button type="button" class="btn btn-xs btn-outline-secondary dual-preset-btn" data-days="1">فردا</button>
                    <button type="button" class="btn btn-xs btn-outline-secondary dual-preset-btn" data-days="3">۳ روز بعد</button>
                    <button type="button" class="btn btn-xs btn-outline-secondary dual-preset-btn" data-days="7">۱ هفته بعد</button>
                    <button type="button" class="btn btn-xs btn-outline-secondary dual-preset-btn" data-days="30">۱ ماه بعد</button>
                    <button type="button" class="btn btn-xs btn-outline-secondary dual-preset-month-end">پایان ماه</button>
                </div>

                <!-- روزهای هفته -->
                <div class="dual-calendar-weekdays px-2 pt-2 pb-1 text-muted">
                    <div class="weekday-cell fw-bold">ش</div>
                    <div class="weekday-cell fw-bold">ی</div>
                    <div class="weekday-cell fw-bold">د</div>
                    <div class="weekday-cell fw-bold">س</div>
                    <div class="weekday-cell fw-bold">چ</div>
                    <div class="weekday-cell fw-bold">پ</div>
                    <div class="weekday-cell fw-bold text-danger">ج</div>
                </div>

                <!-- شبکه روزهای ماه -->
                <div class="dual-calendar-grid px-2 pb-2"></div>

                <!-- بخش ساعت و دقیقه (ویژه datetime) -->
                ${this.mode === 'datetime' ? `
                <div class="dual-time-section p-2.5 border-top bg-light-subtle">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                        <span class="small fw-bold text-secondary">
                            <i class="fas fa-clock text-primary me-1"></i>تنظیم دقیق ساعت و دقیقه:
                        </span>
                        <div class="d-flex align-items-center gap-1">
                            <button type="button" class="btn btn-xs btn-outline-secondary dual-time-preset" data-time="00:00">۰۰:۰۰</button>
                            <button type="button" class="btn btn-xs btn-outline-secondary dual-time-preset" data-time="12:00">۱۲:۰۰</button>
                            <button type="button" class="btn btn-xs btn-outline-secondary dual-time-preset" data-time="18:00">۱۸:۰۰</button>
                            <button type="button" class="btn btn-xs btn-outline-secondary dual-time-preset" data-time="23:59">۲۳:۵۹</button>
                        </div>
                    </div>
                    <div class="row g-2 align-items-center">
                        <div class="col-6">
                            <div class="input-group input-group-sm">
                                <span class="input-group-text small">ساعت</span>
                                <select class="form-select font-monospace text-center dual-hour-select"></select>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="input-group input-group-sm">
                                <span class="input-group-text small">دقیقه</span>
                                <select class="form-select font-monospace text-center dual-minute-select"></select>
                            </div>
                        </div>
                    </div>
                </div>
                ` : ''}

                <!-- پاورقی خلاصه زنده و دکمه‌های عملیات -->
                <div class="dual-picker-footer p-2.5 border-top d-flex align-items-center justify-content-between gap-2 flex-wrap">
                    <div class="dual-live-summary text-truncate" style="max-width: 65%;">
                        <div class="fw-bold text-primary small dual-summary-shamsi">--</div>
                        <div class="text-muted dual-summary-sub" style="font-size: 0.72rem;">--</div>
                    </div>
                    <div class="d-flex align-items-center gap-1">
                        ${this.allowClear ? `
                        <button type="button" class="btn btn-sm btn-outline-danger py-1 px-2.5 dual-btn-clear" title="پاک کردن تاریخ">
                            پاک کردن
                        </button>
                        ` : ''}
                        ${!this.inline ? `
                        <button type="button" class="btn btn-sm btn-primary py-1 px-3 fw-bold dual-btn-confirm">
                            تایید
                        </button>
                        ` : ''}
                    </div>
                </div>
            `;

            // قرار دادن اجزا در DOM
            this.container.appendChild(this.triggerBox);
            this.container.appendChild(this.panel);
            this.input.parentNode.insertBefore(this.container, this.input.nextSibling);

            // پر کردن سلکتورهای ماه و سال
            this.populateSelects();
        }

        populateSelects() {
            const mSel = this.panel.querySelector('.dual-month-select');
            if (mSel) {
                mSel.innerHTML = '';
                SHAMSI_MONTHS.forEach((name, idx) => {
                    mSel.add(new Option(`${toPersianDigits(idx + 1)}. ${name}`, idx + 1));
                });
            }

            const ySel = this.panel.querySelector('.dual-year-select');
            if (ySel) {
                ySel.innerHTML = '';
                for (let y = this.minYear; y <= this.maxYear; y++) {
                    ySel.add(new Option(`${toPersianDigits(y)} هـ.ش`, y));
                }
            }

            if (this.mode === 'datetime') {
                const hSel = this.panel.querySelector('.dual-hour-select');
                if (hSel) {
                    hSel.innerHTML = '';
                    for (let h = 0; h < 24; h++) {
                        const val = String(h).padStart(2, '0');
                        hSel.add(new Option(`${toPersianDigits(val)} (${val})`, h));
                    }
                }

                const minSel = this.panel.querySelector('.dual-minute-select');
                if (minSel) {
                    minSel.innerHTML = '';
                    for (let m = 0; m < 60; m += 1) {
                        const val = String(m).padStart(2, '0');
                        minSel.add(new Option(`${toPersianDigits(val)} (${val})`, m));
                    }
                }
            }
        }

        readInitialValue() {
            const val = this.input.value;
            if (val) {
                this.setValueFromIso(val, false);
            } else {
                this.updateTriggerBox();
            }
        }

        bindEvents() {
            // کلیک روی تریگر باکس
            if (!this.inline) {
                this.triggerBox.addEventListener('click', (e) => {
                    // اگر کلیک روی دکمه پاک کردن تریگر بود
                    if (e.target.closest('.dual-trigger-clear-btn')) {
                        e.stopPropagation();
                        this.clearValue();
                        return;
                    }
                    this.toggle();
                });

                // کلیک خارج برای بستن
                document.addEventListener('click', (e) => {
                    if (this.isOpen && !this.container.contains(e.target)) {
                        this.close();
                    }
                }, true);
            }

            // تغییر ماه و سال
            const mSel = this.panel.querySelector('.dual-month-select');
            if (mSel) {
                mSel.addEventListener('change', () => {
                    this.viewJm = parseInt(mSel.value, 10);
                    this.renderCalendarGrid();
                });
            }

            const ySel = this.panel.querySelector('.dual-year-select');
            if (ySel) {
                ySel.addEventListener('change', () => {
                    this.viewJy = parseInt(ySel.value, 10);
                    this.renderCalendarGrid();
                });
            }

            // ناوبری ماه قبل و بعد
            const btnPrev = this.panel.querySelector('.dual-btn-prev');
            if (btnPrev) {
                btnPrev.addEventListener('click', () => this.prevMonth());
            }

            const btnNext = this.panel.querySelector('.dual-btn-next');
            if (btnNext) {
                btnNext.addEventListener('click', () => this.nextMonth());
            }

            // رفتن به امروز
            const btnToday = this.panel.querySelector('.dual-btn-today');
            if (btnToday) {
                btnToday.addEventListener('click', () => this.goToToday());
            }

            // دکمه‌های میانبر زمانی سریع
            this.panel.querySelectorAll('.dual-preset-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const days = parseInt(btn.dataset.days, 10);
                    this.addDaysFromToday(days);
                });
            });

            const btnMonthEnd = this.panel.querySelector('.dual-preset-month-end');
            if (btnMonthEnd) {
                btnMonthEnd.addEventListener('click', () => {
                    const daysInMonth = getDaysInJalaliMonth(this.viewJy, this.viewJm);
                    this.selectDay(this.viewJy, this.viewJm, daysInMonth);
                });
            }

            // ساعت و دقیقه
            if (this.mode === 'datetime') {
                const hSel = this.panel.querySelector('.dual-hour-select');
                if (hSel) {
                    hSel.addEventListener('change', () => {
                        this.selectedHour = parseInt(hSel.value, 10);
                        this.syncToInput();
                    });
                }

                const minSel = this.panel.querySelector('.dual-minute-select');
                if (minSel) {
                    minSel.addEventListener('change', () => {
                        this.selectedMinute = parseInt(minSel.value, 10);
                        this.syncToInput();
                    });
                }

                this.panel.querySelectorAll('.dual-time-preset').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const [h, m] = btn.dataset.time.split(':').map(Number);
                        this.selectedHour = h;
                        this.selectedMinute = m;
                        if (hSel) hSel.value = h;
                        if (minSel) minSel.value = m;
                        this.syncToInput();
                    });
                });
            }

            // دکمه پاک کردن
            const btnClear = this.panel.querySelector('.dual-btn-clear');
            if (btnClear) {
                btnClear.addEventListener('click', () => {
                    this.clearValue();
                    if (!this.inline) this.close();
                });
            }

            // دکمه تایید
            const btnConfirm = this.panel.querySelector('.dual-btn-confirm');
            if (btnConfirm) {
                btnConfirm.addEventListener('click', () => this.close());
            }

            // همگام‌سازی با تغییرات خارجی روی input اصلی
            this.input.addEventListener('change', () => {
                if (this.input.value !== this.getCurrentIso()) {
                    this.setValueFromIso(this.input.value, false);
                }
            });
        }

        toggle() {
            if (this.isOpen) {
                this.close();
            } else {
                this.open();
            }
        }

        open() {
            if (this.isOpen || this.inline) return;
            this.isOpen = true;
            this.panel.classList.remove('d-none');
            this.triggerBox.classList.add('is-active');
            this.render();
        }

        close() {
            if (!this.isOpen || this.inline) return;
            this.isOpen = false;
            this.panel.classList.add('d-none');
            this.triggerBox.classList.remove('is-active');
        }

        prevMonth() {
            this.viewJm--;
            if (this.viewJm < 1) {
                this.viewJm = 12;
                this.viewJy--;
            }
            this.renderCalendarGrid();
        }

        nextMonth() {
            this.viewJm++;
            if (this.viewJm > 12) {
                this.viewJm = 1;
                this.viewJy++;
            }
            this.renderCalendarGrid();
        }

        goToToday() {
            const now = new Date();
            const todayJ = gregorianToJalali(now.getFullYear(), now.getMonth() + 1, now.getDate());
            this.viewJy = todayJ.jy;
            this.viewJm = todayJ.jm;
            this.selectDay(todayJ.jy, todayJ.jm, todayJ.jd);
        }

        addDaysFromToday(days) {
            const now = new Date();
            const target = new Date(now.getTime() + days * 24 * 3600 * 1000);
            const targetJ = gregorianToJalali(target.getFullYear(), target.getMonth() + 1, target.getDate());
            this.viewJy = targetJ.jy;
            this.viewJm = targetJ.jm;
            this.selectDay(targetJ.jy, targetJ.jm, targetJ.jd);
        }

        selectDay(jy, jm, jd) {
            this.selectedJy = jy;
            this.selectedJm = jm;
            this.selectedJd = jd;
            this.syncToInput();
            this.renderCalendarGrid();
        }

        setValueFromIso(isoStr, triggerEvents = true) {
            if (!isoStr) {
                this.clearValue(triggerEvents);
                return;
            }
            const p = parseIsoString(isoStr);
            if (!p) return;

            const j = gregorianToJalali(p.gy, p.gm, p.gd);
            this.selectedJy = j.jy;
            this.selectedJm = j.jm;
            this.selectedJd = j.jd;
            this.selectedHour = p.hour;
            this.selectedMinute = p.minute;

            this.viewJy = j.jy;
            this.viewJm = j.jm;

            this.syncToInput(triggerEvents);
            this.render();
        }

        clearValue(triggerEvents = true) {
            this.selectedJy = null;
            this.selectedJm = null;
            this.selectedJd = null;
            this.input.value = '';

            this.updateTriggerBox();
            this.updateSummaryFooter();
            this.renderCalendarGrid();

            if (triggerEvents) {
                this.input.dispatchEvent(new Event('input', { bubbles: true }));
                this.input.dispatchEvent(new Event('change', { bubbles: true }));
                if (typeof this.onChange === 'function') {
                    this.onChange('', null);
                }
            }
        }

        getCurrentIso() {
            if (!this.selectedJy || !this.selectedJm || !this.selectedJd) return '';
            const g = jalaliToGregorian(this.selectedJy, this.selectedJm, this.selectedJd);
            const datePart = `${g.gy}-${String(g.gm).padStart(2, '0')}-${String(g.gd).padStart(2, '0')}`;
            if (this.mode === 'datetime') {
                return `${datePart}T${String(this.selectedHour).padStart(2, '0')}:${String(this.selectedMinute).padStart(2, '0')}`;
            }
            return datePart;
        }

        syncToInput(triggerEvents = true) {
            const iso = this.getCurrentIso();
            this.input.value = iso;
            this.updateTriggerBox();
            this.updateSummaryFooter();

            if (triggerEvents) {
                this.input.dispatchEvent(new Event('input', { bubbles: true }));
                this.input.dispatchEvent(new Event('change', { bubbles: true }));
                if (typeof this.onChange === 'function') {
                    this.onChange(iso, this.getDetails());
                }
            }
        }

        getDetails() {
            if (!this.selectedJy) return null;
            const g = jalaliToGregorian(this.selectedJy, this.selectedJm, this.selectedJd);
            return {
                shamsi: { jy: this.selectedJy, jm: this.selectedJm, jd: this.selectedJd },
                gregorian: { gy: g.gy, gm: g.gm, gd: g.gd },
                time: { hour: this.selectedHour, minute: this.selectedMinute },
                iso: this.getCurrentIso()
            };
        }

        render() {
            const mSel = this.panel.querySelector('.dual-month-select');
            const ySel = this.panel.querySelector('.dual-year-select');
            if (mSel) mSel.value = this.viewJm;
            if (ySel) {
                // اطمینان از وجود سال
                let hasOpt = false;
                for (let i = 0; i < ySel.options.length; i++) {
                    if (parseInt(ySel.options[i].value, 10) === this.viewJy) {
                        hasOpt = true;
                        break;
                    }
                }
                if (!hasOpt) {
                    ySel.add(new Option(`${toPersianDigits(this.viewJy)} هـ.ش`, this.viewJy));
                }
                ySel.value = this.viewJy;
            }

            if (this.mode === 'datetime') {
                const hSel = this.panel.querySelector('.dual-hour-select');
                const minSel = this.panel.querySelector('.dual-minute-select');
                if (hSel) hSel.value = this.selectedHour;
                if (minSel) minSel.value = this.selectedMinute;
            }

            this.renderCalendarGrid();
            this.updateSummaryFooter();
            this.updateTriggerBox();
        }

        renderCalendarGrid() {
            // بروزرسانی سلکتورها
            const mSel = this.panel.querySelector('.dual-month-select');
            const ySel = this.panel.querySelector('.dual-year-select');
            if (mSel) mSel.value = this.viewJm;
            if (ySel) ySel.value = this.viewJy;

            // محاسبه بازه معادل میلادی
            const daysInMonth = getDaysInJalaliMonth(this.viewJy, this.viewJm);
            const gStart = jalaliToGregorian(this.viewJy, this.viewJm, 1);
            const gEnd = jalaliToGregorian(this.viewJy, this.viewJm, daysInMonth);

            const gBadge = this.panel.querySelector('.dual-gregorian-range-badge');
            if (gBadge) {
                const faRange = `${GREGORIAN_MONTHS[gStart.gm - 1]} - ${GREGORIAN_MONTHS[gEnd.gm - 1]}`;
                const enRange = `${GREGORIAN_MONTHS_SHORT[gStart.gm - 1]} - ${GREGORIAN_MONTHS_SHORT[gEnd.gm - 1]}`;
                const yr = (gStart.gy === gEnd.gy) ? gStart.gy : `${gStart.gy}/${gEnd.gy}`;
                gBadge.innerHTML = `<i class="fas fa-globe-americas text-primary me-1"></i>${faRange} ${toPersianDigits(yr)} <span class="opacity-75 font-monospace">(${enRange} ${yr})</span>`;
            }

            const grid = this.panel.querySelector('.dual-calendar-grid');
            if (!grid) return;
            grid.innerHTML = '';

            // محاسبه روز شروع هفته (۰ = شنبه، ۶ = جمعه)
            const gStartDate = new Date(gStart.gy, gStart.gm - 1, gStart.gd);
            const startDayOfWeek = (gStartDate.getDay() + 1) % 7;

            // خانه‌های خالی قبل از شروع ماه
            for (let i = 0; i < startDayOfWeek; i++) {
                const emptyCell = document.createElement('div');
                emptyCell.className = 'dual-day-cell is-empty';
                grid.appendChild(emptyCell);
            }

            const now = new Date();
            const todayJ = gregorianToJalali(now.getFullYear(), now.getMonth() + 1, now.getDate());

            // تولید خانه‌های روزهای ماه
            for (let jd = 1; jd <= daysInMonth; jd++) {
                const gDay = jalaliToGregorian(this.viewJy, this.viewJm, jd);
                const isToday = (todayJ.jy === this.viewJy && todayJ.jm === this.viewJm && todayJ.jd === jd);
                const isSelected = (this.selectedJy === this.viewJy && this.selectedJm === this.viewJm && this.selectedJd === jd);

                const dayDate = new Date(gDay.gy, gDay.gm - 1, gDay.gd);
                const dOfWeek = (dayDate.getDay() + 1) % 7;
                const isFriday = (dOfWeek === 6);

                const cell = document.createElement('div');
                cell.className = 'dual-day-cell' +
                    (isSelected ? ' is-selected' : '') +
                    (isToday ? ' is-today' : '') +
                    (isFriday ? ' is-friday' : '');

                cell.title = `شمسی: ${toPersianDigits(jd)} ${SHAMSI_MONTHS[this.viewJm - 1]} ${toPersianDigits(this.viewJy)} | میلادی: ${gDay.gd} ${GREGORIAN_MONTHS[gDay.gm - 1]} ${gDay.gy}`;
                cell.onclick = () => this.selectDay(this.viewJy, this.viewJm, jd);

                const gregLabel = (gDay.gd === 1) ? `1 ${GREGORIAN_MONTHS_SHORT[gDay.gm - 1]}` : `${gDay.gd}`;

                cell.innerHTML = `
                    <div class="day-shamsi-number">${toPersianDigits(jd)}</div>
                    <div class="day-gregorian-number">${gregLabel}</div>
                `;

                grid.appendChild(cell);
            }
        }

        updateTriggerBox() {
            if (!this.selectedJy) {
                this.triggerBox.innerHTML = `
                    <div class="d-flex align-items-center gap-2 text-muted">
                        <i class="far fa-calendar-alt text-primary fs-5"></i>
                        <span>${this.placeholder}</span>
                    </div>
                    <i class="fas fa-chevron-down text-muted small"></i>
                `;
                return;
            }

            const g = jalaliToGregorian(this.selectedJy, this.selectedJm, this.selectedJd);
            const gDate = new Date(g.gy, g.gm - 1, g.gd, this.selectedHour, this.selectedMinute);
            const dayIdx = (gDate.getDay() + 1) % 7;
            const dayName = SHAMSI_WEEK_DAYS[dayIdx];

            const timeStr = `${String(this.selectedHour).padStart(2, '0')}:${String(this.selectedMinute).padStart(2, '0')}`;
            const timeStrFa = toPersianDigits(timeStr);

            const shamsiText = (this.mode === 'datetime') ?
                `${dayName}، ${toPersianDigits(this.selectedJd)} ${SHAMSI_MONTHS[this.selectedJm - 1]} ${toPersianDigits(this.selectedJy)} - ساعت ${timeStrFa}` :
                `${dayName}، ${toPersianDigits(this.selectedJd)} ${SHAMSI_MONTHS[this.selectedJm - 1]} ${toPersianDigits(this.selectedJy)}`;

            const gregText = (this.mode === 'datetime') ?
                `${g.gy}-${String(g.gm).padStart(2, '0')}-${String(g.gd).padStart(2, '0')} ${timeStr}` :
                `${g.gy}-${String(g.gm).padStart(2, '0')}-${String(g.gd).padStart(2, '0')}`;

            // محاسبه زمان مانده
            const diffMs = gDate.getTime() - Date.now();
            let badgeHtml = '';
            if (diffMs > 0) {
                const diffHours = Math.floor(diffMs / (1000 * 3600));
                const diffDays = Math.floor(diffHours / 24);
                if (diffDays > 0) {
                    badgeHtml = `<span class="badge bg-success-subtle text-success border border-success-subtle font-monospace">${toPersianDigits(diffDays)} روز مانده</span>`;
                } else if (diffHours > 0) {
                    badgeHtml = `<span class="badge bg-info-subtle text-info border border-info-subtle font-monospace">${toPersianDigits(diffHours)} ساعت مانده</span>`;
                } else {
                    badgeHtml = `<span class="badge bg-warning-subtle text-warning border border-warning-subtle">کمتر از ۱ ساعت</span>`;
                }
            } else if (Math.abs(diffMs) < 24 * 3600 * 1000) {
                badgeHtml = `<span class="badge bg-primary-subtle text-primary border border-primary-subtle">امروز</span>`;
            } else {
                badgeHtml = `<span class="badge bg-secondary-subtle text-secondary font-monospace">گذشته</span>`;
            }

            this.triggerBox.innerHTML = `
                <div class="d-flex align-items-center gap-2.5 overflow-hidden">
                    <i class="fas fa-calendar-check text-primary fs-5 flex-shrink-0"></i>
                    <div class="text-truncate">
                        <div class="fw-bold dual-trigger-shamsi text-truncate" style="font-size: 0.92rem;">${shamsiText}</div>
                        <div class="d-flex align-items-center gap-2 mt-0.5" style="font-size: 0.74rem;">
                            <span class="text-muted font-monospace"><i class="fas fa-globe-americas me-1 opacity-75"></i>${gregText}</span>
                            ${badgeHtml}
                        </div>
                    </div>
                </div>
                <div class="d-flex align-items-center gap-2 flex-shrink-0 ms-2">
                    ${this.allowClear ? `
                    <button type="button" class="btn btn-sm btn-link text-muted p-0 dual-trigger-clear-btn" title="حذف انتخاب" style="text-decoration: none;">
                        <i class="fas fa-xmark"></i>
                    </button>
                    ` : ''}
                    <i class="fas fa-chevron-down text-muted small"></i>
                </div>
            `;
        }

        updateSummaryFooter() {
            const sumShamsi = this.panel.querySelector('.dual-summary-shamsi');
            const sumSub = this.panel.querySelector('.dual-summary-sub');
            if (!sumShamsi || !sumSub) return;

            if (!this.selectedJy) {
                sumShamsi.textContent = 'هیچ تاریخی انتخاب نشده است';
                sumSub.textContent = 'روی یکی از روزهای تقویم بالا کلیک کنید';
                return;
            }

            const g = jalaliToGregorian(this.selectedJy, this.selectedJm, this.selectedJd);
            const gDate = new Date(g.gy, g.gm - 1, g.gd, this.selectedHour, this.selectedMinute);
            const dayIdx = (gDate.getDay() + 1) % 7;
            const dayName = SHAMSI_WEEK_DAYS[dayIdx];
            const gDayName = GREGORIAN_WEEK_DAYS[gDate.getDay()];

            const timeStr = `${String(this.selectedHour).padStart(2, '0')}:${String(this.selectedMinute).padStart(2, '0')}`;
            const timeStrFa = toPersianDigits(timeStr);

            sumShamsi.textContent = (this.mode === 'datetime') ?
                `${dayName}، ${toPersianDigits(this.selectedJd)} ${SHAMSI_MONTHS[this.selectedJm - 1]} ${toPersianDigits(this.selectedJy)} (ساعت ${timeStrFa})` :
                `${dayName}، ${toPersianDigits(this.selectedJd)} ${SHAMSI_MONTHS[this.selectedJm - 1]} ${toPersianDigits(this.selectedJy)}`;

            sumSub.innerHTML = `معادل میلادی: <strong class="font-monospace">${gDayName}, ${g.gd} ${GREGORIAN_MONTHS_SHORT[g.gm - 1]} ${g.gy}</strong>`;
        }
    }

    // ─── متدهای استاتیک و اتصالات کمکی ──────────────────────────────────
    DualDatePicker.attach = function(elementOrSelector, options = {}) {
        return new DualDatePicker(elementOrSelector, options);
    };

    DualDatePicker.gregorianToJalali = gregorianToJalali;
    DualDatePicker.jalaliToGregorian = jalaliToGregorian;
    DualDatePicker.toPersianDigits = toPersianDigits;
    DualDatePicker.isJalaliLeapYear = isJalaliLeapYear;
    DualDatePicker.getDaysInJalaliMonth = getDaysInJalaliMonth;

    DualDatePicker.initAll = function(root = document) {
        const elements = root.querySelectorAll('input[data-dual-picker]');
        elements.forEach(el => {
            if (!el.__dualDatePicker) {
                const mode = el.dataset.dualPicker || (el.type === 'datetime-local' ? 'datetime' : 'date');
                const inline = el.dataset.dualInline === 'true';
                DualDatePicker.attach(el, { mode, inline });
            }
        });
    };

    // اتواینیت به محض لود DOM
    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => DualDatePicker.initAll());
        } else {
            DualDatePicker.initAll();
        }
    }

    global.DualDatePicker = DualDatePicker;

})(typeof window !== 'undefined' ? window : this);
