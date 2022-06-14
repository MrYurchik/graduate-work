import pdb

import requests
import json
from bs4 import BeautifulSoup

response = requests.get(
    'http://wiki.lp.edu.ua/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D0%B0%D1%84%D0%B5%D0%B4%D1%80#.D0.86.D0.BD.D1.81.D1.82.D0.B8.D1.82.D1.83.D1.82_.D0.B0.D1.80.D1.85.D1.96.D1.82.D0.B5.D0.BA.D1.82.D1.83.D1.80.D0.B8')
soup = BeautifulSoup(response.text, 'html.parser')


def check_get(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    box = soup.select_one('.infobox')
    if not box:
        print('ВЖЕ НЕ ІСНУЄ')
        return
    for desc in box.select('tr'):
        if desc.select_one('th'):
            title = desc.select_one('th').text
            text = desc.select_one('td').text
            if 'ліквідації' in title:
                print('ВЖЕ НЕ ІСНУЄ')
                return
            if 'Розташування' in title:
                place = text
                print(place)
                return place
        else:
            continue


info_list = list()
for item in soup.select('li'):
    if ';' in item or '.' in item:

        if len(item.select('a')) > 1:
            pdb.set_trace()
        print('http://wiki.lp.edu.ua' + item.select('a')[0]['href'], item.select('a')[0]['title'])
        checked = check_get('http://wiki.lp.edu.ua' + item.select('a')[0]['href'])
        if checked:
            ifn = {"link": 'http://wiki.lp.edu.ua' + item.select('a')[0]['href'], "desc": checked, "build": "",
                   "title": item.select('a')[0]['title']}

            info_list.append(ifn)
with open('kafedri.json', 'a', encoding='UTF-8') as file:
    file.write(str(info_list))

print(len(info_list))
