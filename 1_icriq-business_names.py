# coded by V.

'''
Use this script to get Business Names.

Note: Script has to be updated with proxy rotation.
'''
import requests
from random import randint
from time import sleep
from lxml import etree
from itertools import product
from string import ascii_uppercase
import re

s = requests.Session()

def saveFile(fajlli, flegu ,respnsiii):
    with open (f'{fajlli}', flegu) as a:
        a.write(respnsiii)

num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
keywords = [''.join(i) for i in product(ascii_uppercase, repeat = 1)]
keywords = keywords + num
for letter in keywords:
    print (f'Letter: {letter}')

    url = "https://www.icriq.com/pls/owa_rib/ribw_liste_entr.afficher"

    querystring = {"p_index":letter,"p_lang":"en"}

    s.headers = {
        'sec-ch-ua': "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'cache-control': "no-cache",
        'postman-token': "25625b93-23e4-38cf-3f79-a16eb5525599"
        }

    response = s.request("GET", url, params=querystring)

    print(response.text)
    content = response.text
    content_tree = etree.HTML(response.text)

# print(content)
    saveFile('aaa.html', 'w', response.text)

    count = 1
    for comp_name in re.findall(r'itemprop="name" target="_blank">\s*([^<]+)\s*</A>', content, re.I|re.S):
        print (comp_name)
        saveFile('companies.txt', 'at', comp_name + "\n")
        count += 1

    nextpage = True
    while nextpage:
        if '<B>Next</B>' in content:
            print ('Next page!')
            next_page = content_tree.xpath("//b[contains(text(), 'Next')]/parent::a/@href")[0]
            next_page = "https://www.icriq.com" + next_page
            print (next_page)
            try:
                response2 = s.request("GET", next_page)
                content_tree = etree.HTML(response2.text)
                for comp_name in re.findall(r'itemprop="name" target="_blank">\s*([^<]+)\s*</A>', content, re.I|re.S):
                    print (comp_name)
                    saveFile('companies.txt', 'at', comp_name + "\n")
                    count += 1
                content = response2.text
                print (f'Crawled links: {count}')
                print ('Waiting... 5 to 10 sec...')
                sleep(randint(1,3))
            except Exception as e:
                print (e)
        else:
            nextpage = False