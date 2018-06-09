import mysql.connector
import re
from operator import itemgetter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# create MySQL connection
def create_connection():
    conn = mysql.connector.connect(user='root', password='',
            host='127.0.0.1',
            database='search_engine')

    return conn


# get document data from DB
def get_data_docs(conn):
    output = []

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM docs")
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

    return tokens


def get_index(tokens):
    uniq_token = [val for token in tokens for val in token]
    uniques = sorted(list(set(uniq_token)))
    return uniques

def main():
    conn = create_connection()
    docs = get_data_docs(conn)
    conn.close()

    contents = get_content_and_stem(docs)
    tokens = tokenizing(contents)
    indices = get_index(tokens)

    # save to file
    with open('index.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % keyword for keyword in indices)

    print("Indexing success!")
    
    # indicies = []
    # with open('index.txt', 'r') as filehandle:
    #     indicies = [keyword.rstrip() for keyword in filehandle.readlines()]


if __name__ == "__main__":
    main()

