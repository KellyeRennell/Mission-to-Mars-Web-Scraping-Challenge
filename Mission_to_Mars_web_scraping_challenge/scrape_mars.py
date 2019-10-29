from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from pymongo import MongoClient
from time import sleep 
import time


def init_browser():
       # Path to chrome driver
   executable_path = {"executable_path": "./chromedriver.exe"}
   return Browser("chrome", **executable_path, headless=False)

def scrape():
       
   browser = init_browser()
   news_data = {}   #creating the mars_data dictionary for scraped data for Mongo DB 

  ##### Mars News ##### 
  #visit mars news url
   nasa_url = "https://mars.nasa.gov/news/"
   browser.visit(nasa_url)
   time.sleep(1)

   html = browser.html
   soup = BeautifulSoup(html, "html.parser")

#Retrieving the mars news title and news paragraph text
   nasa_news_title = soup.find_all("div", class_= "content_title")[2].get_text()
   nasa_news_p = soup.find_all("div", class_= "article_teaser_body")[2].get_text()

#close browser after completion of scraping
   browser.quit()

##### JPL Mars Space Images - Featured Image #####
   browser = init_browser()

   jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(jpl_url)
   time.sleep(1)
   html_space_images = browser.html
   soup = BeautifulSoup(html_space_images, "html.parser")

# main_jpl = "https://www.jpl.nasa.gov"
   #Retrieving space images
   space_images = soup.find_all("a", class_="fancybox")
#Retrieving space images link
   partial_url = []
   for image in space_images:
          featured_image = image['data-fancybox-href']
          partial_url.append(featured_image)
   featured_image_url = "https://www.jpl.nasa.gov" + featured_image
     
#close browser after scraping complete
   browser.quit()
   
##### Mars Weather Twitter Account #####
   browser = init_browser()

   mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
   browser.visit(mars_twitter_url)
   time.sleep(1)

   html_weather = browser.html
   mars_weather_soup = BeautifulSoup(html_weather, "html.parser")

   recent_mars_tweet = mars_weather_soup.find("div", class_="js-tweet-text-container")
   mars_weather = recent_mars_tweet.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

#close browser after scraping complete                                                
   browser.quit()

##### Mars Facts ######

   mars_facts_url = "https://space-facts.com/mars/"
# reading from url with pandas to create data table
   mars_facts_table = pd.read_html(mars_facts_url)  
#creating data frame and preparing for converting to html string
   mars_facts_df = mars_facts_table[1]
   mars_facts_df.columns = ["Description", "Values"]
   mars_facts_html = mars_facts_df.to_html()

   
##### Mars Hemispheres #####
   browser = init_browser()

   usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
   browser.visit(usgs_url)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")

#retrieving the 4 listed hemispheres data
   hemispheres = soup.find_all("div", class_="item")
#creating this empty list for the 4 hemispheres, one dictionary for each
   hemisphere_image_urls = []
# storing the main usgs url to add to the hemispheres url
   usgs_main = "https://astrogeology.usgs.gov"
# looping through the hemisphere data above
   for hemisphere in hemispheres:
         title = hemisphere.find("h3").text
         partof_url = hemisphere.find("a", class_="itemLink product-item")["href"] #finding full size image website
         browser.visit(usgs_main + partof_url) # visiting the full image site
       
         partof_url_html = browser.html    #html object for each hemisphere
         html_soup = BeautifulSoup(partof_url_html, "html.parser")

#need to grab full size image##
         img_url = usgs_main + html_soup.find("img", class_="wide-image")["src"]
          
       
#Appending image url strings into a list of dictionairies, one dictionary for each hemisphere
         hemisphere_image_urls.append({"title": title, "img_url": img_url})

   browser.quit()

#store data into a dictionary
   news_data = {
      "NASA_Mars_News_Title": nasa_news_title,
      "NASA_Mars_Paragraph_Text": nasa_news_p,
      "JPL_Featured_Image": featured_image_url,
      "Mars_Weather": mars_weather,
      "Mars_Facts": mars_facts_html,
      "Mars_Hemispheres": hemisphere_image_urls
   }

   return news_data
  

   
if __name__ == "__main__":
      mars_data = scrape()
      print(mars_data)
       
 

















