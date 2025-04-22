# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# def get_amazon_book_info(book_title):
#     # Set up headless browser (no UI)
#     options = Options()
#     options.headless = True
    
#     # Set up Chrome driver service
#     service = Service(ChromeDriverManager().install())
    
#     # Use the correct method to instantiate WebDriver
#     driver = webdriver.Chrome(service=service, options=options)

#     # Search Amazon for the book
#     search_url = f"https://www.amazon.com/s?k={book_title.replace(' ', '+')}&i=stripbooks-intl-ship"
#     driver.get(search_url)

#     # Scroll the page to ensure content is fully loaded
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  # Wait after scrolling
#     driver.get(search_url)
#     driver.execute_script("window.scrollTo(0, document  .body.scrollHeight);")
#     # Wait for the first book result to be clickable
#     try:
#         first_book = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '.s-result-item h2 a'))
#         )
#         book_url = first_book.get_attribute('href')
#         print(f"Found book URL: {book_url}")  # Debugging output
#     except Exception as e:
#         print(f"Error finding book URL: {e}")
#         driver.quit()
#         return None

#     # Go to the book's detail page
#     driver.get(book_url)
#     time.sleep(3)

#     # Scrape book details
#     book_details = {}
#     try:
#         book_details["Title"] = driver.find_element(By.ID, 'productTitle').text
#     except:
#         book_details["Title"] = "N/A"
    
#     try:
#         book_details["Author"] = driver.find_element(By.CSS_SELECTOR, '.author a.a-link-normal').text
#     except:
#         book_details["Author"] = "N/A"
    
#     try:
#         book_details["Price"] = driver.find_element(By.CSS_SELECTOR, '.a-price .a-offscreen').text
#     except:
#         book_details["Price"] = "N/A"

#     try:
#         book_details["Rating"] = driver.find_element(By.CSS_SELECTOR, 'i.a-icon-star span').text
#     except:
#         book_details["Rating"] = "N/A"
    
#     try:
#         book_details["Description"] = driver.find_element(By.ID, 'bookDescription_feature_div').text
#     except:
#         book_details["Description"] = "N/A"

#     try:
#         image_url = driver.find_element(By.ID, 'imgBlkFront').get_attribute('src')
#         book_details["Image URL"] = image_url
#     except:
#         book_details["Image URL"] = "N/A"

#     try:
#         # ISBN-10 and ISBN-13
#         isbn_10, isbn_13 = "N/A", "N/A"
#         details = driver.find_elements(By.CSS_SELECTOR, '#detailBullets_feature_div li')
#         for item in details:
#             text = item.text.strip()
#             if "ISBN-10" in text:
#                 isbn_10 = text.split(":")[-1].strip()
#             elif "ISBN-13" in text:
#                 isbn_13 = text.split(":")[-1].strip()
#         book_details["ISBN-10"] = isbn_10
#         book_details["ISBN-13"] = isbn_13
#     except:
#         book_details["ISBN-10"] = "N/A"
#         book_details["ISBN-13"] = "N/A"

#     # Close the driver
#     driver.quit()
    
#     return book_details

# # ----- USAGE -----
# book_name = input("Enter book name: ")
# book_info = get_amazon_book_info(book_name)

# if book_info:
#     print("\n📚 Book Details:")
#     for key, val in book_info.items():
#         print(f"{key}: {val}")
# else:
#     print("Book not found.")











# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import numpy as np
# import csv

# # Function to extract Product Title
# def get_title(soup):

#     try:
#         # Outer Tag Object
#         title = soup.find("span", attrs={"id":'productTitle'})
        
#         # Inner NavigatableString Object
#         title_value = title.text

#         # Title as a string value
#         title_string = title_value.strip()

#     except AttributeError:
#         title_string = ""

#     return title_string

# # Function to extract Product Price
# def get_price(soup):

#     try:
#         price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

#     except AttributeError:

#         try:
#             # If there is some deal price
#             price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

#         except:
#             price = ""

#     return price

# # Function to extract Product Rating
# def get_rating(soup):

#     try:
#         rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
#     except AttributeError:
#         try:
#             rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
#         except:
#             rating = ""	

#     return rating

# # Function to extract Number of User Reviews
# def get_review_count(soup):
#     try:
#         review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

#     except AttributeError:
#         review_count = ""	

#     return review_count

# # Function to extract Availability Status
# def get_availability(soup):
#     try:
#         available = soup.find("div", attrs={'id':'availability'})
#         available = available.find("span").string.strip()

#     except AttributeError:
#         available = "Not Available"	

#     return available
# if __name__ == '__main__':

#     # add your user agent 
#     HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

#     BookName = input("Enter the book name: ").lower()
    
#     BookName = BookName.replace(" ", "+")
    
#     # The webpage URL
#     URL = "https://www.amazon.com/s?k="+BookName+"&i=stripbooks-intl-ship"

#     # HTTP Request
#     webpage = requests.get(URL, headers=HEADERS)

#     # Soup Object containing all data
#     soup = BeautifulSoup(webpage.content, "html.parser")

#     # Fetch links as List of Tag Objects
#     links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

#     # Store the links
#     links_list = []

#     # Loop for extracting links from Tag Objects
#     for link in links:
#             links_list.append(link.get('href'))

#     d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
#     print(URL)
    
#     # Loop for extracting product details from each link 
#     for link in links_list:
#         new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

#         new_soup = BeautifulSoup(new_webpage.content, "html.parser")

#         # Function calls to display all necessary product information
#         d['title'].append(get_title(new_soup))
#         d['price'].append(get_price(new_soup))
#         d['rating'].append(get_rating(new_soup))
#         d['reviews'].append(get_review_count(new_soup))
#         d['availability'].append(get_availability(new_soup))
#     print("Titles: " + ", ".join(d['title']))
    
#     header1 = ["title", "rating", "reviews", "availability"]
    
#     with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=header1)
    
#     # Write the header row
#         writer.writeheader()
    
#     # Assuming all lists in the dictionary have the same length, write the rows
#         for i in range(len(d['title'])):
#             row = {
#                 "title": d['title'][i],
#                 # "price": d['price'][i],
#                 "rating": d['rating'][i],
#                 "reviews": d['reviews'][i],
#                 "availability": d['availability'][i]
#             }
#             writer.writerow(row)

# print("CSV file 'output.csv' has been created successfully.")
#     # amazon_df = pd.DataFrame.from_dict(d)
#     # amazon_df['title'].replace('', np.nan, inplace=True)
#     # amazon_df = amazon_df.dropna(subset=['title'])
#     # amazon_df.to_csv("amazon_data.csv", header=True, index=False)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
def get_book():
    driver = webdriver.Chrome()
    query = "books"
    file = 0


    for i in range(1,20):
        if i == 1:
            driver.get(f"https://www.amazon.com/")
            time.sleep(2)
        # driver.get(f"https://www.amazon.in/s?k={query}&page={i}&crid=1895KSWNLJ6QB&sprefix={query}%2Caps%2C349&ref=nb_sb_noss_1")
        driver.get(f"https://www.amazon.com/s?k={query}&i=stripbooks-intl-ship&page={i}&xpid=HNT9qdpqEBV3w&crid=1SF4CI6N17Q7J&qid=1744802388&sprefix={query}%2Cstripbooks-intl-ship%2C308&ref=sr_pg_{i}")
        elems = driver.find_elements(By.CLASS_NAME,"puis-card-container")
        for elem in elems:
            d= elem.get_attribute("outerHTML")
            with open(f"data/{query}{file}.html","w",encoding="utf-8") as f:
                f.write(d)
                file+=1
        time.sleep(2)

    driver.close()

