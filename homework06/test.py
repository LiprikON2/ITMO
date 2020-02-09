import requests
from bs4 import BeautifulSoup


r = requests.get("https://news.ycombinator.com/newest")
page = BeautifulSoup(r.text, 'html.parser')
print(page.body.center.table.findAll('table')[1].findAll('tr')[3].text)