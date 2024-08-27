from seleniumwire import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

# configure the proxy
proxy_address = "2a0e:cd41:a761:10b5:2eab:25ff:fe7b:8c83"
proxy_port = "6787"  # Используем один и тот же порт для HTTP и HTTPS
proxy_username = "luyr9j"
proxy_password = "VgFbEPmLQp"

# formulate the proxy url with authentication
proxy_url = f"http://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}"
print(proxy_url)
# set selenium-wire options to use the proxy
seleniumwire_options = {
    "proxy": {
        "http": proxy_url,
        "https": proxy_url
    },
}

# set Chrome options to run in headless mode
options = Options()
# options.add_argument("--headless")
edge_service = Service('C:\\Apps\\App\\edgedriver_win64\\msedgedriver.exe')
# initialize the Chrome driver with service, selenium-wire options, and chrome options
driver = webdriver.Edge(
    service=edge_service,
    seleniumwire_options=seleniumwire_options,
    options=options
)

# navigate to the target webpage
driver.get("https://httpbin.io/ip")

# print the body content of the target webpage
print(driver.find_element(By.TAG_NAME, "body").text)

# release the resources and close the browser
driver.quit()
