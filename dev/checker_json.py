import time,requests,uuid
from fake_useragent import UserAgent
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime

def auth():
    username = "cbolotova@yandex.ru"
    password = "Bilya2003@"

    options = Options()
    ua = UserAgent().random
    options.add_argument(f"--user-agent={ua}")
    options.add_argument("--disable-logging")
    options.add_argument("--headless") 
    service = Service('C:\\Apps\\App\\edgedriver_win64\\msedgedriver.exe')

    url = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?client_id=account&redirect_uri=https%3A%2F%2Fsrv-gg.ru%2Fbooking&code_challenge_method=S256"

    with Edge(service=service, options=options) as driver:
        driver.get(url)

        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
        login.clear()
        login.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys("\n")
        time.sleep(1)
        cookies = driver.get_cookies()
        
        cookies = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        seq_kk_token = driver.execute_script("""var token = localStorage.getItem('seq_kk_token');return token;""")
        
        return seq_kk_token,ua,cookies
    
def parse_date():
    token,ua,cookies = auth()
    
    headers = {
        "Authorization": "Bearer " + token,
        "User-Agent": ua,
        "Cookie": cookies,
        "Referer": "https://srv-gg.ru/booking-process"
    }
    body = {"mappId": "2e6dafae-8d48-4176-8cdf-cfaf79627c75"}
    
    # file_path = f"data/date_{uuid.uuid4()}.json"
    file_name = f"12count_dates.json"

    for i in range(400000000):
        resp = requests.post("https://srv-gg.ru/api/booking_slots", json=body,headers=headers)
        try:
            if resp.json().get("error") == "token parse with claims failed":
                token,ua,cookies = auth()
                headers = {
                "Authorization": "Bearer " + token,
                "User-Agent": ua,
                "Cookie": cookies,
                "Referer": "https://srv-gg.ru/booking-process"
                }
                continue
            else:
            #     with open(file_path, 'r', encoding='utf-8') as f:
            #         data = json.load(f)
            # except (FileNotFoundError, json.JSONDecodeError):
            #     data = []
            
            # data.append(resp.json())

            # with open(file_path, 'w', encoding='utf-8') as f:
            #     json.dump(data, f, ensure_ascii=False, indent=4)
            # if len(data) > 400:
            #     file_path = f"data/date_{uuid.uuid4()}.json"
            # time.sleep(1.5)
            # print(i)
                dates = resp.json().get("data")
                # dates = [
                #     {
                #         "time": "2024-07-11T00:00:00Z",
                #         "count": 12,
                #         "bph": 12
                #     },
                #     {
                #         "time": "2024-07-11T01:00:00Z",
                #         "count": 12,
                #         "bph": 12
                #     }
                # ]
                for date in dates:
                    if date["count"] == 12:
                        print(str(date["time"]))
                        date["current_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        try:
                            with open(file_name, "r", encoding="utf-8") as file:
                                data = json.load(file)
                        except (FileNotFoundError, json.JSONDecodeError):
                            data = []

                        if not any(item["time"] == date["time"] and item["count"] == date["count"] for item in data):
                            data.append(date)
                            with open(file_name, "w", encoding="utf-8") as file:
                                json.dump(data, file, ensure_ascii=False, indent=4)
                print(i)
                time.sleep(1.7)
            
        except requests.exceptions.JSONDecodeError:
            continue

if __name__ == "__main__":
    parse_date()

