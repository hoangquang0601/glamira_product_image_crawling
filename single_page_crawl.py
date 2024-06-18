from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from tqdm import tqdm

# Create the directory if it does not exist
output_dir = "D:\\Download\\Data Engineer K9\\Crawling\\diamond-rings"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the browser and open the page
browser = webdriver.Chrome()
browser.get('https://www.glamira.com/diamond-rings/')

# Function to scroll down the page
def scroll_down():
    browser.execute_script("window.scrollBy(0, 500);")

# Scroll down and click 'load more' button multiple times
for _ in range(120):
    scroll_down()
    time.sleep(0.05)
    print("Scrolling down " + str(_))

# Find and click the 'load more' button
try:
    load_more_button = browser.find_element(By.ID, "loadding_more_item")
    for i in range(118):
        load_more_button.click()
        time.sleep(0.05)
        print("Clicking 'load more' button " + str(i))
        for j in range(5):
            scroll_down()
            time.sleep(0.05)
            print("Scrolling down " + str(j))
except Exception as e:
    print(f"Could not find or click 'load more' button: {e}")

# Get the page source and close the browser
page_source = browser.page_source
browser.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all image tags
image_tags = soup.find_all('img')

# Function to download and save images
def download_image(url, file_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Check content type to ensure it's an image
            if 'image' in response.headers.get('content-type', ''):
                image = Image.open(BytesIO(response.content))
                # Convert image to RGB if it has an alpha channel
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                image.save(file_path, format='JPEG')
    except Exception as e:
        print(f"Could not download {url}: {e}")

# Extract image URLs and download the images with a progress bar
for index, img in enumerate(tqdm(image_tags, desc="Downloading images")):
    img_url = img.get('src')
    alt_text = img.get('alt', f'image_{index}')
    if img_url and img_url.startswith('http'):
        # Clean the alt text to make it a valid filename
        alt_text = alt_text.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(output_dir, f'{alt_text}.jpg')
        download_image(img_url, file_path)
