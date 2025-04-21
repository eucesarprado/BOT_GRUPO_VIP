from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument
import os
import time

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
client = TelegramClient("session4", api_id, api_hash)

origem_id = -1002368866066
destino_id = -1002632937431
enviados_file = "ids_enviados.txt"

def carregar_ids_enviados():
    if not os.path.exists(enviados_file):
        return set()
    with open(enviados_file, "r") as f:
        return set(map(int, f.read().splitlines()))

def salvar_id_enviado(msg_id):
    with open(enviados_file, "a") as f:
        f.write(f"{msg_id}\n")

print("🔄 Iniciando busca de vídeos antigos...")
ids_enviados = carregar_ids_enviados()

with client:
    while True:
        for msg in client.iter_messages(origem_id):
            if msg.id in ids_enviados:
                continue
            if msg.video or (isinstance(msg.media, MessageMediaDocument) and msg.file and 'video' in msg.file.mime_type):
                try:
                    client.send_file(destino_id, msg.media)
                    salvar_id_enviado(msg.id)
                    print(f"✅ Vídeo enviado | ID {msg.id}")
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Erro ao enviar ID {msg.id}: {e}")
            else:
                print(f"⏭️ Ignorado (ID {msg.id})")
        print("🚀 Fim do histórico. Reiniciando em 5 minutos...")
        time.sleep(300)
