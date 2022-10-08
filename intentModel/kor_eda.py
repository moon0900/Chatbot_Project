"""
문장 데이터의 어순을 바꾸는 등의 기법으로 데이터 증강시키는 코드
출처: https://github.com/catSirup/KorEDA/blob/master/eda.py

"""

import random
import re

wordnet = {     # 대체할 수 있는 표현 정리한 딕셔너리인데, 코드 내에서 유사어 표현 바꾸는 부분을 주석 처리했기 때문에 이 코드에선 실제로 사용되진 않음.
    '도서관': ['도서실', '미디어실', '일반도서실','멀티미디어실','열람실'],
    '언제까지': ['얼마나', '몇 시간', '몇 시까지', '언제'],
    '오늘': ['내일','주말에','평일에','학기 중에', '방학 때', '밤에','낮에', '아침에', '새벽에', '지금'],
    '하나요?': ['문 닫나요?','문 여나요?', '문 열어?', '문 닫아?', '해?', '가도 되나요?','가도 돼?', '갈 수 있나요?'],
    '책': ['도서', '자료', '교재', '문헌'],
    '열람실': ['스터디룸','컴퓨터존','pc존', '컴퓨터실'],
    '어딨어요?': [ '어디?', '어딨음?', '어디에 있어요?', '찾아주세요', '찾아줘', '있나요?','있어?'],
    '궁금해요' : ['알려줘','모르겠어'],
    '자리':['좌석','의자'],
    '몇 개':['몇 명', '얼마나'],
    '남았나요?':['있나요?', '남았어?', '있어?'],
    '많나요?':['적나요?', '많아?', '적어?']
}

# 한글만 남기고 나머지는 삭제
def get_only_hangul(line):
    parseText = re.compile('/ ^[ㄱ-ㅎㅏ-ㅣ가-힣]*$/').sub('', line)

    return parseText


########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################
def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    if len(new_words) != 0:
        sentence = ' '.join(new_words)
        new_words = sentence.split(" ")

    else:
        new_words = ""

    return new_words

def get_synonyms(word):
    synomyms = []

    try:
        for syn in wordnet[word]:
            for s in syn:
                synomyms.append(s)
    except:
        pass

    return synomyms


########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p
########################################################################
def random_deletion(words, p):
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words) - 1)
        return [words[rand_int]]

    return new_words


########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################
def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)

    return new_words


def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words) - 1)
    random_idx_2 = random_idx_1
    counter = 0

    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words) - 1)
        counter += 1
        if counter > 3:
            return new_words

    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words


########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################
def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)

    return new_words


def add_word(new_words):
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        if len(new_words) >= 1:
            random_word = new_words[random.randint(0, len(new_words) - 1)]
            synonyms = get_synonyms(random_word)
            counter += 1
        else:
            random_word = ""
        if counter >= 10:
            return

    random_synonym = synonyms[0]
    random_idx = random.randint(0, len(new_words) - 1)
    new_words.insert(random_idx, random_synonym)


def EDA(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
    #sentence = get_only_hangul(sentence)
    words = sentence.split(' ')
    words = [word for word in words if word != ""]
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug / 4) + 1

    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))
    """
    # sr    유의어 변환인데 이 방식이 안맞는 것 같아 주석처리하고 data_generation.py 코드에서 유의어 변환하여 데이터 증강
    for _ in range(num_new_per_technique):
        a_words = synonym_replacement(words, n_sr)
        augmented_sentences.append(' '.join(a_words))
    """
    # ri
    for _ in range(num_new_per_technique):
        a_words = random_insertion(words, n_ri)
        augmented_sentences.append(' '.join(a_words))

    # rs
    for _ in range(num_new_per_technique):
        a_words = random_swap(words, n_rs)
        augmented_sentences.append(" ".join(a_words))

    # rd
    for _ in range(num_new_per_technique):
        a_words = random_deletion(words, p_rd)
        augmented_sentences.append(" ".join(a_words))

    augmented_sentences = [get_only_hangul(sentence) for sentence in augmented_sentences]
    random.shuffle(augmented_sentences)

    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    augmented_sentences.append(sentence)

    return augmented_sentences

"""
우리 데이터에 적용
"""

import pandas as pd
import csv

df = pd.read_csv('./train_intent_SR.csv')
print(len(df['intent']))
data = df.values.tolist()

newDatas=[]
for idx, d in enumerate(data):
    print(idx, d)
    string = d[0]
    label = d[1]
    newStrings = EDA(string, num_aug=5)
    for s in newStrings:
        newData = [s, d[1]]
        newDatas.append(newData)
data = data + newDatas
fields = ['question', 'intent']
rows = data
print(len(rows))
with open('train_intent_SR_auged.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(rows)