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

def database_push(data_frame, table_name):
    server = 'DESKTOP-R5K275N\SQLEXPRESS'
    database = 'Yogabar'
    params = urllib.parse.quote_plus('Driver={SQL Server};SERVER='+server+';DATABASE='+database)
    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=False)
    data_frame.to_sql(f'{table_name}', con=engine, index=False, if_exists='append', chunksize=5000,
                      dtype={col_name: NVARCHAR(length=1500) for col_name in data_frame})

    return 'successfully data pushed'

df = pd.read_excel('input.xlsx')
asins = df['code'].values

data = []
driver_path = r"E:\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

for asin in asins:
    page = 6
    for i in range(1, page):
        url = f'https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_fmt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={i}&formatType=current_format'
        driver.get(url)
        time.sleep(2)
        dom = etree.HTML(driver.page_source)
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
        review_list = dom.xpath('//*[@id="cm_cr-review_list"]//div[@data-hook="review"]')

##        if len(review_list) == 0 and i != 1:
##            print('not_found')
##            break

        if len(review_list) != 0:
            title = dom.xpath('//*[@data-hook="product-link"]/text()')
            title = ''.join(title)
            rating = dom.xpath('//*[@data-hook="average-star-rating"]//span/text()')
            rating = ''.join(rating)
            total_rating = dom.xpath('//*[@data-hook="cr-filter-info-review-rating-count"]/text()')
            total_rating = ''.join(total_rating).strip()
            pack_size = dom.xpath('//div[@style="padding-left:2%;float:left;"]/div[3]//span/text()[2]') \
                        or dom.xpath('//div[@style="padding-left:2%;float:left;"]/div[3]//span/text()')
            pack_size = ''.join(pack_size).replace('Size: ', '').replace('Style Name: ', '')
            for j in range(0, len(review_list)):
                cust_rating = dom.xpath(f'//*[@id="cm_cr-review_list"]//div[@data-hook="review"][{j+1}]//i[contains(@class, "review-rating")]/span/text()')
                cust_rating = ''.join(cust_rating)
                cust_rating = cust_rating if cust_rating else None

                comments = dom.xpath(f'//*[@id="cm_cr-review_list"]//div[@data-hook="review"][{j+1}]//span[@data-hook="review-body"]/span/text()')
                comments = ''.join(comments)
                comments = comments if comments else None

                cust_name = dom.xpath(f'//*[@id="cm_cr-review_list"]//div[@data-hook="review"][{j+1}]//div[@class="a-profile-content"]/span/text()')
                cust_name = ''.join(cust_name)
                cust_name = cust_name if cust_name else None

                comment_date = dom.xpath(f'//*[@id="cm_cr-review_list"]//div[@data-hook="review"][{j+1}]//span[@data-hook="review-date"]/text()')
                comment_date = ''.join(comment_date).replace('Reviewed in India 🇮🇳 on ','').replace('Reviewed in India on ', '')
                parsed_date = datetime.datetime.strptime(comment_date, "%d %B %Y")
                formatted_date = parsed_date.strftime("%Y-%m-%d")
                comment_date = formatted_date if formatted_date else None

                comment_title = dom.xpath(f'//*[@id="cm_cr-review_list"]//div[@data-hook="review"][{j+1}]//a[@data-hook="review-title"]/span/text()')
                comment_title = ''.join(comment_title)
                comment_title = comment_title if comment_title else None

                dat = {
                    'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'title': title,
                    'platform_code': asin,
                    'rating': rating,
                    'total_rating': total_rating,
                    'cust_ratings': cust_rating,
                    'comment_title': comment_title,
                    'comments': comments,
                    'cust_name': cust_name,
                    'comment_date': comment_date
                }
                data.append(dat)
                print(dat)

# Close the webdriver
driver.quit()

# Create a dataframe from the dictionary
df = pd.DataFrame(data)

# Drop duplicate rows
# df.drop_duplicates(inplace=True)

# Save the dataframe to an Excel file
filename = 'amazon_ratings.xlsx'
df.to_excel(filename, index=False)
database_push(df,'rating&reviews')

### Connect to the database again to remove duplicates
def delete_duplicate_records():
    server = 'DESKTOP-R5K275N\SQLEXPRESS'
    database = 'Yogabar'
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')

    cursor = conn.cursor()

    query = """
            WITH cte AS (
                SELECT *,
                ROW_NUMBER() OVER (PARTITION BY comment_title, comments, cust_name, comment_date ORDER BY comment_title, comments, cust_name, comment_date ASC) AS duplicate
                FROM [rating&reviews]
            )
            DELETE FROM cte
            WHERE duplicate > 1
            """

    try:
        cursor.execute(query)
        conn.commit()  # Commit the deletion operation

        print("Duplicate records deleted successfully.")
        
    except pyodbc.Error as e:
        print("Error occurred:", e)
    finally:
        cursor.close()
        conn.close()

delete_duplicate_records()

