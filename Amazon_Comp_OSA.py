from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from lxml import etree 
import pandas as pd
import datetime
import time
import re
import sqlalchemy as sa
from sqlalchemy.types import NVARCHAR
import pyodbc
import urllib
from selenium.webdriver.chrome.options import Options
from shutil import which
import random

def database_push(data_frame, table_name):
    server = 'DESKTOP-R5K275N\SQLEXPRESS'
    database = 'Yogabar'
    params = urllib.parse.quote_plus('Driver={SQL Server};SERVER='+server+';DATABASE='+database)
    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=False)
    data_frame.to_sql(f'{table_name}', con=engine, index=False, if_exists='append', chunksize=5000,
                      dtype={col_name: NVARCHAR(length=1500) for col_name in data_frame})

    return 'successfully data pushed'

# Create a list of ASINs
df = pd.read_excel('comp_input.xlsx')
asins = df['code'].values
##asins = ['B09PB5CCXB',	' B07CN1K1Z6',	' B08R7BYNVV']
# Create an empty dictionary to store the data
data = []
# Set up the webdriver
##driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe")
##driver_path = r"E:\chromedriver.exe"
chrome_options=Options()
chrome_path=which("chromedriver")
driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe",options=chrome_options)
driver.maximize_window()
##driver.get('chrome://settings/')
##driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.8);')
##driver.maximize_window()


