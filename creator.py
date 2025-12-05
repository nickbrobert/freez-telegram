from pyrogram import Client
from pyrogram.errors import FloodWait, UserRestricted
import os
import json
import time

def create_channels():
    session_files = [f for f in os.listdir("sessions") if f.endswith(".session")]
    
    if not session_files:
        print("Нет активных сессий")
        return
    
    for session in session_files:
        app = Client(session[:-8], workdir="sessions")
        try:
            app.start()
            print(f"Работаю с сессией: {session}")
            
            storage_file = f"storage/{session[:-8]}.json"
            os.makedirs("storage", exist_ok=True)
            
            if os.path.exists(storage_file):
                with open(storage_file, 'r') as f:
                    channels = json.load(f)
            else:
                channels = []
            
            while len(channels) < 40:
                try:
                    new_channel = app.create_channel(f"chat_{len(channels)+1}", "Канал")
                    channels.append(new_channel.id)
                    
                    with open(storage_file, 'w') as f:
                        json.dump(channels, f)
                    
                    print(f"Канал {len(channels)} создан")
                    time.sleep(3)
                    
                except FloodWait as e:
                    print(f"Флудвейт {e.value} секунд на сессии {session}")
                    app.stop()
                    break
                except UserRestricted:
                    print(f"Аккаунт {session} ограничен, пропускаем")
                    app.stop()
                    break
                except Exception as e:
                    print(f"Ошибка: {e}")
                    break
            
            if app.is_connected:
                app.stop()
            
        except FloodWait as e:
            print(f"Флудвейт при старте сессии {session}: {e.value} секунд")
            continue
        except UserRestricted:
            print(f"Аккаунт {session} полностью ограничен")
            continue
        except Exception as e:
            print(f"Проблема с сессией {session}: {e}")
            continue
