import customtkinter as ctk
import random
import string
import requests

# ===== НАСТРОЙКИ =====
SERVER_URL = "https://ТВОЙ-СЕРВЕР.onrender.com/add_key"
ADMIN_PASSWORD = "Kalambur01"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Ultimate Optimization — KeyManager")
app.geometry("520x420")
app.resizable(False, False)

# ===== UI =====
title = ctk.CTkLabel(app, text="KeyManager", font=("Segoe UI", 26, "bold"))
title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(app, text="Генератор одноразовых ключей", font=("Segoe UI", 14))
subtitle.pack(pady=(0, 20))

result_box = ctk.CTkEntry(app, width=360, height=40, justify="center", font=("Consolas", 16))
result_box.pack(pady=10)

status_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 12))
status_label.pack(pady=5)

# ===== ЛОГИКА =====
def generate_key(prefix):
    def block():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{block()}-{block()}"

def send_key(plan, prefix):
    key = generate_key(prefix)
    result_box.delete(0, "end")
    result_box.insert(0, key)

    data = {
        "password": ADMIN_PASSWORD,
        "key": key,
        "plan": plan
    }

    try:
        r = requests.post(SERVER_URL, json=data, timeout=5)
        if r.json().get("ok"):
            status_label.configure(text="✅ Ключ сохранён на сервере", text_color="green")
        else:
            status_label.configure(text="❌ Ошибка сервера", text_color="red")
    except:
        status_label.configure(text="❌ Сервер недоступен", text_color="red")

# ===== КНОПКИ =====
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=20)

ctk.CTkButton(
    btn_frame,
    text="Стабильный FPS — 1000",
    width=260,
    command=lambda: send_key(1, "ULT1")
).pack(pady=5)

ctk.CTkButton(
    btn_frame,
    text="FPS + Интернет — 1800",
    width=260,
    command=lambda: send_key(2, "ULT2")
).pack(pady=5)

ctk.CTkButton(
    btn_frame,
    text="Максимальная мощность — 4500",
    width=260,
    command=lambda: send_key(3, "ULT3")
).pack(pady=5)

info = ctk.CTkLabel(
    app,
    text="Ключ сразу уходит на сервер и становится одноразовым",
    font=("Segoe UI", 12),
    text_color="#94a3b8"
)
info.pack(pady=10)

app.mainloop()
