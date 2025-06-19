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

##driver.get("https://www.amazon.in/")
##time.sleep(2)
# Find the search box and enter the keyword "go desi"
##search_box = driver.find_element(By.XPATH, "//input[contains(@id,  'twotabsearchtextbox')]")
##search_box.send_keys("beardhood")
##time.sleep(1)
##search_box.submit() 
##find = driver.find_element(By.XPATH, "//input[@id = 'nav-search-submit-button']")
##find.click
##time.sleep(1)
keywords = 'beardhood'
data = []
# Wait for the search results to load and extract the HTML content
##wait = WebDriverWait(driver, 10)
##wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")))
##html_content = driver.page_source
##for keyword in keywords:   
for page in range(1,2):
    p_url = 'https://www.amazon.in/s?k='+str(keywords)##+'&page='+str(page)
    driver.get(p_url)
    time.sleep(2)
    # Parse the HTML content using etree
    dom = etree.HTML(driver.page_source)
    prod_list = dom.xpath("//div[@data-component-type='s-search-result']")
    prod_len = len(prod_list)
    for i in range (0, prod_len):
# Extract the product names and ASINs using XPath
        product_names = dom.xpath('//div[@data-component-type="s-search-result"]//span[@class = "a-size-base-plus a-color-base a-text-normal"]/text()')\
            or dom.xpath('//div[@data-component-type="s-search-result"]//span[@class = ""]/text()') 
        asins = dom.xpath('//div[@data-component-type="s-search-result"]//@data-asin')
        dat = {
            'product_names': product_names,
            'asins': asins,
            }
        data.append(dat)
        print(dat)

driver.quit()

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("Brand_products.xlsx", index=False)

# Close the driver

