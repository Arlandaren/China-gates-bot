from bs4 import BeautifulSoup

# Открытие и чтение HTML страницы из файла
with open('data\\2024-07-11_09.html', 'r') as file:
    html_content = file.read()

# Парсинг HTML страницы с помощью BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')


slots = soup.find_all("div", class_="time-block-item py-2 px-2 d-flex flex-column align-items-center rounded-1")
# print(slots)
count = 0
for slot in slots:
    count +=1
    time_slot = slot.text.split("Д")
    hint = slot.find(class_="hint")

    hint_text = hint.text.strip()
    print(f"{time_slot[0]} ||| {hint_text}")
    hint_count = hint_text.split(":")[1].strip()
    print(hint_count)
    if int(hint_count) > 0:
        print(f"{time_slot} ДОСТУПЕН")

print(count)
