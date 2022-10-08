"""
학습한 모델 불러와서 예측 시켜보기
pip install konlpy 설치 필요

"""

from tensorflow.keras.models import load_model
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

okt = Okt()
# 학습시킨 Tokenizer 로드
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# 레이블 정보
idx_label = ['도서검색', '운영시간', '자리현황']


# 모델 불러오기 & 모델 input 크기 구하기
model = load_model('intent_model.h5')
max_len = model.get_config()["layers"][0]["config"]["batch_input_shape"][1]

# 입력 문장을 모델 input에 맞게 변환해주는 함수
def question_processing(sentences):
  if type(sentences) == str:
    sentences = [sentences]
  inputs = []
  for sentence in sentences :
    sentence = okt.morphs(sentence)
    encoded = tokenizer.texts_to_sequences([sentence])
    inputs.append(encoded[0])
  padded_inputs = pad_sequences(inputs, maxlen=max_len, padding='post')
  return padded_inputs

# 입력문장을 넣으면 모델의 예측 레이블을 리턴해주는 함수
def get_prediction(model, input):
  input_sentence = question_processing(input)
  prediction = np.argmax(model.predict(input_sentence), axis = 1)
  return prediction

query = ['연오의 파이썬 책이 있는지 궁금해', '파이썬 알고리즘 인터뷰책 좀 찾아줘','노트북실 몇시에 열어?','휴게실 몇시부터 운영해?','열람실 좌석 남았어?', '열람실 좌석 현황이 궁금해!', '열람실 몇시까지야?', '지금 노트북존 문 열었어?', '메타버스책 어디에있는지 알려줘']
for q in query:
  p = get_prediction(model, q)
  print('질문:', q, '\t모델이 예측한 질문의 의도:', idx_label[p[0]])