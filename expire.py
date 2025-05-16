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
def format_remaining_time(expiry_ist, now_ist):
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

# ========== Get User Timezone ==========
def get_user_timezone():
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5)
        res.raise_for_status()
        tz_str = res.json().get("timezone")
        return ZoneInfo(tz_str)
    except Exception:
        live_text(colorize("⚠️ Could not detect timezone. Defaulting to UTC.", YELLOW))
        return ZoneInfo("UTC")

# ========== Access Logic ==========
def check_access(user_id, csv_text, now_ist, user_tz):
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        row_id = row.get("id", "").strip().lower()
        expiry_str = row.get("expiry", "").strip()
        expiry_dt = parse_expiry(expiry_str)
        if not expiry_dt:
            continue

        if row_id == "all":
            return validate_access(expiry_dt, now_ist, "⏳ Free access expired!", user_tz)
        elif row_id == user_id.lower():
            return validate_access(expiry_dt, now_ist, "⏳ Your access has expired!", user_tz)

    deny_access("🚫 You are not authorized! Contact developer.")

def validate_access(expiry_dt, now_ist, error_msg, user_tz):
    # If user is in IST, show the time normally
    if user_tz == IST:
        return show_access_time(expiry_dt, now_ist)

    # If user is not in IST, adjust for time zone difference
    expiry_local = expiry_dt.astimezone(user_tz)
    remaining_local = format_remaining_time(expiry_local, now_ist)
    live_text(colorize(f"\n✅ Access Granted! ({user_tz})", GREEN))
    live_text(colorize(f"⏱ Time remaining: ", CYAN) + remaining_local)
    print(colorize("🔓 Welcome to the system!", BOLD))

def show_access_time(expiry_ist, now_ist):
    remaining = format_remaining_time(expiry_ist, now_ist)
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

    # Get user's real-time in IST (converted from their local time zone)
    user_tz = get_user_timezone()
    now_user_local = datetime.now(user_tz)
    now_ist = now_user_local.astimezone(IST)

    csv_data = fetch_csv(CSV_URL)
    if csv_data:
        check_access(user_id, csv_data, now_ist, user_tz)

if __name__ == "__main__":
    main()
