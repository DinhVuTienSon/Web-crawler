from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
from selenium.webdriver.chrome.options import Options
import requests
import json

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
url = 'https://masothue.com/'
browser.get(url)

# sleep(5)
# def getUrl():
all_profile_url = []
page_src = BeautifulSoup(browser.page_source, 'html.parser')
section = page_src.find('section', class_='tax-listing')
if section:
    h3_tag = section.find_all('h3')
    profiles = [h3.find('a')['href'] for h3 in h3_tag if h3.find('a')]
    for profile in profiles:
        profile_url = 'https://masothue.com' + profile
        if profile_url not in all_profile_url:
            all_profile_url.append(profile_url)
    # return all_profile_url
    
companies_data = []

for company_url in all_profile_url:
    access = requests.get(company_url)
    if access.status_code == 200:
        soup = BeautifulSoup(access.content, 'html.parser')
        table = soup.find('table', class_='table-taxinfo')
        rows = table.find_all("tr")

        # Extract text row by row   
        all_text = []
        data = {}
        for row in rows:
            cells = row.find_all(["td", "th"])
                
            cells = row.find_all(["td", "th"])
            if len(cells) == 1:  # Row spans multiple columns
                all_text.append(" ".join(cell.get_text(strip=False) for cell in cells).replace('\n', ''))
                # print(all_text)
            else:  # Normal row
                all_text.append(": ".join(cell.get_text(strip=True) for cell in cells).replace('Ẩn thông tin', ''))
        # print("\n".join(all_text))
    
    companies_data.append(all_text)    
        
with open("company_info.json", "w", encoding="utf-8") as json_file:
    json.dump(companies_data, json_file, ensure_ascii=False, indent=4)
            
print('data saved')

# sleep(10)
browser.close()