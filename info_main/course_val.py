# -*- coding: utf-8 -*-

import requests
import json
import datetime as dt



def get_course():
    dot = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

    # URL = "https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC"
    URL = "https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC"
    old_price = 0
    j = requests.get(URL)
    data = json.loads(j.text)
    price = data['result']['Ask']

    uah = int(dot['Valute']['CNY']['Value'])
    kazah = int(dot['Valute']['KZT']['Value'])
    euro = int(dot['Valute']['EUR']['Value'])
    dollar = int(dot['Valute']['USD']['Value'])
    return [f'💶 Цена за €:  {euro} ₽', f'💴 Цена за KZT:  {kazah / 100} ₽', f'💴 Цена за ¥:  {uah} ₽', f'💵 Цена за $:  {dollar} ₽', f'Цена за BTC:  {price} $']
    # price = f'💶 Цена за €:  {euro} ₽\n💴 Цена за KZT:  {kazah / 100} ₽\n💴 Цена за ¥:  {uah} ₽\n💵 Цена за $:  {dollar} ₽\n🪙 Цена за BTC:  {price} $\n'

# print(get_course())