import os
from creator import create_channels
from ban import ban_user

print("== Успешно запущено ==")
target = input("Введите юзернейм цели: ").strip()

if not os.path.exists("sessions"):
    os.makedirs("sessions")

print("[1/2] Создаю каналы...")
create_channels()

print("[2/2] Блокирую цель...")
ban_user(target)

print(">> Готово")
