from bs4 import BeautifulSoup
import mysql.connector
import urllib.request
import sys
import re
import math
from operator import itemgetter
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# create MySQL connection
def create_connection():
    conn = mysql.connector.connect(user='root', password='',
            host='127.0.0.1',
            database='search_engine')

    return conn


# get document data from DB
def get_data_docs(conn, keyword):
    param = "|".join(keyword)
    output = []

    query = "SELECT * FROM docs WHERE content REGEXP '" + param + "'"

    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        output.append(list(row))

    return output


# dapatkan hanya konten dokumen
# dan format menjadi lower case dan hilangkan karakter spesial
def get_content_and_stem(docs):
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    contents = []

    for doc in docs:
        text = doc[2]
        text = text.lower()
        text = re.sub('[^A-Za-z]+', ' ', text)
        # text = stemmer.stem(text)
        contents.append(text)

    return contents


# method for tokenize string
def tokenizing(docs):
    conjunctions = ['dan', 'serta', 'lagipula', 'tetapi', 'sedangkan', 'akan', 
            'tetapi', 'sebaiknya', 'namun', 'maupun', 'baik', 'entah', 'atau', 
            'sebelumnya', 'setelahnya', 'ketika', 'bila', 'sampai', 'demi', 'sementara', 
            'semenjak', 'tatkala', 'seraya', 'supaya', 'agar', 'untuk', 'karena', 
            'sebab', 'itu', 'ini', 'akibatnya', 'asalkan', 'jika', 'apabila', 'jadi', 'bagi',
            'kalau', 'jikalau', 'walaupun', 'biarpun', 'meskipun', 'seperti', 'bagai', 
            'bagaikan', 'ibarat', 'umpama', 'seakan-akan', 'sebagaimana', 'tetapi', 
            'sedemikian', 'sehingga', 'semakin', 'yakni', 'apalagi', 'misalnya', 'yaitu', 
            'akhirnya', 'bahwa', 'meskipun', 'kendatipun', 'sekalipun', 'lalu', 'kemudian', 
            'mula-mula', 'kecuali', 'asalkan', 'selain', 'terutama', 'umpama', 'padahal',
            'sedangkan', 'sambil', 'asal', 'pada', 'yang', 'manakala', 'sejak', 'sewaktu', 
            'dari', 'saat', 'begitu', 'seraya', 'selagi', 'selama', 'sehabis', 'selesai', 
            'sesuai', 'hingga', 'biar', 'walau', 'seolah-olah', 'maka', 'tanpa', 'dengan', 
            'bahwa', 'daripada']

    tokens = []
    for doc in docs:
        token = doc.split(" ")
        token = list(filter(None, token))
        # FILTERING
        token = [text for text in token if text not in conjunctions]
        tokens.append(token)
    
    # print("\n\nTOKENS")
    # print(tokens)

    return tokens


# method for calculate tf.idf
def tfidf(tokens):
    tables = []
    N = len(tokens)

    uniq_token = [val for token in tokens for val in token]
    uniques = sorted(list(set(uniq_token)))
    # print("\n\n\nUNIQ")
    # print(uniques)

    for token in tokens:
        table = {k:0 for k in uniques}
        for key in token:
            if key in table:
                table[key] += 1
        tables.append(table)

    # for table in tables:
    #     print("\n", table)

    # hitung df
    df_table = {k:0 for k in uniques}
    for table in tables:
        for key in table:
            if table[key] != 0:
                df_table[key] += 1

    # print("\n\nDF Table")
    # print(df_table)

    # hitung idf
    idf_table = {k:0 for k in uniques}
    for key in idf_table:
        idf_table[key] = (1 + math.log10((N / df_table[key])))

    # print("\n\nIDF Table")
    # print(idf_table)

    # tf.idf
    tfidf_table = []
    for table in tables:
        temp_table = {k:0 for k in uniques}
        for key in table:
            if table[key] != 0:
                temp_table[key] = table[key] * idf_table[key]
        tfidf_table.append(temp_table)

    # print("\n\nTFIDF Table")
    # for table in tfidf_table:
    #     print("\n", table)

    return tfidf_table


# method for search by keyword
def search_keyword(q, docs, tfidf_table):
    scores = []

    for obj in tfidf_table:
        score = 0
        for key in obj:
            if key in q:
                score += obj[key]
        scores.append(score)

    # print(scores)
    for x in range(len(scores)):
        docs[x].append(scores[x])

    sorted_doc = sorted(docs, key=itemgetter(4), reverse=True)

    # for doc in sorted_doc:
    #     print("\n\n", doc)

    return sorted_doc



def get_result(keyword):
    conn = create_connection()
    docs = get_data_docs(conn, keyword)
    conn.close()

    contents = get_content_and_stem(docs)
    tokens = tokenizing(contents)
    tfidf_table = tfidf(tokens)
    result = search_keyword(keyword, docs, tfidf_table)
    return result
