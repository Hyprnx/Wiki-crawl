import re
import requests
from bs4 import BeautifulSoup
import json
import codecs

#well, since its kinda long and complicated to use lxml so i will scrape using beautiful soup for now

url = "https://sitde.neu.edu.vn/vi/ly-lich-can-bo-giang-vien"
html = requests.get(url)
soup = BeautifulSoup(html.text,"lxml")
#print(soup)

articles = soup.find_all("p", class_="article-thumb")
#print(len(articles))

#print(soup)

name = []
for i in range(len(articles)):
    contain = soup.find_all("h3", class_="tieu-de ellipsis ellipsis-height-48")[i].text
    name.append(contain)
    #print(contain)
print(name)

temp_href = []
for l in soup.findAll('a', attrs={'href': re.compile("ly-lich-can-bo-giang-vien/")}):
    link = l.get('href')
    #print(link)
    temp_href.append(link)

#print(temp_href)
href = []
#print((len(temp_href)))

for t in range(len(temp_href)):
    if temp_href[t] not in href:
        href.append(temp_href[t])

href.append(temp_href[(len(temp_href)-1)])


#print((len(href)))

#print(href)

url_to_add = 'https://sitde.neu.edu.vn'
for t in range(len(href)):
    href[t] = url_to_add+href[t]
    #print(href[t])

emails = []

for t in range(len(href)):
    url = href[t]
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    email = soup.findAll(text=re.compile('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'))
    #print(email)
    emails.append(email)

for t in range(len(href)):
    if emails[t] == '':
        emails[t] = "No email given"

print(emails)

data = []
count = 0
for i in range(len(articles)):
    if len(name) > 1:
        count += 1
        info = {
            'no.': count,
            'name': name[i],
            'email(s)': emails[i]
        }
    data.append(info)
print(data)

with codecs.open('data.json', 'w','utf-8-sig') as outfile:
    json.dump(data, outfile,ensure_ascii=False)
    outfile.write('\n')


