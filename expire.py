import requests
import csv
import webbrowser
from datetime import datetime

CSV_URL = "https://raw.githubusercontent.com/jaikshaikh/Vortexcodes/refs/heads/main/expiry_list.csv"
USER_ID = str(ID)  # Replace ID with actual variable or input

def fetch_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        print("\033[91m🚨 Error fetching CSV:\033[0m", e)
        return None

def check_expiry(user_id, csv_data):
    reader = csv.reader(csv_data.splitlines())
    next(reader)  # Skip header

    all_users_allowed = False
    user_found = False

    for row in reader:
        if row[0].lower() == "all":
            all_users_allowed = True
            break
        elif row[0] == user_id:
            user_found = True
            expiry_date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()

            if current_time > expiry_date:
                print("\033[91m❌ The code has expired. ❌\033[0m")
                print("\033[93m📩 Contact the owner:\033[0m https://t.me/Vortexcodez")
                webbrowser.open("https://t.me/Vortexcodez")
                exit()
            else:
                remaining_time = expiry_date - current_time
                print(f"\033[92m✅ The code is still valid. Time remaining: {remaining_time}\033[0m")
                return

    if all_users_allowed:
        print("\033[92m✅ Access granted to all users.\033[0m")
        return

    if not user_found:
        print("\033[91m⚠️ User ID not found in database. Exiting...\033[0m")
        exit()

csv_content = fetch_csv(CSV_URL)
if csv_content:
    check_expiry(USER_ID, csv_content)
