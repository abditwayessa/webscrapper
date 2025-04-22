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



from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
import subprocess
import msvcrt
import Amazon
import threading
import time
import sys

def extractor():
    data = {"title":[],"price":[],"image":[],"rating":[],"delivery":[],"image":[]}

    for file in os.listdir("data"):
        try:
            with open(f"data/{file}") as f:
                html_doc = f.read()
                print("Reading file: " + file)
            soup = BeautifulSoup(html_doc,"html.parser")
            print("______________________________Parsing file: " + file)

            title = soup.find("h2").get_text()
            price = soup.find("span",attrs={'class':'a-price-whole'}).get_text()
            if(price=="" or price==None or price==FileNotFoundError):
                print("Price not found")
                price = soup.find("span",attrs={'class':'a-price-symbol'}).get_text()
            image_container = soup.find('div', class_='s-product-image-container')
            img_tag = image_container.find('img', class_='s-image')['src']
            rating = soup.find('span', class_='a-icon-alt').get_text()
            delivery = soup.find('div',class_='s-align-children-center').get_text()
            
            data["title"].append(title)
            data["price"].append(price)
            data["image"].append(img_tag)
            data["rating"].append(rating)
            data["delivery"].append(delivery)
            
            header1 = ["Title", "Price", "Rating", "Delivery","Image"]
            with open('Data.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=header1)
        
                writer.writeheader()
            
                for i in range(len(data['title'])):
                    row = {
                        "Title": data['title'][i],
                        "Price": data['price'][i],
                        "Rating": data['rating'][i],
                        "Delivery": data['delivery'][i],
                        "Image": data['image'][i]
                    }
                    writer.writerow(row)
            # print("Reading Book data. File number: " + str(i))
            os.system('cls') 
        except Exception as e:
            a=1
            a = a+1
            # print("Exception: ")
            # print(e)
    print()
    print()
    print()
    print()
    print()
    print()
    print("Data extracted successfully")
    print("Data.csv file created successfully")

    # openFile = input("Do you want to open the file? (Y/N): ")
    # if openFile == 'Y' or openFile == 'y':
    #     subprocess.Popen(['start', 'Data.csv'], shell=True)
    # else:
    #     print("File not opened")
    # print("Exiting the program...")


# open the file
def open_file():
    print("Do you want to open the file? (Y/N): ", end='', flush=True)

    key = msvcrt.getch().decode('utf-8')

    if key.lower() == 'y':
        subprocess.Popen(['start', 'Data.csv'], shell=True)
    else:
        print("\nFile not opened")
    os.system('cls') 
    print("Exiting the program...")

    # Loader
def animate_loading(stop_event):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        print(f"\rLoading... {spinner[idx % len(spinner)]}", end="")
        idx += 1
        time.sleep(0.1)
    os.system('cls') 
    print("\rData Loaded Successfully!")
    print("\rData Extracted Successfully!")
    print("\rData Reading Done Successfully!")
    print("\rSuccessfully!")
    # Hooker
def run_with_loading(met):
    stop_event = threading.Event()
    loader_thread = threading.Thread(target=animate_loading, args=(stop_event,))
    
    loader_thread.start()
    if met == 1:
        Amazon.get_book()
    else:
        extractor()
    stop_event.set()
    loader_thread.join()

if __name__ == "__main__":
    
    os.system('cls')
    print("1 for Scraping")
    print("2 for Extracting")
    print("3 for Scraping & Extracting")
    option = input("Enter your option: ")
    os.system('cls')
    if option == '1':
        print("Scraping")
        run_with_loading(1)
    elif option == '2':
        print("Extracting")
        run_with_loading(2)
        open_file()
    elif option == '3':
        run_with_loading(1)
        run_with_loading(2)
        open_file()
    else:
        print("Invalid option")
        sys.exit()
        
    # run_with_loading(1)
    # run_with_loading(2)
    # open_file()