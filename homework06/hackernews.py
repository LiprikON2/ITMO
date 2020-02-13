from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    print(request.query.id, request.query.label)
    
    for news in s.query(News).filter_by(id=request.query.id):
        news.label = request.query.label
    s.commit()
    
    redirect("/news")


@route("/update")
def update_news():
    news_count = 0
    page = 1
    s = session()
    while news_count < 30:
        news_list = get_news('https://news.ycombinator.com/newest', page)
        for news in news_list:
            # Check if news is already in db by its title and author
            if not s.query(News).filter(News.title == news.title).filter(News.author == news.author).all():
                s.add(news)
                news_count += 1
        page += 1
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE sss

    pass


if __name__ == "__main__":
    run(host="localhost", port=8080, reloader = True)

