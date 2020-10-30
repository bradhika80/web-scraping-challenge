from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
from selenium import webdriver
from pprint import pprint
import pandas as pd


def init_browser():
    # Setup configuration variables to enable Splinter to interact with browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return (browser)

# a method to scrape website
def scrape():

    #get the browser object
    browser = init_browser()

    news_title = None
    news_p = None

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
        gridList = news_soup.find_all('div', class_='react_grid_list grid_list_container')
       
        # get the first title
        news_title = gridList[0].find('div', class_='content_title').text

        # get the first title description
        news_p = gridList[0].find('div', class_='rollover_description_inner').text

    except Exception as ex:
        print (ex)

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
        carousel_item = image_soup.find("article", class_="carousel_item")

      
        #get the footer a element of the article
        footer_a_item = carousel_item.find("a", "button fancybox")

        # get the imageurl from the footer
        img_url = footer_a_item['data-fancybox-href']

        # remove the spaceimages 
        substring = "/spaceimages"
        featured_image_url = jpl_url + img_url.replace(substring, '')

    except Exception as ex:
        print (ex)


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
        
        #rename column names
        df = df[0].rename(columns = {0 : 'Description', 1 : 'Mars'})

        #reset the index 
        df = df.set_index('Description')

        # convert to html
        mars_fact_table = df.to_html( classes="table table-striped")
               

    except Exception as ex:
        print (ex)



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
            title_item = item.find('h3')
            if (title_item != None) :
                title  = title_item.text
            else :
                title = None

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
        print (ex)


    # close the browser object
    browser.quit()

    
    try :

        # build the scrape dictionary object
        mars_dict = {
            'news_title' : news_title,
            'news_p': news_p,
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

        # close the client connection
        client.close()

        return ("Successful")

    except Exception as ex:
        print (ex)
    
   


#  a method to retrieve data
def GetData():

    try :
        # connect to mongo server
        client = pymongo.MongoClient('mongodb://localhost:27017')
        
        # connect to database
        db = client.marsExpedition_db

        # map mars collection
        collection = db.mars 

        # read from mongo
        mars_data = collection.find()

        client.close()

        return (mars_data)


    except Exception as ex:
        print(ex)
        






    



    

    

    
    
