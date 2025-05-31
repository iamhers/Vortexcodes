import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime

# ==================== Configuration ====================
CSV_URL = "https://github.com/iamhers/Vortexcodes/blob/main/expiry_list.csv"
CONTACT_URL = "https://t.me/PrayagRajj"
USE_COLOR = True  # Set to False for plain terminal output

# ==================== Color Helper ====================
def colorize(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m",
        "cyan" : "\033[96m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m" if USE_COLOR else text

RED = "91"
GREEN = "92"
YELLOW = "93"
CYAN = "96"
BOLD = "1"

# ==================== Typing Animation ====================
def live_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ==================== Time Formatter ====================
def format_remaining_time(expiry):
    now = datetime.now()
    if expiry <= now:
        return colorize("Expired", RED)

    total_seconds = int((expiry - now).total_seconds())

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days:    parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:   parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes: parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds: parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return colorize(", ".join(parts), GREEN)

# ==================== CSV Fetching ====================
def fetch_csv(url):
    try:
        live_text(colorize("📡 Fetching access list...", YELLOW))
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        live_text(colorize(f"🚨 Error fetching CSV: {e}", RED))
        sys.exit(1)

# ==================== Expiry Parser ====================
def parse_expiry(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        live_text(colorize("🚨 Invalid date format in CSV! Use 'YYYY-MM-DD HH:MM:SS'", RED))
        return None

# ==================== Access Check ====================
def check_access(user_id, csv_text):
    reader = csv.DictReader(csv_text.splitlines())
    now = datetime.now()

    for row in reader:
        row_id = row.get("id", "").strip().lower()
        expiry_str = row.get("expiry", "").strip()
        expiry_date = parse_expiry(expiry_str)
        if not expiry_date:
            continue

        if row_id == "all":
            if now > expiry_date:
                deny_access("⏳ Free access expired! Contact developer.")
            else:
                show_access_time(expiry_date)
            return

        if row_id == user_id.lower():
            if now > expiry_date:
                deny_access("⏳ Your access has expired! Contact developer.")
            else:
                show_access_time(expiry_date)
            return

    deny_access("🚫 You are not authorized! Contact developer.")

# ==================== Output Helpers ====================
def show_access_time(expiry_date):
    remaining = format_remaining_time(expiry_date)
    live_text(colorize("\n✅ Access Granted!", GREEN))
    live_text(colorize("⏱️ Time remaining: ", CYAN) + remaining)
    print(colorize("🔓 Welcome to Vortex Tool!", BOLD))

def deny_access(message):
    live_text(colorize(f"\n{message}", RED))
    live_text(colorize(f"📩 Contact: {CONTACT_URL}", CYAN))
    try:
        webbrowser.open(CONTACT_URL)
    except:
        pass
    sys.exit(1)

# ==================== Main Logic ====================
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
