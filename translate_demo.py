import io

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("<span>Username</span>", "<span>نام کاربری</span>")
c = c.replace("<span>Password</span>", "<span>رمز عبور</span>")
c = c.replace(">Captcha Code</span>", ">شناسه امنیتی (Captcha)</span>")
c = c.replace(">Sign In</button>", ">ورود</button>")
c = c.replace(">Forgot password?</span>", ">فراموشی رمز؟</span>")
c = c.replace(">Welcome back.</div>", ">خوش آمدید.</div>")
c = c.replace(">Sign in to continue.</div>", ">برای ادامه وارد شوید.</div>")

# Adjust demo text alignment to rtl
c = c.replace('id="tab-swiss" dir="ltr"', 'id="tab-swiss" dir="rtl"')

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
