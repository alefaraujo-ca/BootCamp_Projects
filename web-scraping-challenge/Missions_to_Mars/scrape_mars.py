from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd

def scrape():
    executable_path={'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')
    table=soup.find('div', class_='grid_layout')
    rows=table.find_all('li')

    pre_df=[]
    columns=['date', 'title', 'content']
    for row in rows[0:]:
        news_dict={}
        cells=row.find('div', class_="list_text")

        for i, cell in enumerate(cells):
            news_dict[columns[i]]=cell.text.strip()
            #print(i, cell.text.strip())
            if i==2:
                pre_df.append(news_dict)

    df_news_nasa=pd.DataFrame(pre_df, columns=columns)

    # JPL Mars Space Images - Featured Image

    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    image = soup.find("img", class_="thumb")["src"]

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'lxml')
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # Mars Facts

    # Scrape the table of Mars facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df_profile = tables[0]
    df_profile.columns = ['Aspect', 'Value']

    # Convert to HTML table string
    df_profile.to_html('mars_profile.html')

    # Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    mars_hemispheres = []
    links = soup.find_all('h3')

    for link in links:
        mars_hemispheres.append(link.text)

    hemisphere_image_urls = []
    data = {}

    for link in mars_hemispheres:
        
        data['title'] = link

        browser.click_link_by_partial_text(link)
        data['image_url'] = browser.find_by_text('Sample')['href']

        hemisphere_image_urls.append(data)
        
        browser.back()
