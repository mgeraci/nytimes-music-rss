from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Response
import requests

# constants
from constants import C

# secret settings
from localsettings import ARTICLES_API_KEY
from localsettings import EVENTS_API_KEY

app = Flask(__name__)

@app.route('/')
def index_route(params={}):
    sort = 'newest'
    q = 'ben+ratliff'
    url = '{root}?q={query}&api-key={key}&sort={sort}'.format(
        root = C['API_ROOT'],
        query = q,
        sort = sort,
        key = ARTICLES_API_KEY,
    )

    r = requests.get(url)
    return Response(r.text, mimetype='text/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
