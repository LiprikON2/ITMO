from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session, engine
from bayes import NaiveBayesClassifier
import sqlalchemy

@route("/news")
def news_list():
    s = session()
    all_count = s.query(News).count()
    rows = s.query(News).filter(News.label == None).all()
    # Show 'empty template' if no news without a label is found
    if rows == []:
        return template('news_template_empty', all_count=all_count)
    
    return template('news_template', rows=rows, all_count=all_count, unlabeled_count=len(rows))


@route("/add_label/")
def add_label():
    s = session()
    # Find News row in db by id
    match = s.query(News).filter_by(id=request.query.id)
    if match:
        # Set label to News row from GET-request
        match[0].label = request.query.label
    s.commit()
    
    redirect("/news")


@route("/update")
def update_news():
    news_count = 0
    page = 1
    s = session()
    # Add more news until 30 new news is added
    while news_count < 30:
        news_list = get_news('https://news.ycombinator.com/newest', page)
        for news in news_list:
            # Check if news is already in db by its title and author
            if not s.query(News).filter(News.title == news.title).filter(News.author == news.author).all():
                s.add(news)
                news_count += 1
        page += 1
        print('proceding to', page)
    s.commit()
    redirect("/news")
    
@route("/drop")
def drop_table():
    s = session()
    s.query(News).delete()
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE sss

    pass


if __name__ == "__main__":
    run(host="localhost", port=8090, reloader=True)

