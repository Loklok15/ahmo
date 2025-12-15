import requests
import time
import re

# ================== TELEGRAM ==================
BOT_TOKEN = "8514660472:AAEMoK8OPCin12-uTDIabe2bdx8uHmk0trw"
CHAT_ID  = "6968718713"

def telegram_gonder(metin):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": metin
    })

# ================== MAIL.TM ==================
API = "https://api.mail.tm"
PASSWORD = "Aa123123"

MAILLER = [
    "plasticframe19@comfythings.com",
    "redmugx55@comfythings.com",
    "quietfan203@comfythings.com",
    "darkmirror15@comfythings.com",
    "tinybox404@comfythings.com",
    "goldenspoon68@comfythings.com",
    "heavybag77@comfythings.com",
    "medi16@comfythings.com",
    "ahmo12@comfythings.com",
    "bluechairx7@comfythings.com",
    "texsas@comfythings.com",
    "wina@comfythings.com",
    "rayban34@comfythings.com",
    "cilginco@comfythings.com",
    "retry34@comfythings.com",
    "fero16@comfythings.com",
    "wonderman@comfythings.com",
    "rezlesne500@comfythings.com",
    "drakula16@comfythings.com",
    "fullforce@comfythings.com",
    "jackpot94@comfythings.com"
]

# ================== DURUM ==================
oturumlar = {}
okunan = {}

def token_al(mail):
    r = requests.post(f"{API}/token", json={
        "address": mail,
        "password": PASSWORD
    })
    if r.status_code != 200:
        return None
    return r.json()["token"]

# ================== OTURUMLARI AÇ ==================
for mail in MAILLER:
    token = token_al(mail)
    if token:
        oturumlar[mail] = {
            "Authorization": f"Bearer {token}"
        }
        okunan[mail] = set()

print(f"🚀 {len(oturumlar)} mail aktif izleniyor")

# ================== ANA DÖNGÜ ==================
while True:
    for mail, headers in oturumlar.items():
        try:
            r = requests.get(f"{API}/messages", headers=headers, timeout=10)
            r.raise_for_status()

            for m in r.json().get("hydra:member", []):
                if m["id"] in okunan[mail]:
                    continue

                okunan[mail].add(m["id"])

                d = requests.get(
                    f"{API}/messages/{m['id']}",
                    headers=headers,
                    timeout=10
                ).json()

                text = ""
                if isinstance(d.get("text"), str):
                    text += d["text"]
                if isinstance(d.get("html"), list):
                    text += " ".join(d["html"])

                kodlar = re.findall(r"\b\d{6}\b", text)
                kodlar = [k for k in kodlar if k != "000000"]

                for kod in kodlar:
                    telegram_gonder(
                        f"🔐 KOD: {kod}\n📧 {mail}"
                    )
                    print(f"📩 Telegram gönderildi: {kod} ({mail})")

        except Exception as e:
            print("❌ hata:", mail, e)

    time.sleep(10)
