"""
유사한 표현 바꿔가며 데이터 증강
*이 코드로 증강시킨 데이터를 kor_eda.py로 어순을 바꿔가며 다시 증강시키고 모델 학습에 사용하였음.
"""

import pandas as pd
import csv

df = pd.read_csv('./train_intent.csv')
print(len(df['intent']))
data = df.values.tolist()
print(len(data))
# 대체할 수 있는 표현 정리한 딕셔너리. 추가할만한 표현이 있다면 추가해주길 바람.
synonym = {
    '도서관': ['도서실', '미디어실', '일반도서실','멀티미디어실','열람실'],
    '언제까지': ['얼마나', '몇 시간', '몇 시까지', '언제'],
    '오늘': ['내일','주말에','평일에','학기 중에', '방학 때', '밤에','낮에', '아침에', '새벽에', '지금'],
    '운영하나요?': ['문 닫나요?','문 여나요?', '문 열어?', '문 닫아?', '운영해?', '가도 되나요?','가도 돼?', '갈 수 있나요?'],
    '책': ['도서', '자료', '교재', '문헌'],
    '열람실': ['스터디룸','컴퓨터존','pc존', '컴퓨터실'],
    '어딨어요?': [ '어디?', '어딨음?', '어디에 있어요?', '찾아주세요', '찾아줘', '있나요?','있어?'],
    '궁금해요' : ['알려줘','모르겠어'],
    '자리':['좌석','의자'],
    '몇 개':['몇 명', '얼마나'],
    '남았나요?':['있나요?', '남았어?', '있어?'],
    '많나요?':['적나요?', '많아?', '적어?']
}

for i in range(5):
    newDatas=[]
    for idx, d in enumerate(data):
        print(idx, d)
        string = d[0]
        label = d[1]
        strings =[]
        for s in synonym:
            if s in string:
                for re_word in synonym[s]:
                    news = string.replace(s, re_word)
                    print(news)
                    strings.append(news)
        for s in strings:
            newData = [s, d[1]]
            newDatas.append(newData)
    data = data + newDatas

fields = ['question', 'intent']
df = pd.DataFrame(data, columns = fields)
print(len(df))
df = df.drop_duplicates(['question'], keep = 'first')
print(len(df))
df.to_csv('train_intent_SR.csv', index=None)
"""
with open('train_intent_SR.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(rows)
"""