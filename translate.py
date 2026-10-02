import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# I will specifically target the strings I wrote in swiss_minimal.
c = c.replace(">Username</span>", ">نام کاربری</span>")
c = c.replace(">Password</span>", ">رمز عبور</span>")
c = c.replace(">Captcha Code</span>", ">شناسه امنیتی (Captcha)</span>")
c = c.replace("Sign In\n                            </div>\n                        {% else %}", "ورود\n                            </div>\n                        {% else %}")
c = c.replace(">Forgot password?</a>", ">فراموشی رمز؟</a>")
c = c.replace("placeholder=\"username\"", "placeholder=\"username\"")

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
