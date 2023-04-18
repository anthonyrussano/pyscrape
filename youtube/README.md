## Description

These scripts are meant to pull rss feed urls from youtube channels.

### Usage

All scripts require URL to be provided as input parameter.

- Example: `python main.py <url>`

#### main.py

This script scrapes YouTube links from a given webpage and then checks each link to see if there is an associated RSS feed.

It does this by making HTTP requests to websites and parsing the HTML content of the responses using the requests and BeautifulSoup libraries.

The script then writes the URLs of any RSS feeds found to an output file. The script requires a command line argument to specify the base URL to scrape.

#### alt.py

This script checks if a given URL has an associated RSS feed. It does this by making an HTTP request to the URL and parsing the HTML content of the response using the requests and BeautifulSoup libraries.

The script then prints the URL of the RSS feed to the console. The script requires a command line argument to specify the URL to check.
