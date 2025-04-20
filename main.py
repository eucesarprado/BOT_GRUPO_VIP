from telethon import TelegramClient, events
import os
from flask import Flask
from threading import Thread
import time
import requests

# 🔁 Uptime com Flask + Ping
app = Flask('')

@app.route('/')
def home():
    return "Bot está online!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def manter_online():
    Thread(target=run_flask).start()

    def ping():
        while True:
            try:
                requests.get("https://SEULINK.railway.app")  # troque pelo seu link Railway
                print("🔁 Ping enviado.")
            except:
                print("⚠️ Erro ao enviar ping.")
            time.sleep(280)

    Thread(target=ping).start()

manter_online()

# 🔐 Credenciais do Telegram
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
client = TelegramClient("session", api_id, api_hash)

# 🛰️ Grupos
origens = [-1002368866066, -4686930379]
destino_id = -1002632937431

# 🔁 Álbuns já enviados
grouped_processados = set()

# ♻️ Limpeza periódica do cache
def limpar_cache():
    while True:
        time.sleep(1800)
        grouped_processados.clear()
        print("♻️ Cache de grouped_processados limpo.")
Thread(target=limpar_cache).start()

@client.on(events.NewMessage(chats=origens))
async def handler(event):
    msg = event.message

    # Verifica se é álbum
    if msg.grouped_id:
        if msg.grouped_id in grouped_processados:
            return
        grouped_processados.add(msg.grouped_id)

        print("📦 Álbum detectado.")
        mensagens = await client.get_messages(event.chat_id, limit=20, min_id=msg.id - 10)
        album = [m for m in mensagens if m.grouped_id == msg.grouped_id]
        album = list(reversed(album))

        midias = [m.media for m in album if m.media]

        if midias:
            print(f"🎯 Enviando álbum com {len(midias)} mídias...")
            await client.send_file(destino_id, midias)
        else:
            print("⚠️ Nenhuma mídia no álbum.")
    elif msg.photo or msg.video:
        print("📸 Mídia única detectada.")
        await client.send_file(destino_id, msg.media)
    else:
        print("❌ Ignorado (sem mídia).")

# 🚀 Inicia o bot
async def main():
    await client.start()
    print("🤖 Bot VIP rodando sem legenda nem botão.")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
