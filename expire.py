import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime

CSV_URL = "https://raw.githubusercontent.com/jaikshaikh/Vortexcodes/refs/heads/main/expiry_list.csv"

try:
    USER_ID = str(ID)
except NameError:
    USER_ID = input("Enter your ID: ").strip()

def live_text(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def fetch_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        live_text(f"🚨 Error fetching CSV: {e}")
        return None

def parse_expiry(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        live_text("🚨 Error: Invalid date format in CSV! Expected 'YYYY-MM-DD HH:MM:SS'")
        return None

def check_access(user_id, csv_text):
    reader = csv.DictReader(csv_text.splitlines())
    current_time = datetime.now()
    
    for row in reader:
        row_id = row.get("id", "").strip().lower()
        expiry_str = row.get("expiry", "").strip()
        expiry_date = parse_expiry(expiry_str)
        if not expiry_date:
            return

        if row_id == "all":
            if current_time > expiry_date:
                deny_access("⏳ Free access expired! Contact developer.")
            else:
                time_left(expiry_date)
            return

        if row_id == user_id.lower():
            if current_time > expiry_date:
                deny_access("⏳ Your access has expired! Contact developer.")
            else:
                time_left(expiry_date)
            return

    deny_access("🚫 You are not authorized! Contact developer.")

def time_left(expiry_date):
    remaining = expiry_date - datetime.now()
    live_text(f"✅ Access valid. Time remaining: {str(remaining).split('.')[0]}")

def deny_access(message):
    live_text(f"    {message}")
    live_text("    📩 Contact: https://t.me/PrayagRajj")
    webbrowser.open("https://t.me/PrayagRajj")
    sys.exit()

# Run the main logic
csv_data = fetch_csv(CSV_URL)
if csv_data:
    check_access(USER_ID, csv_data)
