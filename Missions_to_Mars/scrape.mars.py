# Splinter is an open source tool for testing web applications
# Install from terminal: pip install splinter
from splinter import Browser
# Beautiful Soup is a python library for pulling data from HTML files
# Install from terminal: pip install beautifulsoup4
from bs4 import BeautifulSoup
# Install from terminal: pip install requests
import requests
# Install from terminal: pip install cssutils
import cssutils
import time
# Importing the required libraries
import pandas as pd
import numpy as np


# Initializing splinter browser
def init_browser():
    # if chromedriver is not in the same directory replace with actual path
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


#--------------------------------------------------------------------

#--------------------------------------------------------------------
def mars_news():
    #Initializing the browser by calling init_browser
    browser = init_browser()
    # Visit mars.nasa.gov/news
    url_to_scrape = "https://mars.nasa.gov/news/"
    browser.visit(url_to_scrape)
    # Time delay of 2 secs to make sure the browser loads
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    # Create BeautifulSoup object; parsed with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Define an array to hold the news titles
    titles = []
    # Get the first five news titles
    results = soup.find_all('div', class_="content_title", limit = 5)
    for result in results:
        try:
            title = result.find('a').text
            if title:
                titles.append(title)
        except AttributeError:
            pass
    # Save the first item as a variable news_title
    news_title = titles[0]
    # Define an array to hold the news paragraphs
    paragraphs = []
    # Get the first five news paragraphs
    results = soup.find_all('div', class_="article_teaser_body", limit = 5)
    for result in results:
        try:
            text = result.text
            if text:
                paragraphs.append(text)
        except AttributeError:
            pass
    # Save the first item as a variable news_title
    news_p = paragraphs[0]
    # Close the browser after scraping
    browser.quit()
    # Return scraped items
    return (news_title,news_p)
#--------------------------------------------------------------------
# Define a function to scrape the featured image - JPL Mars Space Image
#--------------------------------------------------------------------
def mars_featured_image():
    #Initializing the browser by calling init_browser
    browser = init_browser()
    # Visit mars.nasa.gov/news
    url_to_scrape = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_to_scrape)
    # Time delay of 2 secs to make sure the browser loads
    time.sleep(2)
    # Find the button "full image" and instantiate button click
    button = browser.find_by_id("full_image")
    button.click()
    # Scrape page into Soup
    html = browser.html
    # Create BeautifulSoup object; parsed with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Scrape the background image url
    url = cssutils.parseStyle(soup.find('article')['style'])['background-image']
    # Remove extra stuff from the url
    url = url.replace('url(','').replace(')','')
    # Define the base_url 
    base_url = 'https://www.jpl.nasa.gov'
    # Create the url for the background image
    image_url = base_url + url
    # Close the browser after scraping
    browser.quit()
    # Return scraped item
    return image_url
#--------------------------------------------------------------------
# Define a function to scrape latest Mars Weather tweet
#--------------------------------------------------------------------
def mars_weather():
    #Initializing the browser by calling init_browser
    browser = init_browser()
    # Visit mars.nasa.gov/news
    url_to_scrape = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_to_scrape)
    # Time delay of 2 secs to make sure the browser loads
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    # Create BeautifulSoup object; parsed with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Define a list to hold the tweets
    tweets = []
    # Get the first five news titles
    results = soup.find_all('div',attrs={"data-testid":"tweet"}, limit = 5)
    for result in results:
        try:
            tweet = result.text
            if tweet:
                tweets.append(tweet)
        except AttributeError:
            pass
    # Let's make sure that the first tweet contains weather information
    for tweet in tweets:
        if 'sol' and 'low' in tweet:
            first_tweet = tweet
            break
        else:
            pass
    # Remove the header from the first tweet
    first_tweet = 'I' + first_tweet.split('I')[1]
    # Close the browser after scraping
    browser.quit()
    # Return scraped item
    return first_tweet
