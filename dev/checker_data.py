import time,requests,json
from fake_useragent import UserAgent
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import parse,book_request

def auth(username:str,password:str):

    options = Options()
    ua = UserAgent().random
    options.add_argument(f"--user-agent={ua}")
    options.add_argument("--disable-logging")
    # options.add_argument("--headless") 
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
        time.sleep(0.5)
        cookies = driver.get_cookies()
        
        cookies = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        seq_kk_token = driver.execute_script("""var token = localStorage.getItem('seq_kk_token');return token;""")
        
        return seq_kk_token,ua,cookies

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
            else:
                
                dates = resp.json().get("data")

                for date in dates:
                    if date["count"] != 0:
                        print(str(date["time"]), date["count"])
                        book_request.send(user_data,date,headers)
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
            
            print(i)
            time.sleep(2)

        except requests.exceptions.JSONDecodeError as e:
            print(resp.text)
            # print(resp.json())
            print("Ошибка:", e)
            break


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
                    "target_truck": "O481EB75",
                    "target_trunk": "AB381003",
                    "driver":{
                        "email": "larisa.tsyrenowa@yandex.ru",
                        "phone": "89145045696"
                    }
                }
    check_date(user_data)

