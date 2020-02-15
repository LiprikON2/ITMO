from bottle import (
    route, run, template, request, redirect, static_file
)

from scraputils import get_news
from db import News, session, engine
from bayes import NaiveBayesClassifier
import sqlalchemy


@route('/all')
def all_news():
    s = session()
        
    count = count_news(s)
    
    rows = s.query(News).all()
    if rows == []:
        return template('./templates/news_empty', count=count)
    
    return template('./templates/news_all', rows=rows, count=count)


@route("/unlabeled")
def unlabeled_news():
    s = session()
    
    count = count_news(s)
    
    rows = s.query(News).filter(News.label == None).all()
    # Show 'empty template' if no news without a label is found
    if rows == []:
        return template('./templates/news_empty', count=count)
    
    return template('./templates/news_unlabeled', rows=rows, count=count)

@route("/upvoted")
def upvoted_news():
    s = session()
    
    count = count_news(s)
    
    rows = s.query(News).filter(News.label == 'upvote').all()
    # Show 'empty template' if no news without a label is foundsssss
    if rows == []:
        return template('./templates/news_empty', count=count)
    
    return template('./templates/news_upvoted', rows=rows, count=count)

@route("/maybe")
def maybe_news():
    s = session()
    
    count = count_news(s)
    
    rows = s.query(News).filter(News.label == 'maybe').all()
    # Show 'empty template' if no news without a label is foundsssss
    if rows == []:
        return template('./templates/news_empty', count=count)
    
    return template('./templates/news_maybe', rows=rows, count=count)

@route("/downvoted")
def downvoted_news():
    s = session()
    
    count = count_news(s)
    
    rows = s.query(News).filter(News.label == 'downvote').all()
    # Show 'empty template' if no news without a label is foundssssssssss
    if rows == []:
        return template('./templates/news_empty', count=count)
    
    return template('./templates/news_downvoted', rows=rows, count=count)


@route("/add_label/")
def add_label():
    s = session()
    # Find News row in db by id
    match = s.query(News).filter_by(id=request.query.id)
    if match:
        # Set label to News row from GET-request
        match[0].label = request.query.label
    s.commit()
    
    handle_redirect(request.query.redirected_from)
        
@route("/remove_label/")
def remove_label():
    s = session()
    
    # Find News row in db by id
    match = s.query(News).filter_by(id=request.query.id)
    if match:
        match[0].label = None
    
    s.commit()
    
    handle_redirect(request.query.redirected_from)
    
        
def handle_redirect(redirected_from):
    # Redirect page back
    if redirected_from == 'all':
        redirect("/all")
    elif redirected_from == 'upvoted':
        redirect("/upvoted")
    elif redirected_from == 'maybe':
        redirect("/maybe")
    elif redirected_from == 'downvoted':
        redirect("/downvoted")
    else:
        redirect("/unlabeled")


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
    redirect("/unlabeled")

@route("/drop")
def drop_table():
    s = session()
    s.query(News).delete()
    s.commit()
    redirect("/unlabeled")


@route("/classify")
def classify_news():
    # PUT YOUR CODE sss
    pass

def count_news(s) -> dict:
    
    count = {
        'all': s.query(News).count(),
        'unlabeled': s.query(News).filter(News.label == None).count(),
        'upvoted': s.query(News).filter(News.label == 'upvote').count(),
        'maybe': s.query(News).filter(News.label == 'maybe').count(),
        'downvoted': s.query(News).filter(News.label == 'downvote').count(),
    }
    
    return count

# For improting css and javacript files into templates
# Ref: https://stackoverflow.com/questions/6978603/how-to-load-a-javascript-or-css-file-into-a-bottlepy-template
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


if __name__ == "__main__":
    run(host="192.168.0.196", port=8090, reloader=True)

