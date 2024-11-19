from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import csv
from selenium.webdriver.chrome.options import Options
import requests
import json

# Code can only run on Linkedin English version (due to the difference in the UI)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.linkedin.com/checkpoint/lg/sign-in-another-account'
browser.get(url)

# username = input('Enter username: ')
# password = input('Enter password: ')

username = 'testscrape@gmail.com'
password = '123asd.'

email_field = browser.find_element(By.ID, 'username')
email_field.send_keys(username)
password_field = browser.find_element(By.ID, 'password')
password_field.send_keys(password)

sleep(2)
password_field.send_keys(Keys.ENTER)

sleep(15)

# search = input('Enter the data you need to scrape: ')
search = 'technology company'

search_field = browser.find_element(By.CLASS_NAME, 'search-global-typeahead__input.search-global-typeahead__input--ellipsis')
search_field.send_keys(search)
search_field.send_keys(Keys.ENTER)
sleep(5)
# print(browser.page_source)

search_btns = browser.find_element(By.XPATH, "//*[@id='search-reusables__filters-bar']/ul/li[6]/button")
search_btns.click()

sleep(5)

def getUrl():
    all_company_url = []

    search_page_src = BeautifulSoup(browser.page_source, 'html.parser')
    # print(search_page_src)
    # with open("output.txt", "w", encoding="utf-8") as file:
    #     file.write(str(search_page_src))

    ul_tag = search_page_src.find_all('a', class_= "app-aware-link scale-down")
    # print(ul_tag)

    for tag in ul_tag:
        src = tag.get('href')
        all_company_url.append(src)
    return all_company_url

url_all_page = []

# no_page = input('Enter the number of pages you want to scrape: ')
no_page = 1
for page in range(no_page):
    url_1_page = getUrl()
    sleep(2)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)
    next_btn = browser.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
    next_btn.click()
    url_all_page = url_all_page + url_1_page
    sleep(2)

# print(url_all_page)
all_company_data = []
for company_url in url_all_page:
    # access = requests.get(company_url)
    # if access.status_code == 200:
    #     company_page = BeautifulSoup(access.content, 'html.parser')
    browser.get(company_url)
    sleep(3)
    company_page = BeautifulSoup(browser.page_source, 'html.parser')

    main_div = company_page.find('div', class_='block mt4')
    
    company_name = main_div.find('h1').get_text(strip=True) if main_div.find('h1') else None
    tagline = main_div.find('p', class_='org-top-card-summary__tagline').get_text(strip=True) if main_div.find('p', class_='org-top-card-summary__tagline') else None

    info_items = main_div.find_all('div', class_='org-top-card-summary-info-list__info-item')
    info_data = [item.get_text(strip=True) for item in info_items] if info_items else []

    industry = info_data[0] if len(info_data) > 0 else None
    location = info_data[1] if len(info_data) > 1 else None

    employees = (
        main_div.find('a', class_='org-top-card-summary-info-list__info-item-link').get_text(strip=True)
        if main_div.find('a', class_='org-top-card-summary-info-list__info-item-link')
        else None
    )

    company_data = {
        "company_name": company_name,
        "tagline": tagline,
        "industry": info_data[0],
        "location": info_data[1] if len(info_data) > 1 else None,
        "employees": employees,
    }
    all_company_data.append(company_data)

# print(all_company_data)

# Save to a JSON file
with open("company_data.json", "w") as json_file:
    json.dump(all_company_data, json_file, indent=4)

print("Data saved to company_data.json")

# sleep(5)
# browser.close()


