"""
채팅 의도 분류하는 모델 적용해본 코드

"""

import telegram
from telegram.ext import Updater, ChatMemberHandler, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

from tensorflow.keras.models import load_model
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

token = '5752050232:AAGnpg_A4lfUHtckrzLQaFSQwm1ZBVHIczM'
id = '5744498162'

tokenizer_path = './ex_code/intentModel/tokenizer.pickle'
model_path = './ex_code/intentModel/intent_model.h5'

# =======================================================
okt = Okt()
# 학습시킨 Tokenizer 로드
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

# 모델 불러오기 & 모델 input 크기 구하기
model = load_model(model_path)
INPUT_LEN = model.get_config()["layers"][0]["config"]["batch_input_shape"][1]

# 입력 문장을 모델 input에 맞게 변환해주는 함수
def question_processing(sentences):
  if type(sentences) == str:
    sentences = [sentences]
  inputs = []
  for sentence in sentences :
    sentence = okt.morphs(sentence)
    encoded = tokenizer.texts_to_sequences([sentence])
    inputs.append(encoded[0])
  padded_inputs = pad_sequences(inputs, maxlen=INPUT_LEN, padding='post')
  return padded_inputs

# 입력문장을 넣으면 모델의 예측 레이블을 리턴해주는 함수
def get_prediction(model, input):
  input_sentence = question_processing(input)
  prediction = np.argmax(model.predict(input_sentence), axis = 1)
  return prediction

# =======================================================

def classifyIntent(update, context):
    # Intent Label
    # 0: '공지검색' | 1: '도서검색' | 2: '운영시간' | 3: '자리현황'
    user_text = update.message.text             # 사용자가 보낸 메세지
    intent = get_prediction(model, user_text)   # 모델이 예측한 사용자의 의도
    # 공지검색
    if intent == 0:
        update.message.reply_text("공지사항을 찾고싶으시군요.")
    # 도서검색
    elif intent == 1:
        update.message.reply_text("소장도서를 검색하고 싶으시군요.")
    # 운영시간
    elif intent == 2:
        update.message.reply_text("운영시간을 알고싶으시군요.")
    # 자리현황
    else:
        update.message.reply_text("도서실 좌석 현황을 알고싶으시군요.")

bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dp = updater.dispatcher

intent_handler = MessageHandler(Filters.text, classifyIntent)
dp.add_handler(intent_handler)

updater.start_polling()