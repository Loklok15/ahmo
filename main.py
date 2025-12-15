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
ilk_calisti = True

while True:
    for mail, headers in oturumlar.items():
        try:
            r = requests.get(f"{API}/messages", headers=headers, timeout=10)
            r.raise_for_status()

            for m in r.json()["hydra:member"]:
                if m["id"] in okunan[mail]:
                    continue

                okunan[mail].add(m["id"])

                # 🔒 İlk çalışmada SADECE işaretle, gönderme
                if ilk_calisti:
                    continue

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

                # 🔥 TEKILLEŞTİR
              for kod in kodlar:
                    if kod != "000000":
                        telegram_gonder(kod, mail)
                        print(f"📩 Telegram gönderildi: {kod} ({mail})", flush=True)

        except Exception as e:
            print(f"❌ hata: {mail} → {e}", flush=True)

    if ilk_calisti:
        print("🧊 İlk tarama tamamlandı, artık yeni mailler izleniyor", flush=True)
        ilk_calisti = False

    time.sleep(20)


