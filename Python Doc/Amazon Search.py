import pandas as pd
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import sqlalchemy as sa
from sqlalchemy.types import NVARCHAR
import pyodbc
import urllib

def database_push(data_frame, table_name):
    server = 'DESKTOP-R5K275N\SQLEXPRESS'
    database = 'Yogabar'
    params = urllib.parse.quote_plus('Driver={SQL Server};SERVER='+server+';DATABASE='+database)
    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=False)
    data_frame.to_sql(f'{table_name}', con=engine, index=False, if_exists='append', chunksize=5000,
                      dtype={col_name: NVARCHAR(length=1500) for col_name in data_frame})

    return 'successfully data pushed'

# Set up the Chrome driver and go to the Amazon search page
driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe")
driver.get("https://www.amazon.in")

# Read keywords from an input file (Excel file)
keywords_df = pd.read_excel('Master File.xlsx', 'Keywords')
keywords = keywords_df["Keywords"].tolist()

# Create an empty DataFrame to store all the crawled data
data = []

for keyword in keywords:   
    for page in range(1):
        p_url = 'https://www.amazon.in/s?k='+str(keyword)+'&page='+str(page)
        driver.get(p_url)
        # Parse the HTML content using etree
        dom = etree.HTML(driver.page_source)

        prod_list = dom.xpath("//div[@data-component-type='s-search-result']")
        prod_len = len(prod_list)
        for i in range (0, prod_len):
            name = dom.xpath('(//div[@data-component-type="s-search-result"])['+str(i+1)+']//h2/a/span/text()')
            name = ''.join(name)
            asin = dom.xpath('(//div[@data-component-type="s-search-result"])['+str(i+1)+']/@data-asin')
            asin = ''.join(asin)
            prod_url = "https://www.amazon.in/dp/"+str(asin)
            prod_url = ''.join(prod_url)
            sp = dom.xpath('(//div[@data-component-type="s-search-result"])['+str(i+1)+']//span[@class = "a-price-whole"]/text()')
            sp = ''.join(sp)
            sponser = dom.xpath('(//div[@data-component-type="s-search-result"])['+str(i+1)+']//span[@class = "puis-label-popover-default"]//text()')
            sponser = ''.join(sponser)
            if sponser == '':
                sponser = 'Organic'                 
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            img_elements = dom.xpath('(//div[@data-component-type="s-search-result"])[' + str(i+1) + ']//img[contains(@class, "s-image")]//@src')
##            img_urls = [driver.find_element(By.XPATH, '.' + img_element.getroottree().getpath(img_element)).get_attribute('src') for img_element in img_elements]
##            img = img_urls[0] if img_urls else ""
            try:
                img = img_elements[0]
            except:
                img = ""

            # Store the data into a temporary DataFrame
            dat = {
                'date': date,
                'keywords': keyword,
                'pname': name,
                'asin': asin,
                'url': prod_url,
                'price': sp,
                'sponsered': sponser,
                'prod_img': img,
                'rank': str(i+1)
                }
            data.append(dat)
            print(dat)
# Close the driver
driver.quit()

# Create a dataframe from the data list
df = pd.DataFrame(data)

# Save the all_data DataFrame to an Excel file
filename = "search.xlsx"
df.to_excel(filename, index=False)
database_push(df,'Search')
