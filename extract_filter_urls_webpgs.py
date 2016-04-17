import unicodecsv as csv
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()

links_filtered = []

for page in range(1, 42):
    # getting the web page
    status, response = http.request('http://www.cio.com.au/author/50427834/rebecca-merrett/articles?page=' + str(page))

    # passing the webpsge to BeautifulSoup
    # BeautifulSoup returns a list of anchors
    anchors = BeautifulSoup(response, parseOnlyThese=SoupStrainer('a'))
    for anchor in anchors:
        #cheking if anchor has link
        if anchor.has_attr('href'):
            #cheking if anchor has http substring
            link = str(anchor['href'])
            title = anchor.text
            if link.find('http') == -1:
                if link.find('/article') == 0:
                    full_link = 'http://www.cio.com.au' + link
                    link_with_title = (full_link, title)
                    links_filtered.append(link_with_title)


with open('my_articles.csv', 'wb') as f:
    writer = csv.writer(f, encoding='utf-8')
    for index, line in enumerate(links_filtered):
        writer.writerow([index, line[0], line[1]])
