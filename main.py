import requests
import time
import re

# ================== TELEGRAM ==================
TELEGRAM_TOKEN = "8514660472:AAH0LriIcVF7CxOLfcXIfBtO0SjK4BmvAYI"
TELEGRAM_CHAT_ID = "6968718713"

TG_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def telegram_gonder(mesaj):
    requests.post(TG_URL, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj
    }, timeout=5)

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
    "jackpot94@comfythings.com",
    "wildwin16@comfythings.com",
    "carrick1@comfythings.com",
    "cimkeri16@comfythings.com",
    "sfenks16@comfythings.com",
    "maskof43@comfythings.com",
    "ahmet444@comfythings.com",
    "scanner15@comfythings.com",
    "wildwild16@comfythings.com",
    "umtbyrm16@comfythings.com",
    "save34@comfythings.com",
    "brsdn1616@comfythings.com",
    "silverlamp34@comfythings.com",
    "cozytable91@comfythings.com",
    "kuzukurt@comfythings.com",
    "ahmo581@comfythings.com",
    "ahmo585521@comfythings.com",
    "ahmo58552@comfythings.com",
    "ahmo5855@comfythings.com",
    "ahmo10771@comfythings.com",
    "ahmo10772@comfythings.com",
    "ahmo10773@comfythings.com",
    "ahmo10774@comfythings.com",
    "ahmo10775@comfythings.com",
    "ahmo10776@comfythings.com",
    "ahmo10777@comfythings.com",
    "cottonpillowx4@comfythings.com",
    "previous1294@comfythings.com",
    "softblanket07@comfythings.com",
    "woodencup72@comfythings.com",
    "youwin@comfythings.com"
]

# ================== SESSION ==================
session = requests.Session()
oturumlar = {}
okunan = {}

def token_al(mail):
    r = session.post(f"{API}/token", json={
        "address": mail,
        "password": PASSWORD
    }, timeout=5)

    if r.status_code != 200:
        return None

    return r.json()["token"]

# ================== BAŞLAT ==================
for mail in MAILLER:
    token = token_al(mail)
    if not token:
        continue

    oturumlar[mail] = {
        "Authorization": f"Bearer {token}"
    }
    okunan[mail] = None  # sadece son mail ID tutulur

print(f"🚀 {len(oturumlar)} mail ultra optimize izleniyor")

# ================== LOOP ==================
while True:
    for mail, headers in oturumlar.items():
        try:
            r = session.get(f"{API}/messages", headers=headers, timeout=5)
            mesajlar = r.json().get("hydra:member", [])
            if not mesajlar:
                continue

            son = mesajlar[0]
            mid = son["id"]

            if okunan[mail] == mid:
                continue

            okunan[mail] = mid

            d = session.get(
                f"{API}/messages/{mid}",
                headers=headers,
                timeout=5
            ).json()

            text = ""
            if isinstance(d.get("text"), str):
                text += d["text"]
            if isinstance(d.get("html"), list):
                text += " ".join(d["html"])

            kodlar = [k for k in re.findall(r"\b\d{6}\b", text) if k != "000000"]
            if not kodlar:
                continue

            kod = kodlar[-1]

            telegram_gonder(
                f"🔐 DOĞRULAMA KODU\n\n{kod}\n\n📧 {mail}"
            )

            print(f"📩 Telegram → {kod} ({mail})")

        except Exception as e:
            print("❌", mail, e)

    time.sleep(3)
