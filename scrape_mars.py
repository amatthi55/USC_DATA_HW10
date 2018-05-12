from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import tweepy
import json
import pandas as pd

from twitterapi import consumer_key, consumer_secret, access_token, access_token_secret


def scrape():

    url = 'https://mars.nasa.gov/news/'

    executable_path = {'executable_path': '/Users/AlexMac/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')


    # In[4]:


    article = soup.find("div", class_="list_text")

    news_date = article.find("div", class_="list_date").text

    headline = article.find("div", class_="content_title").find("a").text

    teaser = article.find("div", class_="article_teaser_body").text




    # In[6]:


    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')


    # In[7]:


    featured_image_url = "https://www.jpl.nasa.gov" + soup.find("article").find("a").get("data-fancybox-href")


    # In[17]:


    featured_image_url


    # In[8]:


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())



    # In[9]:


    target_user = "MarsWxReport"


    tweets = api.user_timeline(target_user)


    for tweet in tweets:

        if tweet["text"][0:3] == "Sol":
            mars_weather = tweet["text"]
            break


    # In[10]:


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    type(tables)


    # In[11]:


    space_df = tables[0]
    space_df.columns = ["Description", "Value"]
    space_df = space_df.set_index("Description")


    # In[14]:


    html_table = space_df.to_html()
    html_table = html_table.replace('\n', '')


    # In[15]:


    html_table


    # In[16]:


    hemisphere_image_urls =[{"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}]

    return {"hemispheres":hemisphere_image_urls, "headline":headline, "teaser":teaser, "featured_image_url":featured_image_url, "mars_weather":mars_weather, "html_table": html_table}