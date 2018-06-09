import mysql.connector
from bs4 import BeautifulSoup
import urllib.request
import sys
import re
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def get_text(url):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    # get title
    title = soup.title.get_text()

    # get content
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()
    # preprocess text remove blank lines
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    text = " ".join(chunk for chunk in chunks if chunk)
    text = stemmer.stem(text)

    return title, text


def create_connection():
    conn = mysql.connector.connect(user='root', password='',
            host='127.0.0.1',
            database='search_engine')

    return conn


def insert_docs(conn, title, content, url):
    cursor = conn.cursor()
    add_docs = ("INSERT INTO docs "
            "(title, content, url) "
            "VALUES (%s, %s, %s)")
    data_docs = (title, content, url)
    cursor.execute(add_docs, data_docs)
    conn.commit()


def main():
    url = sys.argv[1]
    title, text = get_text(url)

    conn = create_connection()
    insert_docs(conn, title, text, url)
    conn.close()


if __name__ == "__main__":
    main()

