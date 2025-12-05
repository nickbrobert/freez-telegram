from pyrogram import Client
import os

api_id = input("Введите API ID: ")
api_hash = input("Введите API Hash: ")

if not os.path.exists("sessions"):
    os.makedirs("sessions")

session_name = input("Введите имя для сессии: ")

with Client(session_name, api_id=api_id, api_hash=api_hash, workdir="sessions") as app:
    print(f"Сессия {session_name} создана")
    print(f"ID аккаунта: {app.get_me().id}")