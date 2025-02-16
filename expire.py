import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime
CSV_URL = "https://raw.githubusercontent.com/jaikshaikh/Vortexcodes/refs/heads/main/expiry_list.csv"
USER_ID = str(ID)  # Replace ID with actual variable or input
def live_text(text, delay=0.05):
    """Prints text character by character with a delay for a typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  

def fetch_csv(url):
    """Fetches CSV data from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        live_text(f"🚨 Error fetching CSV: {e}")
        return None

def check_expiry(user_id, csv_data):
    """Checks if the user ID is in the CSV and verifies expiry status."""
    reader = csv.reader(csv_data.splitlines())
    next(reader)  # Skip header

    all_users_allowed = False
    user_found = False
    expiry_date = None

    for row in reader:
        if row[0].lower() == "all":
            all_users_allowed = True
            try:
                expiry_date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                live_text(f"    🚨 Error: Invalid date format in CSV!")
                return
            break
        elif row[0] == user_id:
            user_found = True
            try:
                expiry_date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                live_text(f"   🚨 Error: Invalid date format in CSV!")
                return

            current_time = datetime.now()
            if current_time > expiry_date:
                live_text(f"    ⏳ Your access has expired! Please contact the developer for more time.")
                live_text(f"    📩 Contact: https://t.me/Vortexcodez")
                webbrowser.open("https://t.me/Vortexcodez")
                exit()
            else:
                remaining_time = expiry_date - current_time
                live_text(f"    ✅ Your access is valid. Time remaining: {remaining_time}")
            return

    if all_users_allowed and expiry_date:
        current_time = datetime.now()
        if current_time > expiry_date:
            live_text(f"     ⏳ Your free time is over! Please contact the developer for more time.")
            webbrowser.open("https://t.me/Vortexcodez")
            exit()
        else:
            remaining_time = expiry_date - current_time
            live_text(f"    ✅ Free access is valid. Time remaining: {remaining_time}")
        return

    if not user_found:
        live_text(f"    🚫 You are not authorized! Please contact the developer.")
        live_text(f"    📩 Contact: https://t.me/Vortexcodez")
        webbrowser.open("https://t.me/Vortexcodez")
        exit()

csv_content = fetch_csv(CSV_URL)
if csv_content:
    check_expiry(USER_ID, csv_content)
