
from surah import suralar_info
import requests
from pprint import pprint
url = "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.min.json"


def sura_info(sura_raqami):
    
    tartib = int(sura_raqami)
    return suralar_info[tartib]

def sura_top(a):

    url1 = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{a}.min.json"
   
    r = requests.get(url1).json()
    sura = r['chapter']
    text = ''
    for a1 in sura:
        text += str(a1['verse']) + '.  ' + a1['text'] + '\n'*2
    return  text

def oyat_top(a1, a2):
    # a1 - sura raqami
    # a2 - oyat raqami 
    url2 = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{a1}/{a2}.min.json"
    r = requests.get(url2)
    r = r.json()
    text = r['text']
    return text

def oyat_soni(sura_raqami):
    
    url3 = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{sura_raqami}.min.json"
   
    r = requests.get(url3).json()
    sura = r['chapter']
    return len(sura)






# if __name__ == '__main__':
#     print("asdas\n"*20)
#     print(oyat_soni(3))
    
    # print(str('olma'))
    
    # print(oyat_top(1, 1))
    # print(oyat_top(1, 2))
    
    # sura = sura_top('yunus')
    # print(sura)
    # print(suralar_info[1])
    # r = requests.get(url)
    # quron = r.json()
    # print(quron)