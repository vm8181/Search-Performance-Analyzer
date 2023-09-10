from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from lxml import etree
import pandas as pd
import datetime
import time
import sqlalchemy as sa
from sqlalchemy.types import NVARCHAR
import pyodbc
import urllib
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import re


def database_push(data_frame, table_name):
    server = 'DESKTOP-R5K275N\SQLEXPRESS'
    database = 'Yogabar'
    params = urllib.parse.quote_plus('Driver={SQL Server};SERVER='+server+';DATABASE='+database)
    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=False)
    data_frame.to_sql(f'{table_name}', con=engine, index=False, if_exists='append', chunksize=5000,
                      dtype={col_name: NVARCHAR(length=1500) for col_name in data_frame})

    return 'successfully data pushed'


# List of categories and their corresponding links
df = pd.read_excel('Master File.xlsx', 'bsr_link')
category = df['category']
link = df['link']
# Create an empty list to store the data
data = []

# Set up the webdriver
driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe")
driver.maximize_window()

# Loop through each category and its link
for category, link in zip(category, link):
    for page in range(2):
        
        # Navigate to the category page
        c_link = str(link)+'/ref=zg_bs_pg_2?ie=UTF8&pg='+str(page+1)
        driver.get(c_link)
        time.sleep(2)

        # Scroll to the bottom of the page using JavaScript
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(3)
        dom = etree.HTML(driver.page_source)

        # Extract the BSR information using XPath
        products = dom.xpath('//div[@class="p13n-gridRow _cDEzb_grid-row_3Cywl"]//div[contains(@id, "p13n-asin")]')
        for index, product in enumerate(products, start=1):
            
            # Extract product details
            asin = product.xpath('.//div[contains(@class, "zg-grid-general-faceout")]/div[contains(@class, "p13n-sc-uncoverable-faceout")]/@id')
            asin = ''.join(asin)
            title = product.xpath('.//div[@class="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"]/text() | .//div[@class="_cDEzb_p13n-sc-css-line-clamp-4_2q2cc"]/text() | .//div[@class="_cDEzb_p13n-sc-css-line-clamp-5_2l-dX"]/text()')
            title = ''.join(title).strip()
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            prod_url = "https://www.amazon.in/dp/"+str(asin)
            rank = product.xpath('.//span[@class = "zg-bdg-text"]/text()')
            rank = ''.join(rank).replace('#', '')
            img_elements = dom.xpath('(//div[@class="p13n-gridRow _cDEzb_grid-row_3Cywl"]//div[contains(@id, "p13n-asin")])['+ str(index) +']//img//@src')
            try:
                img = img_elements[0]
            except:
                img = ""
##            img_urls = [driver.find_element(By.XPATH, '.' + img_element.getroottree().getpath(img_element)).get_attribute('src') for img_element in img_elements]
##            img = img_urls[0] if img_urls else ""

            
##            print("Category:", category)
##            print("rank", rank)
##            print("Title:", title)
##            print("ASIN:", asin)
##            print("url:", prod_url)
            

            # Add the data to the list
            result = {
                'date': date,
                'last_node': category,
                'title': title,
                'asin': asin,
                'url': prod_url,
                'rank': rank,
                'cat_link': link,
                'prod_img': img
                }
            data.append(result)
            print(result)

# Close the webdriver
driver.quit()

# Create a dataframe from the data list
df = pd.DataFrame(data)

# Save the dataframe to an Excel file
filename = 'amazon_bsr_data.xlsx'
df.to_excel(filename, index=False)
database_push(df,'Shelf')
