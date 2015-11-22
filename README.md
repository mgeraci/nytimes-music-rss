# NY Times Music RSS
This is a simple app which combines a few queries from the NY Times api into a
single RSS feed.

## Installation
Assuming that you already have pip, virtualenv, and virtualenvwrapper installed:

* clone the repo
* get an API key for the (NYTimes Articles API)['http://developer.nytimes.com']
* create a file in the project root called `localsettings.py` and add your api
  key to it with `ARTICLES_API_KEY = "your key here"`
* `mkvirtualenv nytimes_music_rss`
* `workon nytimes_music_rss`
* `pip install -r requirements.txt`
* `python nytimes_music_rss.txt`

Then you should be able to load `localhost:5000` and see the XML of the RSS
feed.

## Modifying the search
The queries that run are enumerated in a list in the file `constants.py`. The
filters that pare down the results of all those	queries is the function
`filter_articles` in (the main python file)['https://github.com/mgeraci/nytimes-music-rss/blob/master/nytimes_music_rss.py'].
