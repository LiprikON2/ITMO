import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import re
from pprint import pprint as pp

def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    # for headline in 
    headlines = parser.body.center.table.findAll('table')[1].findAll('tr', {'class': 'athing'})
    for headline in headlines:
        
        title = headline.findChild('a', {'class': 'storylink'}).text
        
        
        url = headline.findChild('a', {'class': 'storylink'}).get('href')
        domain = "{0.scheme}://{0.netloc}/".format(urlsplit(url))

        # Subtext contains info about author, number of upvotes and comments
        subtext = headline.find_next_siblings('tr')[0].find('td', {'class': 'subtext'})

        # Extract story's author
        author = subtext.find('a', {'class': 'hnuser'}).text


        upvotes_text = subtext.find('span', {'class': 'score'}).text
        # Extract number from text
        upvotes = re.findall(r'\d+', upvotes_text)[0]
        
        
        comments_text = subtext.findAll('a')[-1].text
        # Extract number of comments from text
        comments = re.findall(r'\d+', comments_text)
        if not comments:
            comments = 0
        else:
            comments = comments[0]
            
        news = {
            'title': title,
            'url': url,
            'domain': domain,
            'author': author,
            'upvotes': upvotes,
            'comments': comments
        }
        news_list.append(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    pass


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        # next_page = extract_next_page(soup)
        # url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

if __name__ == '__main__':
    get_news('https://news.ycombinator.com/newest')