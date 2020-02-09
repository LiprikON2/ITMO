import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import re
from pprint import pprint as pp

import db

def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    # for headline in 
    headlines = parser.body.center.table.findAll('table')[1].findAll('tr', {'class': 'athing'})
    for headline in headlines:
        
        # Extract headline's title
        title = headline.findChild('a', {'class': 'storylink'}).text
        # Skip deleted headlines
        if title == '[deleted]':
            continue
        
        
        # Extract headline's link and fix internal site links
        if headline.findChild('a', {'class': 'storylink'}).has_attr('rel'):
            url = headline.findChild('a', {'class': 'storylink'}).get('href')
        else:
            url = "https://news.ycombinator.com/" + headline.findChild('a', {'class': 'storylink'}).get('href')
            
        domain = "{0.scheme}://{0.netloc}/".format(urlsplit(url))


        # Subtext contains info about author, number of upvotes and comments
        subtext = headline.find_next_siblings('tr')[0].find('td', {'class': 'subtext'})

        
        # Extract headline's author
        author = subtext.find('a', {'class': 'hnuser'}).text


        # Extract number of upvotes from text
        upvotes_text = subtext.find('span', {'class': 'score'}).text
        upvotes = int(re.findall(r'\d+', upvotes_text)[0])
        
        
        # Extract number of comments from text
        comments_text = subtext.findAll('a')[-1].text
        comments = re.findall(r'\d+', comments_text)
        if not comments:
            comments = 0
        else:
            comments = int(comments[0])
           
        news = db.News(
            title=title,
            author=author,
            url=url,
            domain=domain,
            upvotes=upvotes,
            comments=comments
        ) 
        # news = {
        #     'title': title,
        #     'author': author,
        #     'url': url,
        #     'domain': domain,
        #     'upvotes': upvotes,
        #     'comments': comments
        # }
        news_list.append(news)
        s.add(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.select('.morelink')[0].get('href')


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

if __name__ == '__main__':
    s = db.session()
    
    news = get_news('https://news.ycombinator.com/newest', 34)
    
    s.commit()
    
    