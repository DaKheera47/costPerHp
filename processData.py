import json
import statistics
from rich import print
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys
import os
PREFIX = "-"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


try:
    REFRESH_DATA = True if sys.argv[1] == f"{PREFIX}r" else False
except IndexError:
    REFRESH_DATA = False


with open("./data.json", "r") as f:
    data = json.load(f)

finalOutput = []

if REFRESH_DATA:
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.maximize_window()
    for info in data:
        collectedPrices = []
        collectedMileage = []

        i = 1
        newLink = f'{info["link"]}?page={i}'
        driver.get(newLink)

        collectedPrices = []
        while True:
            newLink = f'{info["link"]}?page={i}'
            driver.get(newLink)

            # if end of cars
            if int(driver.current_url.split("=")[1]) < i:
                break

            costsFound = driver.find_elements(by=By.CLASS_NAME, value="price-details")
            mileage = driver.find_elements(by=By.CLASS_NAME, value="search-vehicle-info-2")

            for m in mileage:
                collectedMileage.append(int(m.text.split(" ")[1].replace(",", "")))

            j = 0
            for cost in costsFound:
                cost = cost.text
                if cost != "Call" or cost != "":
                    try:
                        cost = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", cost)[0])
                        collectedPrices.append(cost)
                        j += 1
                    except IndexError:
                        pass

            print(f"Page {i}. {j} cars -- Total: {len(collectedPrices)}")
            i += 1

        # printing
        print(f"{len(collectedPrices)} cars in total")
        print(f"Average price: {statistics.mean(collectedPrices) :.2f}")
        print(f"Average mileage: {statistics.mean(collectedMileage) :.2f}")
        print(f"Max price: {max(collectedPrices)}")
        print(f"Min price: {min(collectedPrices)}")

        output = {
            "title": info["title"],
            "hp": info["hp"],
            "link": info["link"],
            "prices": collectedPrices,
            "mileage": collectedMileage,
            "averagePrice": statistics.mean(collectedPrices),
            "averageMileage": statistics.mean(collectedMileage),
        }

        finalOutput.append(output)

    with open("./data.json", "w") as f:
        json.dump(finalOutput, f)

    driver.close()
