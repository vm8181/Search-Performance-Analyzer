import pandas as pd
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service


# Set up the Chrome driver and go to the Amazon search page
driver_path = r"E:\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.flipkart.com")

# Find the search box and enter the keyword "go desi"
search_box = driver.find_element(By.XPATH, "//input[contains(@title, 'Search for Products, Brands and More')]")
search_box.send_keys("oil")
time.sleep(1)
search_box.submit() 
find = driver.find_element(By.XPATH, "//button[@type = 'submit']")
find.click
time.sleep(1)
print('starting wait...')
# Wait for the search results to load and extract the HTML content
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'slAVV4']")))
print('wait end...')
html_content = driver.page_source

# Parse the HTML content using etree
dom = etree.HTML(html_content)

# Extract the product names and ASINs using XPath
product_names = dom.xpath('//div[@data-component-type="s-search-result"]//span[@class = "a-size-base-plus a-color-base a-text-normal"]/text()')\
                or dom.xpath('//div[@data-component-type="s-search-result"]//span[@class = ""]/text()')
asins = dom.xpath('//div[contains(@class, "s-result-item s-asin")]//@data-asin')
print(product_names)
print(asins)
# Ensure product_names and asins have the same length
min_length = min(len(product_names), len(asins))
product_names = product_names[:min_length]
asins = asins[:min_length]

# Store the data into a Pandas DataFrame
data = {"Product Name": product_names, "ASIN": asins}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("Brand_products.xlsx", index=False)

# Close the driver
driver.quit()
