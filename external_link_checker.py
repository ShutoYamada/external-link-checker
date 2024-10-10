import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import argparse
import urllib3
import os
from dotenv import load_dotenv
from google.cloud import webrisk_v1
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Load environment variables from .env file
load_dotenv()

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set of visited URLs to avoid processing the same URL multiple times
visited_urls = set()
# Dictionary to store external links and their source pages and safety status
external_links = {}

# Dictionary to store proxy settings
proxies_dic = {
    #"http": "http://your_proxy:port",
    #"https": "http://your_proxy:port"
}

# Get the Google API key from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')

# Selenium Chrome Driver setup
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--lang=ja')  # 言語設定を日本語に変更

# Use the appropriate path for your ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

def is_external_link(url, base_url):
    """
    Check if a URL is an external link and return the link type.
    :param url: URL to check
    :param base_url: The base URL of the website
    :return: 'External' if the URL is an external HTTP/HTTPS link, 'Not Applicable' for mailto, tel, etc., otherwise None
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme in ['mailto', 'tel', 'te', 'javascript']:
        return 'Not Applicable'
    if urlparse(url).netloc != urlparse(base_url).netloc:
        return 'External'
    return None

def check_url_safety(url):
    """
    Check the safety of a URL using Google Safe Browsing Web Risk API.
    :param url: URL to check
    :return: 'Safe' if the URL is safe, 'Unsafe' if the URL is risky
    """
    if google_api_key:
        client = webrisk_v1.WebRiskServiceClient(
            client_options={"api_key": google_api_key}
        )
        uri = url
        threat_types = [webrisk_v1.ThreatType.MALWARE,
                        webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                        webrisk_v1.ThreatType.UNWANTED_SOFTWARE]

        try:
            response = client.search_uris(uri=uri, threat_types=threat_types)
            if response.threat:
                return 'Unsafe'
            return 'Safe'
        except Exception as e:
            print(f"Error checking URL safety {url}: {e}")
            return 'Unknown'
    else:
        return 'Not Checked'

def scrape_links(url, base_url):
    """
    Recursively scrape links from the given URL and optionally take screenshots of external links.
    :param url: The current URL to scrape
    :param base_url: The base URL of the website
    :return: Updated index value for the next link
    """
    try:
        visited_urls.add(url)
        response = requests.get(url, proxies=proxies_dic)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if link not in visited_urls:
                link_type = is_external_link(link, base_url)
                if link_type == 'External':
                    parsed_link = urlparse(link)
                    if parsed_link.scheme in ['http', 'https']:
                        safety_status = check_url_safety(link)
                        external_links[link] = (url, safety_status)
                    else:
                        safety_status = 'Not Applicable'

                else:
                    scrape_links(link, base_url)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e} : base={base_url}")

def save_to_csv(external_links, csv_path):
    """
    Save the collected external links, their source pages, and safety status to a CSV file.
    :param external_links: Dictionary of external links, their source pages, and safety status
    :param csv_path: The CSV file path
    """
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['External Link', 'Source Page', 'Safety Status'])
        for link, (source, safety_status) in external_links.items():
            csvwriter.writerow([link, source, safety_status])

def main(base_url, output_path, take_screenshots=True):
    """
    Main function to start the scraping process and save results to a CSV file and optionally take screenshots.
    :param base_url: The base URL of the website to scrape
    :param output_path: Path for the output (CSV file and optionally a directory for screenshots)
    :param take_screenshots: Whether or not to take screenshots of external links
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Paths for the CSV file and screenshot directory
    csv_path = os.path.join(output_path, 'output.csv')
    screenshot_dir = output_path

    # Scrape links and optionally take screenshots
    scrape_links(base_url, base_url)

    # Save the results to the CSV file
    save_to_csv(external_links, csv_path)
    print(f"Saved {len(external_links)} external links to {csv_path}")

    # TODO take_screenshots=Trueならexternal_linksのデータを用いて1件ずつリンク先のスクリーンショットを撮る
    # TODO スクリーンショットはCSVの行数と対応させるためN_xxxx.example.pngのようなフォーマットにする(N=レコードの連番)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape external links from a website and optionally take screenshots.")
    parser.add_argument("base_url", help="The base URL of the website to scrape")
    parser.add_argument("output_path", help="The output path (directory for CSV and screenshots)")
    parser.add_argument("--no-screenshots", action="store_true", help="Do not take screenshots of external links")
    args = parser.parse_args()

    # Call the main function with the appropriate flags
    main(args.base_url, args.output_path, take_screenshots=not args.no_screenshots)

# Don't forget to close the driver when done
driver.quit()