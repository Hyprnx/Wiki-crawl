import lxml.html
import requests
import json

url = "https://datatables.net/examples/advanced_init/object_dom_read.html"
html = requests.get(url)
#print("Response from web server : \n", html)
#print("Elements:",html.text)
tree = lxml.html.fromstring(html.content)
print (tree)
rows = tree.xpath('//*[@id="example"]/tbody/tr')
print(len(rows))

name = []
age = []

for i in range(len(rows)):
    xpath1 = '//*[@id="example"]/tbody/tr[%d]/td[1]/text()' %(i+1)      #name
    xpath2 ='//*[@id="example"]/tbody/tr[%d]/td[4]/text()' %(i+1)         #age

    name_list = tree.xpath(xpath1)
    age_list = tree.xpath(xpath2)

    name.append(name_list)
    age.append(age_list)


    print('\nName: ',name[i])
    print('Age: ',age[i])

count = 0

data = []
for i in range(len(rows)):
    if len(name) > 1:
        count += 1
        info = {
            'no.': count,
            'name': name[i],
            'year': age[i]
        }
    data.append(info) 
print(data)

with open('data.json', 'w') as outfile:
    for d in data:
        json.dump(data, outfile)
        outfile.write('\n')

