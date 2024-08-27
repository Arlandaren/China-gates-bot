import time,requests,json
from fake_useragent import UserAgent
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import parse

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

def send(body,user_data):
    token,ua,cookies = auth(user_data["username"],user_data["password"])
    
    headers = {
        "Authorization": "Bearer " + token,
        "User-Agent": ua,
        "Cookie": cookies,
        "Referer": "https://srv-gg.ru/booking-process"
    }
    
    resp = requests.post(url="https://srv-gg.ru/api/bookings",json=body,headers=headers)
    # resp = requests.get(url="https://srv-gg.ru/api/captcha",headers=headers)

    print(resp.text)


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
    body = {
        "load_type": "loaded",
        "transportation_type": "transit",
        "driver": {
            "email": "batom***mail.ru",
            "phone": "+79141248157"
        },
        "car": {
            "1": {
                "id": "9c7fc202-52d7-4e85-b573-9f42c48b0fbb",
                "type_name": "Truck",
                "name": "FREIGHTLINER",
                "model": "FLC120",
                "grnz": "O498BX75",
                "file_uuid": "d7dc11c6-1605-4332-9490-4b4c3f49da2b"
            },
            "2": {
                "id": "1a2e16e0-47cb-47f9-ba8a-e905c708845d",
                "type_name": "Trailer",
                "grnz": "AE069775",
                "file_uuid": "01e1bb33-fb96-41f6-ab4b-3994ed0e461b"
            }
        },
        "time_slot": "2024-09-05T08:00:00Z",
        "bph": 13,
        "mapp_id": "2e6dafae-8d48-4176-8cdf-cfaf79627c75",
        "lang": "RU",
        "is_kiosk": False,
        "captcha_id": "7EjGCFK6MaJ40tN932oD",
        "captcha_input": "273041"
    }
    send(body,user_data)

