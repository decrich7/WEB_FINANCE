# -*- coding: utf-8 -*-

import requests


def get_liders():
    url = 'https://bcs-express.ru/webapi2/api/quotes/leaders?delay=true&datefilter=month&volume=more3kk&portfolioId=0'
    req = requests.get(url)
    get_json = req.json()
    leaders_up = get_json.get("up")
    leaders_down = get_json.get("down")
    ld_up = list()
    ld_down = list()
    for lead in leaders_up:
        msg = [lead.get("shortName"),round(float(lead.get("change")), 2), float(lead.get("value")),
               'https://bcs-express.ru/kotirovki-i-grafiki' + lead.get(
            "hyperlink")]
        ld_up.append(msg)

    for lead in leaders_down:
        # msg = f'📌 Название акционерного общества: {lead.get("shortName")}<br>' + \
        #       f'⬇   Изменение цены: {round(float(lead.get("change")), 2)} %<br>' + \
        #       f'💵  Цена акции: {float(lead.get("value"))} ₽<br>' + \
        #       f'🔎  Подробная информация - ' + 'https://bcs-express.ru/kotirovki-i-grafiki' + lead.get(
        #     "hyperlink") + '<br>'
        msg = [lead.get("shortName"),round(float(lead.get("change")), 2), float(lead.get("value")),
               'https://bcs-express.ru/kotirovki-i-grafiki' + lead.get(
            "hyperlink")]
        ld_down.append(msg)
    # up = '\n'.join(ld_up[:5])
    # down = '\n'.join(ld_down[:5])
    return (ld_up[:5], ld_down[:5])


print(get_liders()[-1])
