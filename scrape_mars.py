#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd



def scrape_news(browser):
    #Visit url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Convert browser html to soup object
    html = browser.html
    news_soup = bs(html, 'html.parser')

    #Create empty lists for titles and paragraphs
    titles=[]
    news_p=[]

    #Assign titles to variable
    title_search=news_soup.find_all('div', class_='content_title')
    for title in title_search:
        titles.append(title.text.strip())

    #Assign paragraphs to variable
    p_search=news_soup.find_all('div', class_='article_teaser_body')
    for p in p_search:
        news_p.append(p.text.strip())

    return titles, news_p


def scrape_image(browser):  
    #Visit url
    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_1)

    #Find full size image
    browser.click_link_by_partial_text('FULL IMAGE')

    #Find full size image
    browser.click_link_by_partial_text('more info')

    #Convert browser html to soup object
    html_1 = browser.html
    pic_soup = bs(html_1, 'lxml')

    #Find featued image url
    results=pic_soup.find('figure', class_='lede')
    featured_path=results.a['href']
    featured_image_url='https://www.jpl.nasa.gov'+featured_path

    return featured_image_url

def scrape_facts():
    #Enter url
    url_2 = 'https://space-facts.com/mars/'

    #Use pandas to scrape table
    tables = pd.read_html(url_2)

    #Select table and clean up
    mars_df=tables[0]
    mars_df.columns=["Description", 'Mars']
    mars_df.set_index("Description", inplace=True)

    #Covert table to html string
    return mars_df.to_html()

def scrape_hemispheres(browser):
    #Visit url
    url_3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_3)

    hemisphere={}
    hemisphere_img_urls=[]
    var=browser.find_by_css('a.product-item h3')

    for i in range(len(var)):
        browser.find_by_css('a.product-item h3')[i].click()
        element=browser.links.find_by_text('Sample').first
        element_title=browser.find_by_css('h2.title').first
        hemisphere['img_url']=element['href']
        hemisphere['title']=element_title.value
        hemisphere_img_urls.append(hemisphere)
        browser.back()

    return hemisphere_img_urls

def scrape_all():

    #Set path and initialize chrome borwser 
    executable_path = {'chromedriver.exe'}
    browser = Browser('chrome', executable_path, headless=False)

    titles, news_p = scrape_news(browser)
    # featured_image_url=scrape_image(browser)
    mars_df=scrape_facts()
    hemi=scrape_hemispheres(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": titles,
        "news_paragraph": news_p,
        # "featured_image": featured_image_url,
        "facts": mars_df,
        "hemispheres": hemi
    }

    # Stop webdriver and return data
    browser.quit()
    return data


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())




