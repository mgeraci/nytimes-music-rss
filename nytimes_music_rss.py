from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
from operator import itemgetter
import datetime
import time
import requests

# constants
from constants import C

# secret settings
from localsettings import ARTICLES_API_KEY
from localsettings import EVENTS_API_KEY

app = Flask(__name__)


# routes
###############################################################################

@app.route('/')
def index_route(params={}):
    queries = ['ben+ratliff', 'jon+pareles']
    query_results = []
    articles = []

    # for each query, execute a request and add the results to the results list
    for i, query in enumerate(queries):
        url = generate_url(query)
        res = requests.get(url).json()
        res = format_response(res['response']['docs'])
        query_results.append(res)

    # add each article to the articles list
    for query_result in query_results:
        for article in query_result:
            articles.append(article)

    articles = sorted(articles, key=itemgetter('date'), reverse=True)

    return jsonify(**{ 'articles': articles })


# helpers
###############################################################################

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
        o['url'] = article['web_url']
        o['lead_paragraph'] = article['lead_paragraph']

        try:
            o['author'] = article['byline']['original']

        # if there is no author, don't add this article
        except Exception:
            continue

        # grab the title from the headline, if it's there
        try:
            o['title'] = article['headline']['main']

        except Exception:
            pass

        # add the publication date as a python timestamp
        # example input: 2015-11-08T00:00:00Z
        try:
            time_format = "%Y-%m-%dT%XZ"
            o['date'] = datetime.datetime.strptime(article['pub_date'], time_format)
            res.append(o)

        except KeyError:
            continue

    return res


# init
###############################################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
