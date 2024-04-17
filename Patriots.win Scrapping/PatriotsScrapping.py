from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Create a new WebDriver instance
driver = webdriver.Chrome(options=options)

# Load the target website
driver.get("https://patriots.win/")
article_data = []

# Function to scroll down to load more content
def scroll_down(driver):
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for content to load

# Function to extract timestamp
def extract_timestamp(article):
    try:
        # Hover over the article to make the timestamp appear
        ActionChains(driver).move_to_element(article).perform()

        # Wait until the tooltip appears
        tooltip = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[aria-describedby]'))
        )

        # Extract the timestamp text
        timestamp = tooltip.text

        return timestamp
    except Exception as e:
        print("Error extracting timestamp:", e)
        return None

# Scroll down repeatedly until no more content is loaded
while True:
    try:
        # Get all <a> tags containing article text
        articles = driver.find_elements(By.CSS_SELECTOR, 'div.post-item a')

        # Extract text and timestamp from each article and add to the list
        for article in articles:
            article_text = article.text
            timestamp = True
            if timestamp:
                print(article_text)
                article_data.append({"Article": article_text, "Timestamp": timestamp})

        # Scroll down to load more content
        scroll_down(driver)

    except Exception as e:
        print("Error:", e)
        break  # Break the loop if any error occurs

# Close the browser
driver.quit()

# Convert the list to a DataFrame
df = pd.DataFrame(article_data)

# Save the DataFrame to an Excel file with UTF-16LE encoding
df.to_excel('articles_with_timestamps.xlsx', index=False)

print("Scraping complete. Data saved to articles_with_timestamps.xlsx.")
