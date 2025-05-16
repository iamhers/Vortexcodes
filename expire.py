import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# ========== Configuration ==========
CSV_URL = "https://raw.githubusercontent.com/jaikshaikh/Vortexcodes/refs/heads/main/expiry_list.csv"
CONTACT_URL = "https://t.me/PrayagRajj"
IST = ZoneInfo("Asia/Kolkata")  # All expiry timestamps are in IST
USE_COLOR = True

# ========== Terminal Colors ==========
def colorize(text, code): return f"\033[{code}m{text}\033[0m" if USE_COLOR else text
RED, GREEN, YELLOW, CYAN, BOLD = "91", "92", "93", "96", "1"

def live_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ========== Time Remaining Formatter ==========
def format_remaining_time(expiry_ist):
    now_ist = datetime.now(IST)
    if expiry_ist <= now_ist:
        return colorize("Expired", RED)

    total_seconds = int((expiry_ist - now_ist).total_seconds())
    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days: parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours: parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes: parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds: parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return colorize(", ".join(parts), GREEN)

# ========== Parse Expiry (assumes IST in CSV) ==========
def parse_expiry(date_str):
    try:
        naive = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S")
        return naive.replace(tzinfo=IST)
    except Exception:
        live_text(colorize("🚨 Invalid expiry format! Use 'YYYY-MM-DD HH:MM:SS'", RED))
        return None

# ========== CSV Download ==========
def fetch_csv(url):
    try:
        live_text(colorize("📡 Fetching access list...", YELLOW))
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        live_text(colorize(f"🚨 Error fetching CSV: {e}", RED))
        sys.exit(1)

# ========== Access Logic ==========
def check_access(user_id, csv_text):
    reader = csv.DictReader(csv_text.splitlines())
    now_ist = datetime.now(IST)

    for row in reader:
        row_id = row.get("id", "").strip().lower()
        expiry_str = row.get("expiry", "").strip()
        expiry_dt = parse_expiry(expiry_str)
        if not expiry_dt:
            continue

        if row_id == "all":
            return validate_access(expiry_dt, now_ist, "⏳ Free access expired!")
        elif row_id == user_id.lower():
            return validate_access(expiry_dt, now_ist, "⏳ Your access has expired!")

    deny_access("🚫 You are not authorized! Contact developer.")

def validate_access(expiry_ist, now_ist, error_msg):
    if now_ist > expiry_ist:
        deny_access(error_msg)
    else:
        show_access_time(expiry_ist)

def show_access_time(expiry_ist):
    remaining = format_remaining_time(expiry_ist)
    live_text(colorize("\n✅ Access Granted!", GREEN))
    live_text(colorize("⏱ Time remaining: ", CYAN) + remaining)
    print(colorize("🔓 Welcome to the system!", BOLD))

def deny_access(msg):
    live_text(colorize(f"\n{msg}", RED))
    live_text(colorize(f"📩 Contact: {CONTACT_URL}", CYAN))
    try:
        webbrowser.open(CONTACT_URL)
    except:
        pass
    sys.exit(1)

# ========== Main ==========
def main():
    try:
        user_id = str(ID)
    except NameError:
        user_id = input(colorize("🔐 Enter your ID: ", CYAN)).strip()

    csv_data = fetch_csv(CSV_URL)
    if csv_data:
        check_access(user_id, csv_data)

if __name__ == "__main__":
    main()
