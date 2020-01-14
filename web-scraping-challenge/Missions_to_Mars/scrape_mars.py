from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    obj = ScrapeMars(browser)

    news_title, news_teaser = obj.mars_news()
    featured_image_url = obj.mars_images()
    mars_weather = obj.mars_weather()
    mars_facts = obj.mars_facts()
    hemisphere_image_urls = obj.mars_hemispheres()

    # Run the functions below and store into a dictionary
    results = {
        "title": news_title,
        "teaser": news_teaser,
        "image_URL": featured_image_url,
        "weather": mars_weather,
        "facts": mars_facts,
        "hemispheres": hemisphere_image_urls
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results


class ScrapeMars:
    def __init__(self, browser_instance):
        self.url_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        self.url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        self.url_weather = 'https://twitter.com/marswxreport?lang=en'
        self.url_facts = 'https://space-facts.com/mars/'
        self.url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        self.browser = browser_instance

    def mars_news(self):
        '''
        NASA Mars News
        '''

        self.browser.visit(self.url_news)

        html = self.browser.html
        soup = bs(html, 'lxml')
        title = soup.find('div', class_="content_title").text.strip()
        news_p = soup.find('div', class_="article_teaser_body").text.strip()

        return title, news_p

    def mars_images(self):
        '''
        JPL Mars Space Images - Featured Image
        '''

        self.browser.visit(self.url_images)
        html = self.browser.html
        soup = bs(html, 'lxml')

        image = soup.find("img", class_="thumb")["src"]

        return image

    def mars_weather(self):
        '''
        Mars Weather
        '''

        self.browser.visit(self.url_weather)
        html = self.browser.html
        soup = bs(html, 'lxml')
        weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

        return weather

    def mars_facts(self):
        '''
        Mars Facts
        '''
        # Scrape the table of Mars facts
        tables = pd.read_html(self.url_facts)
        df_profile = tables[0]
        df_profile.columns = ['Aspect', 'Value']

        # Convert to HTML table string
        df_profile.to_html('mars_profile.html')

        return df_profile

    def mars_hemispheres(self):
        '''
        Mars Hemispheres
        '''
        self.browser.visit(self.url_hemispheres)
        html = self.browser.html
        soup = bs(html, 'lxml')

        mars_hemispheres = []
        links = soup.find_all('h3')

        for link in links:
            mars_hemispheres.append(link.text)

        image_urls = []
        data = {}

        for link in mars_hemispheres:
            data['title'] = link

            self.browser.click_link_by_partial_text(link)
            data['image_url'] = self.browser.links.find_by_partial_text('Sample')['href']

            image_urls.append(data)

            self.browser.back()

        return image_urls


if __name__ == '__main__':
    scrape()
