from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from fake_useragent import UserAgent

def booking(target_date, user_data:dict):
    link = "https://srv-gg.ru/auth/realms/fseq/protocol/openid-connect/auth?client_id=account&redirect_uri=https%3A%2F%2Fsrv-gg.ru%2Fbooking&code_challenge_method=S256"

    username = user_data["username"]
    password = user_data["password"]
    target_truck = user_data["target_truck"]
    target_trunk = user_data["target_trunk"]
    target_mapp = user_data["target_mapp"]

    options = Options()
    ua = UserAgent().random
    options.add_argument(f"--user-agent={ua}")
    options.add_argument("--disable-logging")

    service = Service('C:\\Apps\\App\\edgedriver_win64\\msedgedriver.exe')

    with Edge(service=service,options=options) as driver:
        driver.get(link)

        login_form =  WebDriverWait(driver,10 ).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#username")))
        login_form.clear()
        login_form.send_keys(username)

        password_from = WebDriverWait(driver,10 ).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#password")))
        password_from.clear()
        password_from.send_keys(password)
        password_from.send_keys(Keys.RETURN)

        time.sleep(1)
        
        add_btn = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div:nth-child(1) > div > div > a')))
        add_btn.click()

        time.sleep(1)
        open_truck_btn = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.pb-40px > div:nth-child(1) > div.seq-select-container.menu-static.css-b62m3t-container > div > div.seq-select__indicators.css-1wy0on6 > div.seq-select__indicator.seq-select__dropdown-indicator.css-tlfecz-indicatorContainer")))
        open_truck_btn.click()

        truck_listbox = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".seq-select__menu-list.css-11unzgr")))


        options = truck_listbox.find_elements(By.CSS_SELECTOR, ".seq-select__option")
        for option in options:
            if option.text.strip() == target_truck:
                option.click()
                break
        
        # if target_trunk != "":
        open_trunk_btn = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.pb-40px > div:nth-child(3) > div > div > div.seq-select__indicators.css-1wy0on6 > div")))
        open_trunk_btn.click()

        trunk_listbox = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".seq-select__menu-list.css-11unzgr")))


        options = trunk_listbox.find_elements(By.CSS_SELECTOR, ".seq-select__option")
        for option in options:
            if option.text.strip() == target_trunk:
                option.click()
                break
        
        # TOdo: добавить экспорт
        transportation_type = driver.find_element(By.CSS_SELECTOR,"#default-checkbox1")
        if not transportation_type.is_selected():
            transportation_type.click()

        # to_driver_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.d-flex.justify-content-between > button.d-inline-block.ms-2.btn.btn-seq-primary")
        to_driver_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.d-flex.justify-content-between > button.d-inline-block.ms-2.btn.btn-seq-primary")
        driver.execute_script("arguments[0].click();", to_driver_btn)

        #TOdo: кастомные контактные данные
        # use_profile_driver_checkbox = driver.find_element(By.CSS_SELECTOR, "#default-checkbox3")
        use_profile_driver_checkbox = WebDriverWait(driver,10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#default-checkbox3")))
        if not use_profile_driver_checkbox.is_selected():
            # use_profile_driver_checkbox.click()
            driver.execute_script("arguments[0].click();", use_profile_driver_checkbox)

        to_mapp_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.d-flex.justify-content-center > button")
        driver.execute_script("arguments[0].click();", to_mapp_btn)

        open_mapp_btn = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.pb-40px > div > div > div > div.seq-select__indicators.css-1wy0on6 > div")))
        open_mapp_btn.click()
        # driver.execute_script("arguments[0].click();", open_mapp_btn)

        mapp_listbox = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".seq-select__menu-list.css-11unzgr")))
        
        options = mapp_listbox.find_elements(By.CSS_SELECTOR, ".seq-select__option")

        for option in options:
            if option.text.strip() == target_mapp:
                # option.click()
                driver.execute_script("arguments[0].click();", option)
                break
        
        to_instruction_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.d-flex.justify-content-center > button")
        # to_instruction_btn.click()
        driver.execute_script("arguments[0].click();", to_instruction_btn)

        accept_checkbox = driver.find_element(By.CSS_SELECTOR,"#informed")
        if not accept_checkbox.is_selected():
            # accept_checkbox.click()
            driver.execute_script("arguments[0].click();", accept_checkbox)

        to_date_btn = driver.find_element(By.CSS_SELECTOR,"#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > div.d-flex.align-items-center.justify-content-center > button")
        # to_date_btn.click()
        driver.execute_script("arguments[0].click();", to_date_btn)

        # date_obj = datetime.fromisoformat(target_date[:-1])
        # target_day = date_obj.day
        # target_month = date_obj.strftime("%B")
        # target_year = date_obj.year

        weeks = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "react-datepicker__week")))
        with open(f"data/{target_date.split("T")[0]}_{target_date.split("T")[1].split(":")[0]}.html", "w") as file:
            file.write(driver.page_source)

        for week in weeks:
            days = week.find_elements(By.CLASS_NAME, "react-datepicker__day.react-datepicker__day--010.react-datepicker__day--keyboard-selected")
            print(days)
            for day in days:
                print(day.get_attribute("innerHTML"))
                if day.get_attribute("aria-label").split(" ")[0] == "Choose":
                    print("Выбран")
                    day.click()
                    driver.execute_script("arguments[0].click();", day)
                else:
                    print("Занят")


        time.sleep(1000)


        slots = WebDriverWait(driver,10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,"time-block-item.py-2.px-2.d-flex.flex-column.align-items-center.rounded-1")))
        book_btn = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.bg-body.d-flex.flex-column.header-offset.px-1 > div > div > div > div > button")))
    
        for slot in slots:
            time_slot = slot.text.split("Д")
            hint = slot.find_element(By.CLASS_NAME,"hint")
            print(f"{time_slot[0]} ||| {hint.text}")
            hint_count = hint.text.strip().split(":")[1]
            if int(hint_count) > 0:
                print(print(f"{time_slot} ДОСТУПЕН"))
                book_btn.click()

        # with open(f"data/{target_date.split("T")[0]}_{target_date.split("T")[1].split(":")[0]}.html", "w") as file:
        #     file.write(driver.page_source)

        time.sleep(100000000)

if __name__ == "__main__":
    user_data = {
        "username": "cbolotova@yandex.ru",
        "password": "Bilya2003@",
        "target_truck": "VOLVOFH VOLVOFH H818HY75",
        "target_trunk": "AM999875",
        "target_mapp": "МАПП Забайкальск"
    }
    # user_data = {
    #     "username": "larisa.tsyrenowa@yandex.ru",
    #     "password": "1tW&uZez3hqG",
    #     "target_truck": "Freightliner Freightliner O415BX75",
    #     "target_trunk": "",
    #     "target_mapp": "МАПП Забайкальск"
    # }
    booking("2024-07-11T20:00:00Z", user_data)