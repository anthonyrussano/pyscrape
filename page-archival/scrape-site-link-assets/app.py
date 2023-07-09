from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


app = Flask(__name__)


def update_asset_links(soup, base_url):
    # Find all the <link> tags with href attribute
    link_tags = soup.find_all("link", href=True)

    for link in link_tags:
        # Update the href attribute value with absolute URL
        link["href"] = urljoin(base_url, link["href"])

    # Find all the <script> tags with src attribute
    script_tags = soup.find_all("script", src=True)

    for script in script_tags:
        # Update the src attribute value with absolute URL
        script["src"] = urljoin(base_url, script["src"])

    # Find all the <img> tags with src attribute
    img_tags = soup.find_all("img", src=True)

    for img in img_tags:
        # Update the src attribute value with absolute URL
        img["src"] = urljoin(base_url, img["src"])

    return soup


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form["url"]
    text = ""

    # Parse the URL to extract scheme and netloc
    parsed_url = urlparse(url)

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Update the links to all the assets
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        updated_soup = update_asset_links(soup, base_url)

        # Save the updated HTML as a file
        with open("result.html", "w", encoding="utf-8") as file:
            file.write(updated_soup.prettify())

    return render_template("success.html")


@app.route("/download")
def download():
    return send_file("result.html", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="10.32.25.124", port=8080)
