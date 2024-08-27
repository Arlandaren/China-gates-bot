import requests
from bs4 import BeautifulSoup
from verifier import *




def auth(account:dict, session:requests.Session):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    auth_page_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36"
    }
    auth_page_url = f"https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?client_id=account&redirect_uri=https%3A%2F%2Fsrv-gg.ru%2Fbooking&state=409585bf-012a-4eb5-a3b3-e107dd96668b&response_mode=fragment&response_type=code&scope=openid&nonce=9fcd5b02-4d85-4530-8c68-595757c9622b&code_challenge={code_challenge}&code_challenge_method=S256"

    auth_page_response =session.get(auth_page_url, headers=auth_page_headers)

    cookies = auth_page_response.cookies.get_dict()
    cookie_str = "; ".join([f"{key}={value}" for key,value in cookies.items()])

    auth_page_headers["Cookie"] = cookie_str
    auth_page_headers["Referer"] = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?"

    auth_page_response = session.get(auth_page_url, headers=auth_page_headers)

    soup = BeautifulSoup(auth_page_response, "html.parser")
    form = soup.find(id="kc-form-login")
    auth_url = form.get("action")

    session_cookies = "; ".join([f"{key}={value}" for key, value in session.cookies.items()])
    auth_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Cookie": session_cookies,
    }

    auth_response = session.post(auth_url, data=account, headers=auth_headers)

    if auth_response.status_code != 200:
        print(f"Ошибка авторизации: {auth_response.status_code}")
        return auth_response.text
    
    auth_redirect_url = auth_response.url
    
    token_code = auth_redirect_url.split("code=")[-1]

    token_url = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/token"

    token_data = {
        'grant_type': 'authorization_code',
        'client_id': 'account',
        'code': token_code,
        'redirect_uri': 'https://srv-gg.ru/booking',
        'code_verifier': code_verifier  
    }

    session_cookies = "; ".join([f"{key}={value}" for key, value in session.cookies.items()])
    auth_headers["Cookie"] = session_cookies

    token_response = session.post(token_url, data=token_data,headers=auth_headers)

    if token_response.status_code != 200:
        print(f"Ошибка получения токена: {token_response.text}")
        return token_response.text

    access_token = token_response.json().get('access_token')

    if access_token:
        return access_token, session_cookies
    else:
        None
