import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Configuration
CSV_URL = "https://raw.githubusercontent.com/jaikshaikh/Vortexcodes/refs/heads/main/expiry_list.csv"
CONTACT_URL = "https://t.me/PrayagRajj"

try:
    USER_ID = str(ID)
except NameError:
    USER_ID = input("🔐 Enter your ID: ").strip()

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

def format_remaining_time(expiry):
    now = datetime.now()
    if expiry <= now:
        return "Expired"

    delta = relativedelta(expiry, now)
    parts = []
    if delta.years:   parts.append(f"{delta.years} year{'s' if delta.years > 1 else ''}")
    if delta.months:  parts.append(f"{delta.months} month{'s' if delta.months > 1 else ''}")
    if delta.days:    parts.append(f"{delta.days} day{'s' if delta.days > 1 else ''}")
    if delta.hours:   parts.append(f"{delta.hours} hour{'s' if delta.hours > 1 else ''}")
    if delta.minutes: parts.append(f"{delta.minutes} minute{'s' if delta.minutes > 1 else ''}")
    if delta.seconds: parts.append(f"{delta.seconds} second{'s' if delta.seconds > 1 else ''}")
    
    return ", ".join(parts)

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
                show_access_time(expiry_date)
            return

        if row_id == user_id.lower():
            if current_time > expiry_date:
                deny_access("⏳ Your access has expired! Contact developer.")
            else:
                show_access_time(expiry_date)
            return

    deny_access("🚫 You are not authorized! Contact developer.")

def show_access_time(expiry_date):
    remaining = format_remaining_time(expiry_date)
    live_text(f"✅ Access valid.\n⏱ Time remaining: {remaining}")

def deny_access(message):
    live_text(f"\n    {message}")
    live_text(f"    📩 Contact: {CONTACT_URL}")
    webbrowser.open(CONTACT_URL)
    sys.exit()

# Run the main logic
csv_data = fetch_csv(CSV_URL)
if csv_data:
    check_access(USER_ID, csv_data)
