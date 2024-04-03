from flask import Flask, jsonify
from flask_cors import CORS 

from datetime import datetime #used for the date article is published 
from bs4 import BeautifulSoup #to scrape html 
import requests #to request page and scrape it 

# Requeesting URL for bullhorn home page
url = "https://www.thebullhorn.net/"
response = requests.get(url)
html_content = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all articles on home page
article_cards = soup.find_all( class_ = "card-side")

# class to hold article data to be sent to front end


all_Articles = []

#tracking variables
article_count = 0


# Iterate through the articles
for article in article_cards:   
    # print("all good")      
    repeats = False  
    title = article.find(class_ = "font-headline").text

    #the webscraper seems to be looking a the articles in certain areas of the site multiple times, so only look for article titles the first time they appear
    for set_article in all_Articles:
        if  title == set_article[0]:
            repeats = True

    if repeats == False:

        author = article.find("a", class_="font-medium").text
        lede = article.find(class_ = "text-sm").text

        #two different ways are used to pull the time because of a bad design choice by Max where half the dates use abbrrviated months (ex. Jun, Jan) and some use the full name (ex. April)
        time = article.time.text
        try:
            time = datetime.strptime(article.time.text, "%b. %d, %Y" )
        except:
            time = datetime.strptime(article.time.text, "%B %d, %Y" )
        

        article_url = url + str(article.find("a")["href"])

        article_response = requests.get(article_url)
        article_html_content = article_response.text
        article_soup = BeautifulSoup(article_html_content, 'html.parser')
        section = article_soup.find(class_ = "hover:text-leman-blue").text

        use_article = [title, author, lede, time, article_url, section]

        all_Articles.append(use_article)

app = Flask(__name__)
cors = CORS(app, origins="*")

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify(
        {
            "articles": [
                'article 1', 
                'article 2',
                'article 3'
            ]
        }
    )

@app.route("/api/articles", methods=['GET'])
def articles():
    return jsonify(all_Articles)


print("Hello world")

if __name__ == "__main__":
    app.run(debug=True, port=8080)