# Loop through each ASIN in the list
for asin in asins:
    # Construct the URL for the product page
    url = f'https://www.amazon.in/dp/{asin}'
    # Navigate to the product page
    driver.get(url)
    time.sleep(2)
    dom=etree.HTML(driver.page_source)
    from amazoncaptcha import AmazonCaptcha
    html = driver.page_source
    dom = etree.HTML(html)
    captcha = dom.xpath('.//input[@id="captchacharacters"]')
     
    if captcha:
         img_link = dom.xpath('.//div[@class="a-row a-text-center"]/img/@src')
         img_link = ''.join(img_link)

         captcha = AmazonCaptcha.fromlink(img_link)
         solution = captcha.solve()

         search_input = driver.find_element_by_id("captchacharacters")
         search_input.send_keys(solution)

         click_btn = driver.find_element_by_xpath('.//button[@class="a-button-text"]')
         click_btn.click()
         time.sleep(5)
         html = driver.page_source
         dom = etree.HTML(html)

    # Extract the data using XPath
    title = dom.xpath('//h1[contains(@id, "title")]/span/text()')
    title = ''.join(title).strip()
    mrp = dom.xpath('//div//tr//span[@data-a-strike = "true"]//span[2]/text()')\
          or dom.xpath('//div[@class = "a-section a-spacing-small aok-align-center"]//span[@data-a-strike = "true"]//span[2]/text()')\
          or dom.xpath('//div//span[@data-a-strike = "true"]//span[2]/text()')
    mrp = ''.join(mrp)
    sp = dom.xpath('//div//span[@class = "a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[2]/text()') \
         or dom.xpath('//div[@class="a-section a-spacing-none aok-align-center"]/span[2]/span[1]/text()') \
         or dom.xpath('//tr[td[contains(text(), "Deal")]]//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[contains(@aria-hidden, "true")]/text()')\
         or dom.xpath('//tr[td[contains(text(), "Price")]]//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]/span[contains(@aria-hidden, "true")]/text()')
    sp = ''.join(sp).strip()
    default_asin = dom.xpath('//th[contains(text(), "ASIN")]/following-sibling::td[@class="a-size-base prodDetAttrValue"]/text()')
    default_asin =''.join(default_asin).strip()
    status = dom.xpath('//span[@id = "submit.add-to-cart-announce"]/text()') or dom.xpath('//div[@id = "availabilityInsideBuyBox_feature_div"]//div/div/span/text()') \
             or dom.xpath('//b[contains(., "Looking for something?")]/text()') or dom.xpath('//div[@id = "outOfStock"]/div/div/span[1]/text()') \
             or dom.xpath('//div[@data-feature-name = "almAvailability"]/div/span/text()') or dom.xpath('//div[@data-feature-name = "almAvailability"]/div/span/text()')
    status = ''.join(status).replace(' In stock  In stock', 'In stock').replace('.', '').strip()
    weight = dom.xpath('//tr[@class="a-spacing-small po-item_weight"]//span[@class="a-size-base po-break-word"]/text()') \
             or dom.xpath('//tr[@class="a-spacing-small po-item_package_weight"]//span[@class="a-size-base po-break-word"]/text()')
    weight = ''.join(weight).strip()
    quantity = dom.xpath('//tr[@class="a-spacing-small po-unit_count"]//span[@class="a-size-base po-break-word"]/text()')
    quantity = ''.join(quantity).strip()
    seller = dom.xpath('//*[@id="merchant-info"]/a[1]/span/text()') or dom.xpath('//*[@id="merchant-info"]/a[2]/span/text()') \
             or dom.xpath('//*[@id="merchant-info"]/a/text()')
    seller = ''.join(seller)
    deal = dom.xpath('//div[@id = "corePrice_desktop"]//tr[2]/td[@class = "a-color-secondary a-size-base a-text-right a-nowrap"]/text()')
    deal = ''.join(deal).replace('Deal of the Day:', 'Deal of the Day')
    rating = dom.xpath('//span[@data-hook = "rating-out-of-text"]/text()')
    rating = ''.join(rating)
    sub_cat = dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[3]/td/span/span[2]/a/text()') \
              or dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[2]/td/span/span[2]/a/text()')
    sub_cat = ''.join(sub_cat)
    sub_cat_rank_raw = dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[3]/td/span/span[2]/text()') \
                       or dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[2]/td/span/span[2]/text()')
    sub_cat_rank_raw = ''.join(sub_cat_rank_raw)
    sub_cat_rank = re.findall(r'\d+', sub_cat_rank_raw)
    sub_cat_rank = ''.join(sub_cat_rank)
    delivery_date_raw = dom.xpath('//*[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"]/span/span[1]/text()')
    delivery_date_raw = ''.join(delivery_date_raw)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    year = current_date[:4]
    delivery_days = ''
    try:
        if 'Tomorrow' in delivery_date_raw:
            delivery_date = datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        else:
            delivery_date = datetime.datetime.strptime(delivery_date_raw + ' ' + str(year), '%A, %d %B %Y')
            formatted_date = delivery_date.strftime('%Y-%m-%d')
            delivery_days = (datetime.datetime.strptime(formatted_date, '%Y-%m-%d') - datetime.datetime.strptime(current_date, '%Y-%m-%d')).days
    except:
        ''        
    main_cat_raw = dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[3]/td/span/span[1]/text()') \
                   or dom.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[2]/td/span/span[1]/text()[1]')
    main_cat_raw = ''.join(main_cat_raw)
    main_cat_rank = re.findall(r'\d+', main_cat_raw)
    main_cat_rank = ''.join(main_cat_rank)
    match = re.search(r'[a-zA-Z&\s]+', main_cat_raw)
    if match:
        main_cat = match.group().strip()
        main_cat = re.sub(r'\bin\b', '', main_cat)
    else:
        main_cat = ""
        
        # Add the data to the dictionary
    dat = {
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'title': title,
        'mrp': mrp,
        'sp': sp,
        'status': status,
        'seller': seller,
        'platform_code': asin,
        'url': url,
        'deal': deal if 'Deal of the Day' in deal else '',
        'rating': rating,
        'main_cat': main_cat,
        'main_cat_rank': main_cat_rank,
        'sub_cat': sub_cat,
        'sub_cat_rank': sub_cat_rank,
        'delivery days': delivery_days,
        'default_asin': default_asin,
        'pack size': weight if weight else quantity
        }
    data.append(dat)
    print(dat)

# Close the webdriver
driver.quit()

# Create a dataframe from the dictionary
df = pd.DataFrame(data)

# Save the dataframe to an Excel file
filename = 'comp_osa.xlsx'
df.to_excel(filename, index=False)
database_push(df,'comp_osa')
