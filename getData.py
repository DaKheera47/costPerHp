from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import time
import re
import statistics

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# driver.get(
#     "https://www.pakwheels.com/used-cars/search/-/mk_toyota/yr_2005_2008/md_passo/")
# driver.get(
#     "https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/vr_altis-1-6-automatic/yr_2016_2016/")
# driver.get(
#     "https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/vr_xli-vvti/yr_2009_2009/")
# driver.get("https://www.pakwheels.com/used-cars/kia-sportage-awd-islamabad/415087")
# driver.get("https://www.pakwheels.com/used-cars/kia-sportage-awd-karachi/417298")
# driver.get("https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/vr_altis-1-8-grande-automatic/yr_2020_2021/ct_islamabad/ct_rawalpindi/")
driver.get("https://www.pakwheels.com/used-cars/search/-/mk_honda/md_civic/ct_islamabad/ct_rawalpindi/tr_manual/yr_2013_2017/")
print(driver.title)
collectedPrices = []

i = 0
while True:
    i += 1
    try:
        time.sleep(10)
        nextButton = driver.find_elements_by_class_name("next_page")

        if nextButton:
            costsFound = driver.find_elements_by_class_name("price-details")
            print(f"Page {i}. {len(costsFound)} cars")
            for cost in costsFound:
                collectedPrices.append(cost.text)

            # next button
            nextButton[0].click()
        else:
            costsFound = driver.find_elements_by_class_name("price-details")
            print(f"Page {i}. {len(costsFound)} cars")
            for cost in costsFound:
                collectedPrices.append(cost.text)

            break

    except StaleElementReferenceException:
        pass

    except ElementClickInterceptedException:
        print("GOT ONE!")
        driver.refresh()
        time.sleep(10)
        # el = driver.find_element_by_class_name("close").click()
        # print(el)

print()
print(f"{len(collectedPrices)} cars found!")
prices = []
for i, price in enumerate(collectedPrices):
    if price != "Call" or price != "":
        try:
            price = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", price)[0])
            prices.append(price)
        except IndexError:
            pass

print("\n")
print(prices)
print("\n")

avg = round(statistics.mean(prices), 2)
cost = avg * 100000
print(f"Rs. {avg}lacs")

driver.close()
