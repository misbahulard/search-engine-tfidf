# Search Engine Based on TF.IDF Algorithm

This is an indonesian search engine program that use tf.idf algorithm. this program built with python3, flask and MySQL.

## Installation

- clone this repo
- install the requirement library with pip:
  - flask
  - flask-wtf
  - Sastrawi
  - mysql-connector
  - beautifulsoup4
- import `search_engine.sql` to your _search_engine_ MySQL database

## Component

there are 2 main component in this program

- main search engine
- add article from url and store to database

## Run

To save the article and store to database, run `add_article.py` in tfidf directory.

```python3 add_article.py http://example.com/some_interesting_page.php```

To run the search engine, run the flask app (`app.py`) and go ahead to the `localhost:5000`.

```python3 app.py```

## Galleries

[![se1.png](https://s5.postimg.cc/r7g1ofjzb/se1.png)](https://postimg.cc/image/5l117eler/)

[![se2.png](https://s5.postimg.cc/5l117et4n/se2.png)](https://postimg.cc/image/icf7dx2wj/)