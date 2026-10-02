import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_user = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">نام کاربری</span>
                                  <div class="flex-grow-1"></div>
                              </div>
                              <div class="d-flex align-items-center" style="border-bottom: 2px solid #fff; padding-bottom: 2px;">
                                  <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5" name="username" placeholder="username" required autofocus style="direction: ltr; text-align: left;">
                              </div>
                          </div>"""

new_user = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-2">
                                  <div style="width: 30px; height: 1px; background: rgba(255,255,255,0.2);"></div>
                                  <span class="text-white opacity-75 px-2" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">نام کاربری</span>
                                  <div style="flex-grow: 1; height: 1px; background: rgba(255,255,255,0.2);"></div>
                              </div>
                              <div class="d-flex align-items-center pb-2" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" name="username" placeholder="username" required autofocus style="direction: ltr; text-align: left; font-family: -apple-system, sans-serif; font-weight: 300;">
                              </div>
                          </div>"""

c = c.replace(old_user, new_user)

old_pass = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">رمز عبور</span>
                                  <div class="flex-grow-1"></div>
                              </div>
                              <div class="d-flex align-items-center" style="border-bottom: 2px solid #fff; padding-bottom: 2px;">
                                  <i class="fas fa-lock text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="password" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5" name="password" id="loginPasswordInput" placeholder="••••••••" required style="direction: ltr; text-align: left; letter-spacing: 2px;">
                                  <button type="button" class="btn btn-link text-white opacity-50 p-0 shadow-none text-decoration-none ms-2" onclick="togglePasswordVisibility()">
                                      <i class="fas fa-eye" id="passwordToggleIcon"></i>
                                  </button>
                              </div>
                          </div>"""

new_pass = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-2">
                                  <div style="width: 30px; height: 1px; background: rgba(255,255,255,0.2);"></div>
                                  <span class="text-white opacity-75 px-2" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">رمز عبور</span>
                                  <div style="flex-grow: 1; height: 1px; background: rgba(255,255,255,0.2);"></div>
                              </div>
                              <div class="d-flex align-items-center pb-2" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <i class="fas fa-lock text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="password" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" name="password" id="loginPasswordInput" placeholder="••••••••" required style="direction: ltr; text-align: left; letter-spacing: 2px;">
                              </div>
                          </div>"""
c = c.replace(old_pass, new_pass)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED INPUTS")
