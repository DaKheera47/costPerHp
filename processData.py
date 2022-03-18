import json
import statistics
from rich import print
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


REFRESH_DATA = False

with open("./data.json", "r") as f:
    data = json.load(f)

# print(data)
collectedData = []
if REFRESH_DATA:
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    for info in data:
        driver.get(info["link"])

        collectedPrices = []
        i = 0
        while True:
            i += 1
            try:
                delay = 10  # seconds
                time.sleep(delay)
                try:
                    nextButton = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'next_page')))
                except TimeoutException:
                    print("Loading took too much time!")
                    break

                if nextButton:
                    costsFound = driver.find_elements_by_class_name(
                        "price-details")
                    print(f"Page {i}. {len(costsFound)} cars")
                    for cost in costsFound:
                        collectedPrices.append(cost.text)

                    # next button
                    nextButton.click()
                else:
                    costsFound = driver.find_elements_by_class_name(
                        "price-details")
                    print(f"Page {i}. {len(costsFound)} cars")
                    for cost in costsFound:
                        collectedPrices.append(cost.text)
                    break

            except StaleElementReferenceException:
                pass

            except ElementClickInterceptedException:
                print("GOT ONE!")
                driver.refresh()

        prices = []
        for i, price in enumerate(collectedPrices):
            if price != "Call" or price != "":
                try:
                    price = float(re.findall(
                        r"[-+]?(?:\d*\.\d+|\d+)", price)[0])
                    prices.append(price)
                except IndexError:
                    pass

        output = {
            "link": info["link"],
            "hp": info["hp"],
            "title": info["title"],
            "prices": prices,
        }
        collectedData.append(output)
        print(output)


    with open("./data.json", "a") as f:
        json.dump(collectedData, f)
    driver.close()

for info in collectedData if collectedData else data:
    avg = round(statistics.mean(info["prices"]), 2)
    cost = avg * 100000

    print(f"{info['title']}")
    print(f"{info['hp']}")
    print(f"Average Cost is Rs. {avg}lacs from {len(info['prices'])} searches")
    print(f"Rs. {round(cost / info['hp'])} / HP")
    print(f"{info['hp'] / cost} HP / rupee")
    print("")
