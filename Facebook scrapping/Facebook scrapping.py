import os
from facebook_page_scraper import Facebook_scraper

page_list = ['antifaunited161']

proxy_port = 10001

posts_count = 100
browser = "firefox"

timeout = 600  # 600 seconds
headless = False

# Directory for output if we scrape directly to CSV
directory = "E:\\facebook_scrape_results"

# Create the directory if it does not exist
if not os.path.exists(directory):
    os.makedirs(directory)

for page in page_list:
    # Our proxy for this scrape
    proxy = f'username:password@us.smartproxy.com:{proxy_port}'
    # Initializing a scraper
    scraper = Facebook_scraper(page, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless)

    # Running the scraper in two ways:

    # 1
    # Scraping and printing out the result into the console window:

    # json_data = scraper.scrap_to_json()
    # print(json_data)

    # 2
    # Scraping and writing into output CSV file:

    filename = page
    scraper.scrap_to_csv(filename, directory)

    # Rotating our proxy to the next port so we could get a new IP and avoid blocks
    proxy_port += 1
