import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import csv
import pdfkit

path = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path)

http = httplib2.Http()

all_articles = []
column_with_links = csv.reader(open('my_articles.csv', 'rb'), delimiter=',')
for row in column_with_links:
    all_articles.append(row[1])

for webpage in all_articles:
    status, response = http.request(webpage)
    if status.get('status') != '200':
        continue

    current_article = [webpage]
    nav = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('nav'))
    anchors = nav.find_all('a')

    for anchor in anchors:
        if not anchor.has_attr('class'):
            link = str(anchor['href'])
            current_article.append('http://www.cio.com.au' + link)

    # converting to PDF
    splitted_url = webpage.split('/')
    if len(splitted_url[-1]) > 6:
        file_name = splitted_url[-1]
    else:
        file_name = splitted_url[-2]

    for index, page in enumerate(current_article, start=1):
        pdfkit.from_url(page, 'my_articles_IDG/' + file_name + str(index) + '.pdf', configuration=config)
