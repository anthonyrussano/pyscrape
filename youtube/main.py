import requests
from bs4 import BeautifulSoup
import re
import sys

def scrape_youtube_links(base_url):
    # Make a GET request to the base URL
    response = requests.get(base_url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the page that match the base URL
    links = soup.find_all('a', href=re.compile("^https?://www\.youtube\.com"))

    # Store the URLs that match the base URL in a list
    matched_links = []
    for link in links:
        matched_links.append(link['href'])

    return matched_links

def get_rss_link(channel_url):
    # Make a GET request to the channel URL
    response = requests.get(channel_url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the RSS link on the page
    rss_link = soup.find('link', {'type': 'application/rss+xml'})

    # Return the URL of the RSS feed if found, otherwise return None
    if rss_link:
        return rss_link['href']
    else:
        return None

# Get the base URL from the command line arguments
if len(sys.argv) > 1:
    base_url = sys.argv[1]
else:
    print("Usage: python script.py <base_url>")
    sys.exit(1)

# Open a file to write the output to
with open('output.txt', 'w') as file:
    # Call the function to scrape the YouTube links
    matched_links = scrape_youtube_links(base_url)

    # Loop over the URLs that match the base URL and call the get_rss_link function on each one
    for link in matched_links:
        rss_link = get_rss_link(link)
        if rss_link:
            modified_line = rss_link.strip() + ' ! "univ"'
            print(modified_line, file=file)
        else:
            pass