def get_words():
    with open('data/words.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    return data


import json

eng = open('MUST Relationship 6 (1).txt', 'r').readlines()
rus = open('MUST Relationship 6.txt', 'r', encoding='UTF-8').readlines()
dict_n = get_words()
print(len(dict_n.keys()))
for i in range(len(eng)):
    eng[i] = eng[i].replace('вЂ”','-')
    rus[i] = rus[i].replace('—', '-')
    if '-' in eng[i]:
        dict_n[eng[i].split('-')[0].lstrip().rstrip().capitalize()] = [j.lstrip().rstrip().capitalize() for j in
                                                                       rus[i].split('-')[-1].split(',')]
with open('data/words.json', 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(dict_n, ensure_ascii=False))
