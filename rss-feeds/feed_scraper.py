import requests
from bs4 import BeautifulSoup
import re
import sys

def get_feed_links(base_url):
    # Make a GET request to the channel URL
    response = requests.get(base_url)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a', href=True)

    # Extract the URL of each link containing "feed" or "rss"
    urls = [link['href'] for link in links if '/feed/' in link['href'] or '/rss/' in link['href'] or '/rss.xml' in link['href']]

    # Find all RSS and Atom links on the page
    feed_links = soup.find_all('link', {'type': ['application/rss+xml', 'application/atom+xml']})

    # Extract the URL of each RSS and Atom feed
    feed_urls = [link['href'] for link in feed_links]

    # Combine the two lists of URLs
    urls += feed_urls

    # Remove duplicate URLs
    urls = list(set(urls))

    # Return the list of URLs
    return urls

# Get the base URL and string from the command line arguments
if len(sys.argv) > 1:
    base_url = sys.argv[1]
else:
    print("Usage: python script.py <base_url> <string>")
    sys.exit(1)

string = ""
if len(sys.argv) > 2:
    string = sys.argv[2]
else:
    print("Usage: python script.py <base_url> <string>")
    sys.exit(1)

feed_links = get_feed_links(base_url)
if not feed_links:
    print("No feed links found on the page.")
else:
    for feed_link in feed_links:
        modified_line = feed_link.strip() + ' ! "' + string + '"'
        print(modified_line)
    else:
        pass
