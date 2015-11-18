from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
import requests
import json

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

    # make an array of the size of the number of queries, defaulting to None
    results = [None for i in range(len(queries))]

    for i, query in enumerate(queries):
        url = generate_url(query)
        res = json.loads(requests.get(url).text)
        res = format_response(res['response']['docs'])
        results[i] = res

    return str(results)


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
        o['title'] = article['headline']['main']

        if article['byline'] != None:
            o['author'] = article['byline']['original']

        res.append(o)

    return res


# init
###############################################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
