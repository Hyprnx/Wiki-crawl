import re
import requests
from bs4 import BeautifulSoup
import json
import codecs
import time
import pymongo

def scrape_link(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    return soup


def get_data(url, container, attributes):
    to_find = scrape_link(url).find(container, attrs=attributes)
    return to_find


def check_living(url):
    soup = scrape_link(url)
    tags = soup.find('div', attrs={'id': 'mw-normal-catlinks'})
    txt = re.compile('Living people')
    if tags.find(text=txt):
        return True
    else:
        return False


def join_str(str1, str2):
    return str1 + str2


def process_cal(counter_variable, str):
    if (counter_variable+1) < len(str):
        percentage = round(((counter_variable+1)/len(str)*100), 2)
        print("Running ", percentage,"% finished", sep='')

    elif (counter_variable+1) == len(str):
        percentage = round(((counter_variable + 1) / len(str) * 100), 2)
        print("Running ", percentage, "% finished", sep='')
        print("\n\nFINISHED\n\n")
    else:
        print("ERRORS")


def main():
    t = time.time()
    url = "https://en.wikipedia.org/wiki/Category:People_of_Vietnamese_descent"
    scrape_link(url)
    data = scrape_link(url).findAll('div', attrs={'class': "CategoryTreeSection"})
    print("letters:", len(data))

    #find all divs that contain the class "CategoryTreeSection"
    #"CategoryTreeSection" is a div that contains the link to more details link
    #"CategoryTreeSection" located in a div, class "mw-category-group"

    href = []

    data_link = []
    data_name = []
    data_nationality = []
    data_age = []
    data_occupation = []

    url_to_add = 'https://en.wikipedia.org'
    for l in scrape_link(url).findAll('a', attrs={'href': re.compile("of_Vietnamese_descent$")}):
        link = l.get('href')
        if link.startswith('https:'):
            continue
        else:
            link = join_str(url_to_add,link)
            get_link = get_data(link ,'div',{'id': 'mw-pages'} )
            if get_link:
                data_in_link = get_link.find_all('div', attrs={'class': 'mw-content-ltr', 'lang': "en", 'dir': "ltr"})
                for data in data_in_link:
                    a_tag = data.find_all('a')
                    for a in a_tag:
                        if ('Vietnamese' in a.attrs['href']) == False:
                            people_link = join_str(url_to_add,a.attrs['href'])
                            href.append(people_link)

    for i in range (0,len(href)):
        soup = scrape_link(href[i])
        name = soup.find('h1',{'id': 'firstHeading', 'class':'firstHeading','lang':'en'}).text
        data = soup.find('div',{'id':'mw-normal-catlinks'})

        if check_living(href[i]) == True:
            data_name.append(name)
            data_link.append(href[i])

            if data.find(text=re.compile('people of Vietnamese descent')):
                nationality_tag = data.find(text = re.compile('\speople of Vietnamese descent')).split()
                nationality = nationality_tag[:-4]
                nationality = str(nationality)
                data_nationality.append(nationality)

            txt = re.compile('births')
            if data.find(text=txt):
                a_tags = data.findAll('a')
                for a in a_tags:
                    a = a.text
                    if a.endswith('births'):
                        birthyear = a.split(" ")
                        data_age.append(birthyear[0])
            else:
                data_age.append("No birthyear found")
        process_cal(i,href)

    count = 0
    json_write_file = []
    for i in range(0,len(data_link)):
        if len(data_link[i]) > 1:
            count += 1
            info ={
                'no': count,
                'Name': data_name[i],
                'Wikipedia Link': data_link[i],
                'Citizen status': data_nationality[i],
                'Born period:': data_age[i]
            }
        json_write_file.append(info)

    with codecs.open('data.json', 'w', 'utf-8-sig') as outfile:
        json.dump(json_write_file, outfile, indent= 4, ensure_ascii=False)
    outfile.close()

    cluster = pymongo.MongoClient(
        "mongodb+srv://db_admin:adminpassword@testdb.uywxs.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = cluster["test"]
    col = db["test"]

    col.insert_many(json_write_file)

    print("Done in ", time.time() - t)

if __name__ == "__main__":
    main()










