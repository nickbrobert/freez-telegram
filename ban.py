from pyrogram import Client
from pyrogram.errors import UserNotParticipant, FloodWait, UserRestricted
import os
import json
import time

def ban_user(username):
    session_files = [f for f in os.listdir("sessions") if f.endswith(".session")]
    
    if not session_files:
        print("Нет активных сессий")
        return
    
    for session in session_files:
        try:
            app = Client(session[:-8], workdir="sessions")
            app.start()
            
            storage_file = f"storage/{session[:-8]}.json"
            
            if not os.path.exists(storage_file):
                print(f"Нет каналов для сессии {session}")
                app.stop()
                continue
            
            with open(storage_file, 'r') as f:
                channels = json.load(f)
            
            banned_count = 0
            for channel_id in channels:
                try:
                    app.ban_chat_member(channel_id, username)
                    banned_count += 1
                    print(f"Забанен в канале {channel_id}")
                    time.sleep(1)
                    
                except UserNotParticipant:
                    continue
                except FloodWait as e:
                    print(f"Флудвейт {e.value} секунд на сессии {session}")
                    break
                except Exception as e:
                    print(f"Ошибка в канале {channel_id}: {e}")
                    continue
            
            print(f"Всего забанено в {banned_count} каналах")
            app.stop()
            
        except FloodWait as e:
            print(f"Флудвейт при старте сессии {session}: {e.value} секунд")
            continue
        except UserRestricted:
            print(f"Аккаунт {session} ограничен, пропускаем")
            continue
        except Exception as e:
            print(f"Проблема с сессии {session}: {e}")
            continue
