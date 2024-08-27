import requests
from bs4 import BeautifulSoup

def parse(account:dict):
    session = requests.Session()

    