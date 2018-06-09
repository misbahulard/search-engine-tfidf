from tfidf import grep_article
import sys

def search_for(query):
    # query = input("Searching for: ")
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

        result = grep_article.get_result(keyword)
        # for res in result:
        #     print("\n", res)

        return result

# if __name__ == "__main__":
#     main()
