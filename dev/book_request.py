import time,requests,json
from fake_useragent import UserAgent
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import parse
from captcha import solve_captcha

body = {
        "load_type": "loaded",
        "transportation_type": "transit",
        "driver": {
            "email": "",
            "phone": ""
        },
        "car": {
            "1": {
                "id": "",
                "type_name": "Truck",
                "name": "",
                "model": "",
                "grnz": "",
                "file_uuid": ""
            },
            "2": {
                "id": "",
                "type_name": "Trailer",
                "grnz": "",
                "file_uuid": ""
            }
        },
        "time_slot": "",
        "bph": int,
        "mapp_id": "2e6dafae-8d48-4176-8cdf-cfaf79627c75",
        "lang": "RU",
        "is_kiosk": False,
        "captcha_id": "",
        "captcha_input": ""
    }

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

def get_captcha_by_rucaptcha(headers):
    resp = requests.get(url="https://srv-gg.ru/api/captcha",headers=headers)
    result = solve_captcha(resp.json().get("captcha"))

    captcha = resp.json()
    captcha["result"] = result["code"]

    return captcha

def get_captcha_from_storage():
    with open("data/captchas.json", "r", encoding="utf-8") as file:
        captchas = json.load(file)
    captcha = captchas[0]
    with open("data/captchas.json", "w") as file:
        json.dump(captchas[1:],file,ensure_ascii=False,indent=4)
    return captcha

def formate_body(target_truck,target_trunk,driver,date,captcha):
    book_body = body
    book_body["car"]["1"]["id"] = target_truck.get("car_id", "")
    book_body["car"]["1"]["name"] = target_truck.get("name", "")
    book_body["car"]["1"]["model"] = target_truck.get("model", "")
    book_body["car"]["1"]["grnz"] = target_truck.get("grnz", "")
    book_body["car"]["1"]["file_uuid"] = target_truck.get("document_uuid", "")

    book_body["car"]["2"]["id"] = target_trunk.get("car_id", "")
    book_body["car"]["2"]["grnz"] = target_trunk.get("grnz", "")
    book_body["car"]["2"]["file_uuid"] = target_trunk.get("document_uuid", "")

    book_body["driver"]["email"] = driver["email"]
    book_body["driver"]["phone"] = driver["phone"]

    book_body["time_slot"] = date["time"]  
    book_body["bph"] = date["bph"]  

    
    book_body["captcha_id"] = captcha["captcha_id"] 
    book_body["captcha_input"] = captcha["result"]

    return book_body

def get_car(grnz,headers,url):
    cars_resp = requests.get(url,headers=headers)
    if cars_resp.status_code == 200:
        cars = cars_resp.json().get("data")
        for car in cars:
            if car.get("grnz") == grnz:
                return car
    else:
        raise Exception("не удалось получить список машин")
    
    raise Exception("Не найдена машина")

def send(user_data,date,request_headers):

    target_truck = get_car(user_data["target_truck"],request_headers,url="https://srv-gg.ru/api/cars?page=1&limit=100&car_type=1&is_booking_available=true&validation_statuses=2")
    target_trunk = get_car(user_data["target_trunk"],request_headers,url="https://srv-gg.ru/api/cars?page=1&limit=100&car_type=2&is_booking_available=true&validation_statuses=2")
    # captcha = get_captcha(request_headers)
    captcha = get_captcha_from_storage()
    request_body = formate_body(target_truck,target_trunk,driver=user_data["driver"],date=date,captcha=captcha)
    
    print(request_body)
    print(captcha)
    resp = requests.post(url="https://srv-gg.ru/api/bookings",json=request_body,headers=request_headers)


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
        "target_truck": "O481EB75",
        "target_trunk": "AB381003",
        "driver":{
            "email": "larisa.tsyrenowa@yandex.ru",
            "phone": "89145045696"
        }
    }
    date = {
            "time": "2024-07-05T11:00:00Z",
            "count": 0,
            "bph": 12
    }

    token,ua,cookies = auth(user_data["username"],user_data["password"])
    
    request_headers = {
        "Authorization": "Bearer " + token,
        "User-Agent": ua,
        "Cookie": cookies,
        "Referer": "https://srv-gg.ru/booking-process"
    }

    send(user_data,date,request_headers)

