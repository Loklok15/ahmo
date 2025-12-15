import requests
import time
import re

# ================== TELEGRAM ==================
BOT_TOKEN = "8514660472:AAH0LriIcVF7CxOLfcXIfBtO0SjK4BmvAYI"
CHAT_ID = "6968718713"
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
]

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

# ================== OTURUM AÇ ==================
for mail in MAILLER:
    token = token_al(mail)
    if token:
        oturumlar[mail] = {
            "Authorization": f"Bearer {token}"
        }
        okunan[mail] = set()

print(f"🚀 {len(oturumlar)} mail aktif izleniyor")

# ================== ANA DÖNGÜ ==================
ilk_calisti = True

while True:
    for mail, headers in oturumlar.items():
        try:
            r = requests.get(f"{API}/messages", headers=headers, timeout=10)
            r.raise_for_status()

            for m in r.json().get("hydra:member", []):
                if m["id"] in okunan[mail]:
                    continue

                okunan[mail].add(m["id"])

                # ilk çalışmada sadece işaretle
                if ilk_calisti:
                    continue

                d = requests.get(
                    f"{API}/messages/{m['id']}",
                    headers=headers,
                    timeout=10
                ).json()

                text = ""
                if d.get("text"):
                    text += d["text"]
                if isinstance(d.get("html"), list):
                    text += " ".join(d["html"])

                kodlar = set(re.findall(r"\b\d{6}\b", text))
                kodlar.discard("000000")

                for kod in kodlar:
                    telegram_gonder(f"🔐 KOD: {kod}\n📧 {mail}")
                    print(f"📩 Telegram gönderildi: {kod} ({mail})", flush=True)

        except Exception as e:
            print(f"❌ hata: {mail} → {e}", flush=True)

    if ilk_calisti:
        print("🧊 İlk tarama bitti, artık sadece YENİ mailler gönderilecek", flush=True)
        ilk_calisti = False

    time.sleep(20)
