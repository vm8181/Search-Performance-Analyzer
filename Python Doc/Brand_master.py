from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from lxml import etree 
import pandas as pd
import datetime
import time
import re

# Create a list of ASINs
df = pd.read_excel('brand_master inputs.xlsx')
asins = df['SKU'].values

# Create an empty dictionary to store the data
data = []

# Set up the webdriver
driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe")
driver.maximize_window()

# Loop through each ASIN in the list
for asin in asins:
    # Construct the URL for the product page
    url = f'https://www.amazon.in/dp/{asin}'

    # Navigate to the product page
    driver.get(url)
    time.sleep(2)
    dom=etree.HTML(driver.page_source)

    # Extract the data using XPath
    title = dom.xpath('//h1[contains(@id, "title")]/span/text()')
    title = ''.join(title).strip()
    brand = dom.xpath('//tr[@class = "a-spacing-small po-brand"]//span[@class = "a-size-base po-break-word"]/text()')
    brand = ''.join(brand).strip()
##    manufacturer = dom.xpath('//*[@id="productDetails_techSpec_section_1"]/tbody/tr[6]/td/text()')
##    manufacturer = ''.join(manufacturer).strip()
        
    # Add the data to the dictionary
    result = {
        'platform': 'Amazon',
        'platform_code': asin,
        'title': title,
        'brands': brand
##        'manufacturer': manufacturer
        }
    data.append(result)
    print(result)

# Close the webdriver
driver.quit()

# Create a dataframe from the dictionary
df = pd.DataFrame(data)

# Save the dataframe to an Excel file
filename = 'brand_master.xlsx'
df.to_excel(filename, index=False)

print(data)
