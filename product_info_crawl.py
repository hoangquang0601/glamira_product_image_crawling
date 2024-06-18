from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# Create the directory if it does not exist
output_dir = "D:\\Download\\Data Engineer K9\\Crawling\\images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the browser and open the page
browser = webdriver.Chrome()
browser.get('https://www.glamira.com/diamond-necklaces/')

# Function to scroll down the page
def scroll_down():
    browser.execute_script("window.scrollBy(0, 500);")

# Scroll down and click 'load more' button multiple times
for _ in range(120):
    scroll_down()
    time.sleep(0.1)
    print("Scrolling down " + str(_))

# Find and click the 'load more' button
try:
    # load_more_button_id = browser.find_element(By.ID, "loadding_more_item")
    load_more_button = browser.find_element(By.CLASS_NAME, "content_loadding_more")
    for i in range(118):
        load_more_button.click()
        time.sleep(0.1)
        print("Clicking 'load more' button " + str(i))
        for j in range(5):
            scroll_down()
            time.sleep(0.1)
            print("Scrolling down " + str(j))
except Exception as e:
    print(f"Could not find or click 'load more' button: {e}")

# Get the page source and close the browser
page_source = browser.page_source
browser.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all product details
product_details = soup.find_all('div', class_='product-item-details')

# Lists to hold the extracted data
product_names = []
short_descriptions = []
prices = []

# Extract the required information
for product in product_details:
    product_name_tag = product.find('h2', class_='product-item-details product-name')
    short_description_tag = product.find('span', class_='short-description')
    price_tag = product.find('span', class_='price-wrapper')
    
    if product_name_tag:
        product_name = product_name_tag.get_text(strip=True).replace('GLAMIRA', '').strip()
        product_names.append(product_name)
    else:
        product_names.append('N/A')
    
    if short_description_tag:
        short_description = short_description_tag.get_text(strip=True)
        short_descriptions.append(short_description)
    else:
        short_descriptions.append('N/A')
    
    if price_tag:
        price = price_tag.get_text(strip=True)
        prices.append(price)
    else:
        prices.append('N/A')

# Create a DataFrame and save to CSV
df = pd.DataFrame({
    'Product Name': product_names,
    'Short Description': short_descriptions,
    'Price': prices
})

output_csv_path = "D:\\Download\\Data Engineer K9\\Crawling\\diamond-necklaces.csv"
df.to_csv(output_csv_path, index=False)

print(f"Product information saved to {output_csv_path}")
