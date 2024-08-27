import time,requests,json
import time
from seleniumwire import webdriver  # Используем Selenium Wire вместо обычного Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from fake_useragent import UserAgent  # Для генерации случайного User-Agent

import parse

def auth(username: str, password: str):
    proxy_host = "45.89.18.233"
    proxy_port = "6787"  # Используем один и тот же порт для HTTP и HTTPS
    proxy_username = "luyr9j"
    proxy_password = "VgFbEPmLQp"
    proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
    proxy_options = {
        'proxy': {
            'http': proxy_url,
            'https': proxy_url,
        }
    }
    
    edge_options = Options()
    ua = UserAgent().random  # Случайный User-Agent
    edge_options.add_argument(f"--user-agent={ua}")
    edge_options.add_argument("--disable-logging")

    edge_service = Service('C:\\Apps\\App\\edgedriver_win64\\msedgedriver.exe')

    url = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?client_id=account&redirect_uri=https%3A%2F%2Fsrv-gg.ru%2Fbooking&code_challenge_method=S256"

    with webdriver.Edge(service=edge_service, options=edge_options, seleniumwire_options=proxy_options) as driver:
        driver.get(url)

        # Аутентификация
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
        login.clear()
        login.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys("\n")

        time.sleep(0.5)  # Небольшая задержка, чтобы страница успела загрузиться

        # Получение cookies и токена
        cookies = driver.get_cookies()
        cookies = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        seq_kk_token = driver.execute_script("""return localStorage.getItem('seq_kk_token');""")
        
        return seq_kk_token, ua, cookies
    
def check_date(user_data):
    token,ua,cookies = auth(user_data["username"],user_data["password"])
    
    headers = {
        "Authorization": "Bearer " + token,
        "User-Agent": ua,
        "Cookie": cookies,
        "Referer": "https://srv-gg.ru/booking-process"
    }

    body = {"mappId": "2e6dafae-8d48-4176-8cdf-cfaf79627c75"}

    file_name = "data/dates.json"
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
            # elif resp.json().get("data") != None:
            else:
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
                    if date["count"] != 0:
                        print(str(date["time"]), date["count"])
                        parse.booking(str(date["time"]),user_data)
                        time.sleep(100000)
                        try:
                            with open(file_name, "r", encoding="utf-8") as file:
                                data = json.load()
                        except (FileNotFoundError, json.JSONDecodeError):
                            data = []
                        if not any(item["time"] == date["time"] and item["count"] == date["count"] for item in data):
                            data.append(date)
                            with open(file_name, "w") as file:
                                json.dump(data,file,ensure_ascii=False, indent=4)
                
            # else:
                # print(resp.text)
            print(i)
            time.sleep(1.7)

        except requests.exceptions.JSONDecodeError as e:
            print(resp.text)
            print(resp.json())
            print("Ошибка:", e)
            # continue


if __name__ == "__main__":
    # user_data = {
    #     "username": "cbolotova@yandex.ru",
    #     "password": "Bilya2003@",
    #     "target_truck": "VOLVOFH VOLVOFH H818HY75",
    #     "target_trunk": "AM999875",
    #     "target_mapp": "МАПП Забайкальск"
    # }
    user_data = {
        "username": "larisa.tsyrenowa@yandex.ru",
        "password": "1tW&uZez3hqG",
        "target_truck": "Freightliner Freightliner O415BX75",
        "target_trunk": "",
        "target_mapp": "МАПП Забайкальск"
    }
    check_date(user_data)