#--------------------------------------------------------------------
# Define a function to scrape Mars facts
#--------------------------------------------------------------------
def mars_facts():
    #Initializing the browser by calling init_browser
    browser = init_browser()
    # Visit mars.nasa.gov/news
    url_to_scrape = "https://space-facts.com/mars/"
    browser.visit(url_to_scrape)
    # Time delay of 2 secs to make sure the browser loads
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    # Create BeautifulSoup object; parsed with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Get the table using attributes
    mars_table = soup.find('table', attrs={"id": "tablepress-p-mars"})
    # Let's check the rows in mars_table
    table_rows = mars_table.find_all('tr')
    # Initiate an array row_values
    row_values = []
    # Fill the array row_values
    for rows in table_rows:
        data = rows.find_all('td') # finding the elements in each row
        values = [rows.text.strip() for rows in data if rows.text.strip()]
        if values:
            row_values.append(values) # Adding elements
    # Initiate column names for the dataframe
    column_names = ["Mars Facts", "Value"]
    # Create the pandas dataframe 
    mars_df = pd.DataFrame(row_values, columns=column_names)
    # Create html table
    html_table = mars_df.to_html(classes='table table-striped',index=False)
    # Close the browser after scraping
    browser.quit()
    # Return scraped item
    return html_table
#--------------------------------------------------------------------
# Define a function to scrape Mars Hemisphere Images
#--------------------------------------------------------------------
def mars_hemispheres():
    # Define lists to store title and url links
    titles = []
    link_urls = []
    title_urls = []
    hemisphere_urls = [] 
    item_dict = {}
    #Initializing the browser by calling init_browser
    browser = init_browser()
    # Base url for the webpage
    base_url = "https://astrogeology.usgs.gov"
    # Visit mars.nasa.gov/news
    url_to_scrape = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_to_scrape)
    # Time delay of 2 secs to make sure the browser loads
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    # Create BeautifulSoup object; parsed with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Inspecting the website we see that images are wrapped in <div class="item">
    results = soup.find_all('div', class_="item")
    # Loop through returned results
    for result in results:
        try:
            # Identify and return text of image headline
            title = result.find('h3').text
            # Identify and return link of image
            link = result.find('a', class_='itemLink product-item')['href']
            # Create image url by appending to the base url
            image_url = base_url + link
            # Print results only if title and link are available
            if (title and link):
                titles.append(title)
                link_urls.append(image_url)        
        except AttributeError:
            pass
    for url in link_urls:
        # Visit the url using browser.visit method
        browser.visit(url)
        # Instantiate button click
        button = browser.find_by_id("wide-image-toggle")
        button.click()
        # Set delay for 1s to make sure the webpage loads correctly
        time.sleep(1)
        # Visit the url with wide-image
        html = browser.html
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')
        # Find the url for the wide-image
        img_url = soup.find('img',class_="wide-image")['src']
        # Combine with the base_url to create the correct url
        image_url = base_url + img_url
        # Append the list
        title_urls.append(image_url)
    for i in range(len(titles)):
        item_dict["title"] = titles[i]
        item_dict["img_url"] = title_urls[i]
        hemisphere_urls.append(item_dict.copy())
    # Close the browser after scraping
    browser.quit()
    # Return scraped item
    return hemisphere_urls

#---------------------------------------------
# Define the scraper function
#--------------------------------------------
def mars_scraper():
    # Define a dictionary to hold all the scraped data
    mars_scrape = {}
    # Get data from individual functions
    title,news_p = mars_news()
    mars_scrape["news_title"] = title
    mars_scrape["news_para"] = news_p
    mars_scrape["featured_image"] = mars_featured_image()
    mars_scrape["first_tweet"] = mars_weather()
    mars_scrape["table"] = mars_facts()
    mars_scrape["hemisphere_urls"] = mars_hemispheres()
    # Return scraped item
    return mars_scrape

# Uncomment the following code only for testing the scraper
# Following code should be commented out after testing
#mars = mars_scraper()
#for x,y in mars.items():
#   print(x,y)