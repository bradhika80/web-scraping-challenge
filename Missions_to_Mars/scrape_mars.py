from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
from selenium import webdriver
from pprint import pprint
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# a method to scrape website
def scrape(search_term):

    #get the browser object
    browser = init_browser()

    # logic to scrape NASA Mars News
    try :
        # url for the NASA Mars News
        news_url ="https://mars.nasa.gov/news/"

        # open the url in browser
        browser.visit(news_url)

        # get the html text
        news_html = browser.html

        # parse the html into beautiful soup objects
        news_soup = BeautifulSoup(news_html, "html.parser")

        # get the div with grid of news articles
        gridList = news_soup.find('div', class_='react_grid_list grid_list_container')
        
        # get the first title
        news_title = gridList.find('div', class_='content_title').text

        # get the first title description
        news_p = gridList.find('div', class_='rollover_description_inner').text

    except Exception as ex:
        print (ex)
        return ("-1", "Error while scraping the NASA Mars News website")

    # logic to scrape JPL Mars Space Images
    try :

        # url for the JPL Mars Space Images
        jpl_url = 'https://www.jpl.nasa.gov/spaceimages'

        # open the url in browser
        browser.visit(jpl_url)

        # get the html text
        image_html = browser.html

        # parse the html into beautiful soup objects
        image_soup = BeautifulSoup(image_html,"html.parser")

        # get the carousel_item
        carousel_item = image_soup.find("article", "carousel_item")

        # get the featured_image_title
        featured_image_title = image_soup.find("h1", "media_feature_title")

        #get the footer a element of the article
        footer_a_item = carousel_item.find("a", "button fancybox")

        # get the imageurl from the footer
        img_url = footer_a_item['data-fancybox-href']

        # remove the spaceimages 
        substring = "/spaceimages"
        featured_image_url = jpl_url + img_url.replace(substring, '')

    except Exception as ex:
        print(ex)
        return ("-1", "Error while scraping the JPL Mars Space Images - Featured Image website")

    # logic to scrape  Mars Facts
    try :

        # url for the JPL  Mars Facts
        space_url = 'https://space-facts.com/mars/'

        # open the url in browser
        browser.visit(space_url)

        # get the html text
        space_html = browser.html

        # parse the html into beautiful soup objects
        space_soup = BeautifulSoup(space_html,"html.parser")

        #reference :- https://pythonprogramminglanguage.com/web-scraping-with-pandas-and-beautifulsoup/

        # get the table element from the page. 
        table_item  = space_soup.find("table", "tablepress tablepress-id-p-mars")

        # read the html and convert to dataframe
        df = pd.read_html(str(table_item))

        # convert to html
        mars_fact_table = df[0].to_html(index = False,header=False)

    except Exception as ex:
        print(ex)
        return ("-1", "Error while scraping the Mars Facts website")


    # logic to scrape  Mars Hemispheres
    try :
        
        # url for the Mars Hemispheres
        astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        # open the url in browser
        browser.visit(astro_url)

        # get the html text
        astro_html = browser.html

        # parse the html into beautiful soup objects
        astro_soup = BeautifulSoup(astro_html,"html.parser")

        # get the mars image urls
        base_url = "https://astrogeology.usgs.gov"

        # get the mars image items
        mars_items = astro_soup.find_all("div", "item")   

        # list of image dict objects
        hemisphere_image_urls  = []

        # iterate through the mars image list
        for item in mars_items :

            # get the title for image
            title = item.find('h3').text

            #url for the image 
            item_url =  item.find("a")["href"]
            link_url = base_url + item_url

            # open the page in the browser
            browser.visit(link_url)

            # get the html text
            page_html = browser.html

            # parse the html into beautiful soup objects
            page_soup = BeautifulSoup(page_html,"html.parser")
            
            # get the image_item
            image_item = page_soup.find('div', 'downloads')

            # get the image url
            image_url = image_item.find('a')['href']    
            
            # build the dictionary
            mars_dict = { "title": title, "img_url": image_url}

            # add the dictionary to the list
            hemisphere_image_urls.append(mars_dict)    

    except Exception as ex:
        print(ex)
        return ("-1", "Error while scraping the Mars Hemispheres website")

        # close the browser object
        browser.quit()

    
    try :

        # build the scrape dictionary object
        mars_dict = {
            'news_title' : news_title,
            'news_p': news_p,
            'featured_image_Title': featured_image_title,
            'featured_image_url': featured_image_url,
            'mars_fact_table': mars_fact_table,
            'hemisphere_image_urls': hemisphere_image_urls
        }

        # connect to mongo server
        client = pymongo.MongoClient('mongodb://localhost:27017')
        
        # connect to database
        db = client.marsExpedition_db

        # map mars collection
        collection = db.mars 

        # drop the collection
        collection.drop()

        #insert the dictionary the collection
        collection.insert_one(mars_dict)

    except Exception as ex:
        print(ex)
        return ("-1", "Error while inserting record into mongo collection")
    
    print ("0", "Scraping website successful")


#  a method to retrieve data
def GetData ():

    try :
         # connect to mongo server
        client = pymongo.MongoClient('mongodb://localhost:27017')
        
        # connect to database
        db = client.marsExpedition_db

        # map mars collection
        collection = db.mars 

        # read from mongo
        mars_data = collection.find()

        return ("0", mars_data)


    except Exception as ex:
        print(ex)
        return ("-1", "Error while inserting record into mongo collection")






    



    

    

    
    
