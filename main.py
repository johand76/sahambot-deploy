from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Telegram Bot Setup
TOKEN = '7719699145:AAGYU7WRi1HdeNY6IW6EofhxnJl_wOJuQ5Q'
CHAT_ID = '-1002658465207'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# Google Sheets Setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPE)
client = gspread.authorize(CREDS)

SHEET_URL = 'https://docs.google.com/spreadsheets/d/149VQbfcpiDt6B3g_QIwgFALegxkuJK6ut_dsIj18YMo/edit'
worksheet = client.open_by_url(SHEET_URL).sheet1

# Flask App
app = Flask(__name__)

def send_message(text):
    requests.post(API_URL, data={
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    })

def get_content(waktu):
    rows = worksheet.get_all_records()
    for row in rows:
        if row['waktu'].lower() == waktu.lower():
            return f"*{row['judul']}*\n\n{row['konten']}"
    return f"⚠️ Tidak ditemukan konten untuk waktu: `{waktu}`"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        text = data["message"].get("text", "").strip().lower()
        if text == "/pagi":
            send_message(get_content("pagi"))
        elif text == "/midday":
            send_message(get_content("midday"))
        elif text == "/closing":
            send_message(get_content("closing"))
        else:
            send_message("Perintah tidak dikenali. Gunakan:\n/pagi\n/midday\n/closing")
    return {"ok": True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
