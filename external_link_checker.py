import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import argparse
import urllib3
import os
from dotenv import load_dotenv
from google.cloud import webrisk_v1

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

def is_external_link(url, base_url):
    """
    Check if a URL is an external link.
    :param url: URL to check
    :param base_url: The base URL of the website
    :return: True if the URL is external, False otherwise
    """
    return urlparse(url).netloc != urlparse(base_url).netloc

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
        # If the API key is not set, assume all URLs are safe (or handle differently as needed)
        return 'Not Checked'

def scrape_links(url, base_url):
    """
    Recursively scrape links from the given URL.
    :param url: The current URL to scrape
    :param base_url: The base URL of the website
    """
    try:
        # Skip already visited URLs
        if url in visited_urls:
            return

        visited_urls.add(url)  # Mark the URL as visited

        response = requests.get(url, proxies=proxies_dic)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            if link not in visited_urls:
                if is_external_link(link, base_url):
                    # Check if the link is an HTTP or HTTPS URL
                    parsed_link = urlparse(link)
                    if parsed_link.scheme in ['http', 'https']:
                        safety_status = check_url_safety(link)
                    else:
                        safety_status = 'Not Applicable'
                    external_links[link] = (url, safety_status)  # Store the external link, its source page, and safety status
                else:
                    scrape_links(link, base_url)  # Recursively scrape internal links only

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")

def save_to_csv(external_links, output_file):
    """
    Save the collected external links, their source pages, and safety status to a CSV file.
    :param external_links: Dictionary of external links, their source pages, and safety status
    :param output_file: The output CSV file path
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['External Link', 'Source Page', 'Safety Status'])
        for link, (source, safety_status) in external_links.items():
            csvwriter.writerow([link, source, safety_status])

def main(base_url, output_file):
    """
    Main function to start the scraping process and save results to a CSV file.
    :param base_url: The base URL of the website to scrape
    :param output_file: The output CSV file path
    """
    scrape_links(base_url, base_url)
    save_to_csv(external_links, output_file)
    print(f"Saved {len(external_links)} external links to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape external links from a website.")
    parser.add_argument("base_url", help="The base URL of the website to scrape")
    parser.add_argument("output_file", help="The output CSV file")
    args = parser.parse_args()
    main(args.base_url, args.output_file)