import os
from facebook_page_scraper import Facebook_scraper

page_list = ['jackie.duvall']

proxy_port = 10001

# Set posts_count to a large number to scrape as many posts as possible
posts_count = 1000
browser = "firefox"

timeout = 600  # 600 seconds
headless = False

# Directory for output set to the same directory as the script
directory = os.getcwd()

# Create the directory if it does not exist (this is redundant since we're using the current working directory)
if not os.path.exists(directory):
    os.makedirs(directory)

for page in page_list:
    # Our proxy for this scrape
    proxy = f'username:password@us.smartproxy.com:{proxy_port}'
    
    # Initializing a scraper
    scraper = Facebook_scraper(page, posts_count, browser, proxy=proxy, timeout=timeout, headless=headless)

    # Configure the scraper to retrieve all comments, not just the first one
    # Note: This assumes the facebook_page_scraper library supports these options.
    try:
        scraper.set_options(comments=True, all_comments=True)
    except AttributeError:
        print("Warning: The scraper does not support retrieving all comments. Check the library documentation.")

    # Scraping and writing into output CSV file
    filename = page
    scraper.scrap_to_csv(filename, directory)

    # Rotating our proxy to the next port so we could get a new IP and avoid blocks
    proxy_port += 1
