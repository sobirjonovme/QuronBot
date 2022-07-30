
from surah import suralar_info
import json
#from pprint import pprint

fayl_nomi = "quron.json"


def sura_info(sura_raqami):
    tartib = int(sura_raqami)
    return suralar_info[tartib]


def oyat_top(a1, a2):
    # a1 - sura raqami
    # a2 - oyat raqami 
    a1, a2 = int(a1)-1, int(a2)-1

    with open(fayl_nomi, "r") as f:
        data = json.load(f)
    if a1 < 114:
        if a2 < len(data["quron"][a1]):
            result = data["quron"][a1][a2]
            text = result['text']
            return text

    return False

def oyat_soni(sura_raqami):

    sura_raqami = int(sura_raqami)-1

    with open(fayl_nomi, "r") as f:
        data = json.load(f)
    result = data["quron"][sura_raqami]
    
    return len(result)






#if __name__ == '__main__':
#     print("asdas\n"*20)
    #print(oyat_soni(37))
    
    # print(str('olma'))
    
    #print(oyat_top(17, 5))
    # print(oyat_top(1, 2))
    
    # sura = sura_top('yunus')
    # print(sura)
    # print(suralar_info[1])
    # r = requests.get(url)
    # quron = r.json()
    # print(quron)