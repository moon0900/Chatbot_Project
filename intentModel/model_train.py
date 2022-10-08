"""
문장입력을 받아 질문의 의도를 분류하는 모델 학습시키기
pip install konlpy 설치 필요

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn import preprocessing
from tensorflow.keras.utils import to_categorical
import pickle

# 데이터 읽어오기
df = pd.read_csv('./train_intent_SR_auged.csv', encoding='cp949')
#df.sample(20)
df.groupby('intent').size().reset_index(name='count')


# 문장을 단어 리스트로 변환
okt = Okt()
X_train = []
for sentence in df.question:
  temp_X = []
  temp_X = okt.morphs(sentence)
  X_train.append(temp_X)
# 단어 리스트를 토큰으로
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)

# 모델 입력의 크기를 정하기 위해 가장 단어 수가 많은 문장의 길이 활용
vocab_size = len(tokenizer.word_index)+1
max_len = max(len(l) for l in X_train)
avg_len = sum(map(len, X_train))/len(X_train)
print(vocab_size, max_len, avg_len)

# 문장의 최대 길이에 맞춰 패딩 넣어주기
X_train = pad_sequences(X_train, maxlen = max_len, padding='post')

# 레이블 인코딩
idx_encode = preprocessing.LabelEncoder()
idx_encode.fit(df['intent'])
y_train = idx_encode.transform(df['intent'])
label_idx = dict(zip(list(idx_encode.classes_), idx_encode.transform(list(idx_encode.classes_))))
idx_label = {}
for key, value in label_idx.items():
  idx_label[value] = key
y_train = to_categorical(y_train)

# 분류를 위한 1d cnn 모델 생성 (출처:https://www.analyticsvidhya.com/blog/2021/12/intent-classification-with-convolutional-neural-networks/)
from keras.layers import Dense, Input
from keras.layers import Conv1D, MaxPooling1D, Embedding, Flatten
from keras.models import Model

MAX_SEQUENCE_LENGTH = max_len
MAX_NUM_WORDS = 5000
EMBEDDING_DIM = 60
word_index = tokenizer.word_index
num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
embedding_layer = Embedding(num_words,EMBEDDING_DIM,input_length=MAX_SEQUENCE_LENGTH,trainable=True)

sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
x = Conv1D(64, 3, activation='relu')(embedded_sequences)
x = Conv1D(64, 3, activation='relu')(x)
x = MaxPooling1D(2)(x)
x=Flatten()(x)
x = Dense(100, activation='relu')(x)
preds = Dense(len(label_idx), activation='softmax')(x)
model = Model(sequence_input, preds)
model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])
model.summary()

# 모델 학습
history=model.fit(X_train, y_train, epochs=15, batch_size=64)

# 모델 저장
model.save('intent_model.h5')

# tokenizer 저장
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)