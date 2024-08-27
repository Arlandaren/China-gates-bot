import requests
from bs4 import BeautifulSoup
import hashlib
import base64
import os

def generate_code_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode('utf-8')

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"
}

session = requests.Session()

url = f"https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?client_id=account&redirect_uri=https%3A%2F%2Fsrv-gg.ru%2Fbooking&state=409585bf-012a-4eb5-a3b3-e107dd96668b&response_mode=fragment&response_type=code&scope=openid&nonce=9fcd5b02-4d85-4530-8c68-595757c9622b&code_challenge={code_challenge}&code_challenge_method=S256"

r = session.get(url, headers=headers)

cookies = r.cookies.get_dict()

cookie_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])

headers["Cookie"] = cookie_str
headers["Referer"] = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?"



response = session.get(url, headers=headers)

# soup = BeautifulSoup(response.text, 'html.parser')

print(response.text)

# form = soup.find(id="kc-form-login")

# login_url = form.get("action")


# form_data = {}
# form_data['username'] = 'cbolotova@yandex.ru'
# form_data['password'] = 'Bilya2003@'

# post_url = form.get('action')
# session_cookies = "; ".join([f"{key}={value}" for key, value in session.cookies.items()])
# login_headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Cache-Control": "max-age=0",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
#     "Cookie": session_cookies,
# }

# req = requests.Request('POST', post_url, data=form_data, headers=login_headers)
# prepared_login_req = session.prepare_request(req)

# login_response = session.send(prepared_login_req)

# if login_response.status_code != 200:
#     print(f"Ошибка авторизации: {login_response.status_code}")
#     exit()

# redirect_url = login_response.url
# if "code=" not in redirect_url:
#     print("Код авторизации не найден в URL перенаправления.")
#     exit()

# code = redirect_url.split("code=")[-1]

# token_url = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/token"

# token_data = {
#     'grant_type': 'authorization_code',
#     'client_id': 'account',
#     'code': code,
#     'redirect_uri': 'https://srv-gg.ru/booking',
#     'code_verifier': code_verifier  
# }

# session_cookies = "; ".join([f"{key}={value}" for key, value in session.cookies.items()])
# token_headers = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "ru,en;q=0.9",
#     "Content-Length": "321",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Cookie": session_cookies,
#     "Origin": "https://srv-gg.ru",
#     "Priority": "u=1, i",
#     "Referer": "https://srv-gg.ru/booking",
#     "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"YaBrowser\";v=\"24.6\", \"Not-A.Brand\";v=\"99\", \"Yowser\";v=\"2.5\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"Windows\"",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"
# }

# req = requests.Request('POST', token_url, data=token_data, headers=token_headers)
# prepared_req = session.prepare_request(req)

# token_response = session.send(prepared_req)

# if token_response.status_code != 200:
#     print(f"Ошибка получения токена: {token_response.text}")
#     exit()

# access_token = token_response.json().get('access_token')

# if access_token:
#     print(f"Токен доступа получен!")
# else:
#     print("Ошибка получения токена доступа.")

# session_cookies = "; ".join([f"{key}={value}" for key, value in session.cookies.items()])

# protected_url = "https://srv-gg.ru/api/booking_slots"
# headers = {
#     'Authorization': f'Bearer {access_token}',
#     "Cookie": session_cookies,
#     "Content-Type": "application/json"
# }

# payload_mappId = {
#     "mappId": "2e6dafae-8d48-4176-8cdf-cfaf79627c75"
# }
# import time
# for i in range(100):
#     protected_response = session.post(protected_url, json=payload_mappId,headers=headers)

#     if protected_response.status_code == 200:
#         with open(f"date({i}).json", "w") as file:
#             file.write(protected_response.text)
#     else:
#         print(f"Ошибка доступа: {protected_response.text}")
#     time.sleep(15)


