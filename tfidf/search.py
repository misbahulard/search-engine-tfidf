""" 
search.py is for search from keyword that user pass, and return the result 
first, keyword is looked up in index file (index.txt) to filter the keyword
is exist or not. And then if exist use tf.idf to get the relevant document

"""

from tfidf import calculate_tfidf
import sys

def search_for(query):
    query = query.split(" ")

    # read index file
    indices = []
    with open('tfidf/index.txt', 'r') as filehandle:
        indices = [keyword.rstrip() for keyword in filehandle.readlines()]
 
    keyword = []

    for index in indices:
        if index in query:
            keyword.append(index)

    if len(keyword) == 0:
        print("Not found!")
        return []
    else:
        print("You search: ")
        print(keyword)

        result = calculate_tfidf.get_result(keyword)

        return result
