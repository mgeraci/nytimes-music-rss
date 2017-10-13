from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
from operator import itemgetter
import datetime
import time
import requests
import re


# constants
from constants import C

# the times api has a rate limit of 5 seconds between requests. this gets
# passed to `time.sleep()` below, which takes seconds
RATE_LIMIT = 5

# secret settings
from localsettings import ARTICLES_API_KEY

app = Flask(__name__)


# routes
# -----------------------------------------------------------------------------

@app.route('/')
def index_route(params={}):
    query_results = []
    articles = []

    # for each query, execute a request and add the results to the results list
    for i, query in enumerate(C['QUERIES']):
        url = generate_url(query)
        res = requests.get(url)

        try:
            res = res.json()

        except Exception:
            time.sleep(RATE_LIMIT)
            continue

        if res and res['response'] and res['response']['docs']:
            res = format_response(res['response']['docs'])
            query_results.append(res)

        time.sleep(RATE_LIMIT)

    # add each article in each result to the main articles list
    for query_result in query_results:
        for article in query_result:
            articles.append(article)

    articles = filter_articles(articles)
    articles.sort(key=itemgetter('date'), reverse=True)

    return render_template('index.xml', params = {
        'articles': articles
    })


# helpers
# -----------------------------------------------------------------------------

def generate_url(query):
    sort = 'newest'

    return '{root}?q={query}&api-key={key}&sort={sort}'.format(
        root = C['API_ROOT'],
        query = query,
        sort = sort,
        key = ARTICLES_API_KEY,
    )

def format_response(articles):
    res = []

    for article in articles:
        o = {}

        try:
            o['url'] = article['web_url']
        except Exception:
            pass

        try:
            o['lead_paragraph'] = article['lead_paragraph']
        except Exception:
            pass

        if not o.get('lead_paragraph'):
            try:
                o['lead_paragraph'] = article['snippet']
            except Exception:
                pass

        # if there is no author, don't add this article (event listing articles
        # often don't have an author)
        try:
            o['author'] = article['byline']['original']
        except Exception:
            continue

        # grab the title from the headline, if it's there
        try:
            o['title'] = article['headline']['main']
        except Exception:
            pass

        # add the publication date as a python timestamp. but if there isn't a
        # date, don't add the article. example input: 2015-11-08T00:00:00Z
        #                                             2016-12-16T20:05:45+0000
        try:
            time_format = "%Y-%m-%dT%H:%M"
            date = article['pub_date']

            # remove seconds in the SS+0000 format
            date = re.sub(r":\d{2}\+\d+$", "", date)

            # remove seconds in the :00Z format
            date = re.sub(r":\d{2}Z$", "", date)

            o['date'] = datetime.datetime.strptime(date, time_format)
        except KeyError:
            continue

        res.append(o)

    return res

def filter_articles(articles):
    res = []

    for article in articles:
        # skip spanish language articles
        if article['author'] and article['author'].find('Por') == 0:
            continue

        # skip popcasts
        if article['title'].find('Popcast') == 0:
            continue

        # skip The Playlist
        if article['title'].find('The Playlist') == 0:
            continue

        # only add articles in the arts/music section
        matches = re.search(r"\d{4}/\d{2}\/\d{2}\/arts\/music", article['url'])
        if matches == None:
            continue

        res.append(article)

    return res


# init
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
