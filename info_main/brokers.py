# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_brokers():
    url = 'https://www.sravni.ru/invest/brokerskoe-obsluzhivanie/rating/'
    req = requests.get(url)
    response = req.text
    soup = BeautifulSoup(response, 'lxml')
    s_list = list()
    br = soup.find_all('div', class_='style_row__uzjMQ style_mainGrid__mhMKz')
    print(len(br))
    for b in br[:11]:
        print(1)
        print(b.find('div', class_='style_column__HWYzl').find('span', class_='style_caption__cqSsy'))
        name = b.find('div', class_='style_column__HWYzl').find('span', class_='style_caption__cqSsy').text
        # print(b.find('span', class_='style_caption__cqSsy'))
        comision = b.find('div', class_='style_range__cjBhD').text
        href = b.find('a').get("href")
        msg = f'📍 Брокер и лицензия: {str(name)} <br>' + \
              f'     📉 Комиссия за операцию: {comision}<br>' \
              f'     🔗 Ссылка на сайт брокера: {href}<br>'
        s_list.append(msg)

    return s_list


# get_brokers()