import requests
from bs4 import BeautifulSoup
import re
import sys

def get_rss_link(base_url):
    # Make a GET request to the channel URL
    response = requests.get(base_url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the RSS link on the page
    rss_link = soup.find('link', {'type': 'application/rss+xml'})

    # Return the URL of the RSS feed if found, otherwise return None
    if rss_link:
        return rss_link['href']
    else:
        return None

# Get the base URL from the command line argument
if len(sys.argv) > 1:
    base_url = sys.argv[1]
else:
    print("Usage: python script.py <base_url>")
    sys.exit(1)

rss_link = get_rss_link(base_url)
print(rss_link)
