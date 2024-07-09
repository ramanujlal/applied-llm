import newspaper
import feedparser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# RSS Feeds sources
# The Economic Times:
# https://b2b.economictimes.indiatimes.com/rss
#
# The Times of India:
# https://timesofindia.indiatimes.com/rssfeedstopstories.cms

# Some useful articles:
# https://www.newscatcherapi.com/blog/python-web-scraping-libraries-to-mine-news-data


def get_text_from_url(url: str) -> str:

    # Configure Selenium to use a headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Provide the path to the ChromeDriver executable
    webdriver_service = Service(r'D:\Dev\chromedriver-win64\chromedriver.exe')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Fetch the webpage
    driver.get(url)

    # Get the page source and parse it with BeautifulSoup
    webpage_content = driver.page_source
    soup = BeautifulSoup(webpage_content, 'html.parser')

    text = soup.text

    # # Extract the data (all links in this example)
    # links = soup.find_all('a')
    #
    # for link in links:
    #     print(link.get('href'))

    # Close the WebDriver
    driver.quit()

    return text


def get_text_from_rss(rss_url: str) -> str:
    feed = feedparser.parse(rss_url)

    print('Number of RSS posts :', len(feed.entries))

    entry = feed.entries
    print('Post Title :', entry.title)

    return feed


def get_content_from_url(url_link: str) -> str:

    # create a newspaper article object
    article = newspaper.Article(url_link)

    # download and parse the article
    article.download()
    article.parse()

    # extract relevant information
    return article.text


def scrape_news_from_feed(feed_url):

    contents = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        content = get_content_from_url(entry.link)
        contents.append(content)

    return contents





if __name__ == "__main__":

    # news_link = f"""
    #     https://timesofindia.indiatimes.com/rssfeedstopstories.cms
    #     """

    # feed_url = 'http://feeds.bbci.co.uk/news/rss.xml'
    feed_url = 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms'
    articles = scrape_news_from_feed(feed_url)

    # print the extracted articles
    for article in articles:
        print(article)






