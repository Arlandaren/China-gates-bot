from bs4 import BeautifulSoup

with open('data\\2024-07-09_05.html', 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

date = soup.find("div", class_="react-datepicker__day react-datepicker__day--010 react-datepicker__day--keyboard-selected")

# print(slots)

# count = 0
print(date.text)
# print(date.get_attribute_list("aria-label")[0].split(" ")[0])

# print(count)
