import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, render_template, request

app = Flask(__name__)


def download_file(url, directory):
    response = requests.get(url, stream=True)
    filename = os.path.basename(url)
    filepath = os.path.join(directory, filename)
    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def scrape_webpage(url, output_directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    styles = soup.find_all("link", {"rel": "stylesheet"})

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Download HTML content
    html_filename = "index.html"
    html_filepath = os.path.join(output_directory, html_filename)
    with open(html_filepath, "wb") as file:
        file.write(response.content)

    # Download style assets
    for style in styles:
        style_url = urljoin(url, style["href"])
        download_file(style_url, output_directory)

    return True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        webpage_url = request.form.get("url")
        output_dir = "output"

        if webpage_url:
            success = scrape_webpage(webpage_url, output_dir)
            if success:
                message = "Scraping successful! HTML and style assets downloaded."
            else:
                message = "Failed to scrape the webpage."
        else:
            message = "Please enter a valid URL."

        return render_template("index.html", message=message)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="10.32.25.124", port=8080)
