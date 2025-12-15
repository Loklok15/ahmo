import requests
import time
import re
import smtplib
from email.mime.text import MIMEText

# ================== GMAIL AYARLARI ==================
GMAIL_USER = "torloto16@gmail.com"
GMAIL_PASS = "bthv rqun zufo itbj"   # BOŞLUKLU OLABİLİR
GMAIL_TO   = "torloto16@gmail.com"

# ================== MAIL.TM AYARLARI ==================
API = "https://api.mail.tm"
PASSWORD = "Aa123123"

MAIL_LISTESI = [
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

# ================== SMTP TEK BAĞLANTI ==================
SMTP = smtplib.SMTP("smtp.gmail.com", 587)
SMTP.starttls()
SMTP.login(GMAIL_USER, GMAIL_PASS)

# ================== OTURUMLAR ==================
oturumlar = {}
okunan = {}

def token_al(mail):
    r = requests.post(f"{API}/token", json={
        "address": mail,
        "password": PASSWORD
    })
    if r.status_code != 200:
        print("❌ token alınamadı:", mail)
        return None
    return r.json()["token"]

for mail in MAIL_LISTESI:
    token = token_al(mail)
    if token:
        oturumlar[mail] = {"Authorization": f"Bearer {token}"}
        okunan[mail] = set()

print(f"🚀 {len(oturumlar)} mail aktif izleniyor")

# ================== GMAIL GÖNDER ==================
def gmail_gonder(mail, subject, kodlar):
    # iOS klavye uyumlu TEK SATIR
    icerik = f"{mail}\n\n" + "  ".join(kodlar)

    msg = MIMEText(icerik)
    msg["Subject"] = "🔐 DOĞRULAMA KODU"
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_TO

    SMTP.send_message(msg)
    print("📤 gönderildi:", mail, kodlar)

# ================== ANA DÖNGÜ (HIZLI) ==================
while True:
    for mail, headers in oturumlar.items():
        try:
            r = requests.get(f"{API}/messages", headers=headers, timeout=5)
            r.raise_for_status()

            # SADECE SON MAİL
            for m in r.json()["hydra:member"][:1]:
                if m["id"] in okunan[mail]:
                    continue

                okunan[mail].add(m["id"])

                d = requests.get(
                    f"{API}/messages/{m['id']}",
                    headers=headers,
                    timeout=5
                ).json()

                text = ""
                if isinstance(d.get("text"), str):
                    text += d["text"]
                if isinstance(d.get("html"), list):
                    text += " ".join(d["html"])

                kodlar = re.findall(r"\b\d{6}\b", text)
                kodlar = [k for k in kodlar if k != "000000"]

                if kodlar:
                    gmail_gonder(mail, d.get("subject", ""), list(set(kodlar)))

        except Exception as e:
            print("❌ hata:", mail, e)

    time.sleep(2)  # ⚡ 2 saniye = aşırı hızlı
