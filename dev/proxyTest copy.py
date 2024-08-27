import requests

def check_proxy(proxy_url):
    try:
        response = requests.get('https://jwt.io/', proxies={'http': proxy_url, 'https': proxy_url}, timeout=10)
        print(response.status_code)
        if response.status_code == 200:
            print('Прокси работает!')
        else:
            print('Прокси не работает!')
    except requests.RequestException as e:
        print(f'Прокси не работает: {e}')

proxy = "http://luyr9j:VgFbEPmLQp@[2a0e:cd41:a761:10b5:2eab:25ff:fe7b:8c83]:6787"
check_proxy(proxy)
