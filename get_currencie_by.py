import requests
import json
import text

a = json.loads(requests.get(text.url_nbrb_cur).content)
b = json.loads(requests.get(text.url_nbrb_all).content)

def get_currencie():
    currencie = {}
    for i in a:
        currencie[i['Cur_Abbreviation']] = [i['Cur_Scale'], i['Cur_Name'], i['Cur_OfficialRate']]
        for j in b:
            if j['Cur_Abbreviation'] == i['Cur_Abbreviation']:
                currencie[j['Cur_Abbreviation']].append(j['Cur_Name'])
                currencie[j['Cur_Abbreviation']].append('BYN')
                break

    currencie['BYN'] = [1, 'Беларусский рубль', 1, 'Беларусский рубль', 'BYN']
    sorted_tuples = sorted(currencie.items(), key=lambda item: item[1][3])
    currencie = {k: v for k, v in sorted_tuples}
    return currencie
