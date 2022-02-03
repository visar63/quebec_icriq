# coded by V.

'''
Use this script to get Inner Links and then Inner data.

Note: Script has to be updated with proxy rotation,
and to add the part that gets inner data.
'''

import requests
from random import randint
from time import sleep
from lxml import etree
from itertools import product
from string import ascii_lowercase

def saveFile(fajlli, flegu ,respnsiii):
    with open (f'{fajlli}', flegu) as a:
        a.write(respnsiii)


# ----------------------------------------
# --> *Unique IDs*
path1 = 'companies.txt'
path2 = 'Inserted.txt'
with open(path2, 'at'): pass

try:
    with open("notIn2.txt", "wt") as w:
        l1 = {str(x).strip() for x in open(path1, 'rt')}
        l2 = {str(x).strip() for x in open(path2, 'rt')}

        l3 = set(l1) - set(l2)

        for link in l3:
            w.write(link + "\n")

    print("Link inserted %d " % (len(l2)))
    print("Link not inserted %d " % (len(l3)))
except Exception as e:
    print(e)
IDs = {str(x).strip() for x in open('notIn2.txt', 'rt')}   

# ----------------------------------------


url = "https://www.icriq.com/pls/owa_rib/ribw_recherche.rech_rap"

for letter in IDs:
    print (f'Letter: {letter}')

    payload = f"p_ecoresp=N&p_inclus_req=N&p_lang=en&p_mot_cle={letter}*&p_portail=&p_tab_alim_atpro=-1&p_type_rech=NOM"
    headers = {
        'sec-ch-ua': "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'cache-control': "no-cache",
        'postman-token': "69c56fe4-9306-4687-a40c-d1389a51e6dd",
        'cookie': 'rib_test_usager=99; rib_id_usager=40081818; captcha=true; _ga=GA1.2.687376895.1637270970; _gid=GA1.2.513113919.1637270970; prot_hash=; JSESSIONID=88F8140A21557749CF7B73B4802FAC59; COOKIE_SUPPORT=true; __utma=200439222.687376895.1637270970.1637271030.1637271030.1; __utmc=200439222; __utmz=200439222.1637271030.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=200439222.2.10.1637271030; _gat=1',
        'origin': 'https://www.icriq.com',
        'referer': 'https://www.icriq.com/pls/owa_rib/ribw_recherche.depart?p_id_req=58890467&p_code_trait=3'
        }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        if 'The company you are looking for is not listed on' in response.text:
            print (f'Not a singe company under letter: {letter} ...')
            sleep(randint(3,7))
            saveFile('Inserted.txt', 'at', letter + "\n")
        elif "403 Forbidden" in response.text:
            print(f"403 Forbidden\n")
            sleep(randint(3, 7))
        else:
            # print(response.text)
            # print("=====\n\n\n\n\n=========+")
            saveFile("aaa.html", "w", response.text)
            content_tree = etree.HTML(response.text)
            number_of_results = content_tree.xpath("//*[@class='cell_5']/text()")[0]
            # print(f"Number of results: {number_of_results}")
            for comp_link in content_tree.xpath(
                '//*[@title="Click to view the company profile"]/@href'
            ):
                comp_link = "https://www.icriq.com" + comp_link
                print(comp_link)
                saveFile(
                    "linqet3.txt",
                    "at",
                    comp_link + ",  " + letter + "\n",
                )
                ress = requests.request("POST", comp_link, headers=headers)
                if ress:
                    if "<B>NEQ</B>" in ress.text:
                        print("*** Kontenti OKKK. ***")
                        # print(ress.text)
                        saveFile(
                            "content.html",
                            "at",
                            ress.text + "\n<Visar>\n",
                        )
                        print(f"Rekorde te marrura: {count}")
                        count += 1
            saveFile("Inserted.txt", "at", letter + "\n")
            sleep(randint(3, 7))
    except Exception as e:
        print(e)
