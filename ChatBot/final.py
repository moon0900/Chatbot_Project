from datetime import time
import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from BookSearchBot.bot import bookSearchGetInput, bookSearchStart, checkSearchResult as BcheckSearchResult, checkKeywordToAdd as BcheckKeywordToAdd,bookAddSearch,checkNoResult as BcheckNoResult, guideOtherWay, cancel
from noticeSearch.bot import noticeSearchGetInput, noticeSearchStart, checkSearchResult as NcheckSearchResult, checkKeywordToAdd as NcheckKeywordToAdd, NoticeAddSearch, checkNoResult as NcheckNoResult
from chatbot import seatstatus as ss
from emoji import emojize

from tensorflow.keras.models import load_model
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import re

# conversation states
BOOKSEARCH, BOOKFEWRESULTS, BOOKMANYRESULTS, BOOKSETSEARCHOPTION, BOOKADDKEYWORD, BOOKNORESULT, BOOKOTHER,\
    NOTICESEARCH, NOTICEFEWRESULTS, NOTICEMANYRESULTS, NOTICESETSEARCHOPTION, NOTICEADDKEYWORD, NOTICENORESULT, NOTICEOTHER= range(14)

token = '5752050232:AAGnpg_A4lfUHtckrzLQaFSQwm1ZBVHIczM'
id = '5744498162'

tokenizer_path = './intentModel/tokenizer.pickle'
model_path = './intentModel/intent_model.h5'

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
    #단어를 숫자 처리
    encoded = tokenizer.texts_to_sequences([sentence])
    inputs.append(encoded[0])
  padded_inputs = pad_sequences(inputs, maxlen=INPUT_LEN, padding='post')
  return padded_inputs

# 입력문장을 넣으면 모델의 예측 레이블을 리턴해주는 함수
def get_prediction(model, input):
    #단어 전처리
  input_sentence = question_processing(input)
  prediction = np.argmax(model.predict(input_sentence), axis = 1)
  return prediction

# =======================================================

bot = telegram.Bot(token=token)

info_message = emojize('''안녕하세요!:waving_hand:\n저는 \U0001F4D5<b>덕성여대 도서관</b>에 대하여 실시간으로 정보를 드리는 덕새챗봇입니다.''')
filepath = '../chatbot/Duksae2.png'
#의도분류
def classifyIntent(update, context):
    # Intent Label
    # 0: '공지검색' | 1: '도서검색' | 2: '운영시간' | 3: '자리현황'
    user_text = update.message.text  # 사용자가 보낸 메세지
    intent = get_prediction(model, user_text)  # 모델이 예측한 사용자의 의도
    # 공지검색
    if intent == 0:
        rm_filters = ['찾아줘', '검색해줘', '검색해주세요', '알려줘', '찾아봐', '어딨어', '있어', '찾아', '올라온 거', '올라왔어','올라왔나요',
                      ' 좀 ', '찾아주세요', '알려주세요', '어딨어요', '어디 있어요', '줄 수 있나요',
                      '줄 수 있어요', '줄 수 있어', '있어요', '있나요', '공지사항', '공지', '교재']
        user_text = re.sub('|'.join(rm_filters), '', user_text)
        user_text = user_text.strip('?')
        user_text = user_text.strip()
        if len(user_text) > 1:
            context.user_data['keyword'] = user_text
            state = noticeSearchStart(update, context)
            return state
        update.message.reply_text('\U0001F4E2 <b>찾아보고 싶은 공지사항</b>이 있으신가요?\n검색하고 싶은 \U0001F50D<b>키워드</b>를 입력해주세요',
                                  parse_mode=telegram.ParseMode.HTML)
        return NOTICESEARCH
    # 도서검색
    elif intent == 1:
        rm_filters = ['찾아줘', '검색해줘', '검색해주세요', '알려줘', '찾아봐', '어딨어', '빌릴 수 있어', '있어',
                      ' 좀 ', '찾아주세요', '알려주세요', '어딨어요', '어디 있어요', '빌릴 수 있나요',
                      '빌릴 수 있어요', '있어요', '있나요', '책', '도서', '교재']
        user_text = re.sub('|'.join(rm_filters),'',user_text)
        user_text = user_text.strip('?')
        user_text = user_text.strip()
        if len(user_text) > 1:
            context.user_data['keyword'] = user_text
            state = bookSearchStart(update, context)
            return state
        update.message.reply_text('\U0001F4D5 <b>소장 도서 검색</b>을 시작합니다.\n검색할 \U0001F50D<b>키워드</b>를 입력해주세요',
                                  parse_mode=telegram.ParseMode.HTML)
        return BOOKSEARCH
    # 운영시간
    elif intent == 2:
        if '방학' in user_text:
            if '일반도서' in user_text:
                update.message.reply_text(text='일반도서실의 방학 중 운영시간은 평일: 9:00 ~ 17:00, 토요일: 휴관')
            elif '노트북' in user_text:
                update.message.reply_text(text='노트북존의 방학 중 운영시간은 평일: 9:00 ~ 17:00, 토요일: 휴관')
            elif '미디어' in user_text:
                update.message.reply_text(text='멀티미디어실의 방학 중 운영시간은 평일: 9:00 ~ 17:00, 토요일: 휴관')
            elif 'play' in user_text:
                update.message.reply_text(text='Play N Create의 방학 중 운영시간은 평일: 9:00 ~ 17:00, 토요일: 휴관')
            elif '제1' in user_text:
                update.message.reply_text(text='연중무휴 06:00 ~ 23:00')
            elif '제2' in user_text:
                update.message.reply_text(text='평일: 06:00 ~ 23:00, 토요일: 휴관')
            elif '24' in user_text:
                update.message.reply_text(text='연중무휴 24시간')
            elif '휴게실' in user_text:
                update.message.reply_text(text='연중무휴 24시간')
            elif '열람실' in user_text:
                task_buttons3 = [
                    [InlineKeyboardButton('<제1자유열람실> 연중무휴 06:00 ~ 23:00', callback_data=30)],
                    [InlineKeyboardButton('<제2자유열람실> 평일: 06:00 ~ 23:00, 토요일: 휴관', callback_data=30)],
                    [InlineKeyboardButton('<24시간 열람실/ 휴게실> 연중무휴 24시간 ', callback_data=30)]
                ]
                reply_markup = InlineKeyboardMarkup(task_buttons3)
                update.message.reply_text(text='\U0001F4D5<b>방학 중</b> 열람실 운영시간입니다.', reply_markup=reply_markup,
                                 parse_mode='HTML')
            else:
                cmd_task_buttons2()
        elif '학기' in user_text:
            if '일반도서' in user_text:
                update.message.reply_text(text='일반도서실의 방학 중 운영시간은 평일: 9:00 ~ 21:00, 토요일: 9:00 ~ 13:00')
            elif '노트북' in user_text:
                update.message.reply_text(text='노트북존의 방학 중 운영시간은 평일: 9:00 ~ 21:00, 토요일: 휴관')
            elif '미디어' in user_text:
                update.message.reply_text(text='멀티미디어실의 방학 중 운영시간은 평일: 9:00 ~ 21:00, 토요일: 9:00 ~ 13:00')
            elif 'play' in user_text:
                update.message.reply_text(text='Play N Create의 방학 중 운영시간은 평일: 9:00 ~ 19:00, 토요일: 휴관')
            elif '제1' in user_text:
                update.message.reply_text(text='연중무휴 06:00 ~ 23:00')
            elif '제2' in user_text:
                update.message.reply_text(text='평일: 06:00 ~ 23:00, 토요일: 휴관')
            elif '24' in user_text:
                update.message.reply_text(text='연중무휴 24시간')
            elif '휴게실' in user_text:
                update.message.reply_text(text='연중무휴 24시간')
            elif '열람실' in user_text:
                task_buttons3 = [
                    [InlineKeyboardButton('<제1자유열람실> 연중무휴 06:00 ~ 23:00', callback_data=30)],
                    [InlineKeyboardButton('<제2자유열람실> 평일: 06:00 ~ 23:00, 토요일: 휴관', callback_data=30)],
                    [InlineKeyboardButton('<24시간 열람실/ 휴게실> 연중무휴 24시간 ', callback_data=30)]
                ]
                reply_markup = InlineKeyboardMarkup(task_buttons3)
                update.message.reply_text(text='\U0001F4D5<b>학기 중</b> 열람실 운영시간입니다.', reply_markup=reply_markup,
                                 parse_mode='HTML')
            else:
                cmd_task_buttons1()
        else:
            update.message.reply_text(text='방학 중 운영시간인지 학기 중 운영시간인지 정확하게 입력해주세요')
        return ConversationHandler.END
    # 자리현황
    else:
        seat_status()
        return ConversationHandler.END

def seat_status(update, context):
    #0부터 10까지
    list_left=ss.Crawling()
    btn1 = InlineKeyboardButton(text="자유열람실A:"+list_left[1],callback_data="5")
    btn2 = InlineKeyboardButton(text="자유열람실B:" + list_left[2], callback_data="5")
    btn3 = InlineKeyboardButton(text="자유열람실C:" + list_left[7], callback_data="5")
    btn4 = InlineKeyboardButton(text="자유열람실D:" + list_left[8], callback_data="5")
    btn5 = InlineKeyboardButton(text="집중형 학습공간:" + list_left[3], callback_data="5")
    btn6 = InlineKeyboardButton(text="개인 학습공간:" + list_left[4], callback_data="5")
    btn7 = InlineKeyboardButton(text="개방형 학습공간I:" + list_left[9], callback_data="5")
    btn8 = InlineKeyboardButton(text="개방형 학습공간Ⅱ:" + list_left[8], callback_data="5")
    btn9 = InlineKeyboardButton(text="24시 열람실:" + list_left[5], callback_data="5")
    btn10 = InlineKeyboardButton(text="노트북실:" + list_left[6], callback_data="5")
    btn11 = InlineKeyboardButton(text="노트북존:" + list_left[9], callback_data="5")
    btn12 = InlineKeyboardButton(text="4인석:" + list_left[13], callback_data="5")
    btn13 = InlineKeyboardButton(text="6인석:" + list_left[14], callback_data="5")
    btn14 = InlineKeyboardButton(text="9인석:" + list_left[15], callback_data="5")
    seatstatus_buttons = [[btn1,btn2],[btn3,btn4],[btn5,btn6],[btn7,btn8],[btn9],[btn10,btn11]]
    reply_markup = InlineKeyboardMarkup(seatstatus_buttons)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=emojize(":round_pushpin:<b>열람실 잔여 좌석수입니다.</b>:round_pushpin:"),
        reply_markup=reply_markup,
        parse_mode='html'
    )

    seatstatus_button2=[[btn12,btn13,btn14]]
    reply_markup = InlineKeyboardMarkup(seatstatus_button2)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=emojize(":round_pushpin:<b>스터디룸 잔여 좌석수입니다</b>:round_pushpin:"),
        reply_markup=reply_markup,
        parse_mode='html'
    )
    context.bot.send_message(
        chat_id=update.effective_user.id, text=emojize(
        ":down_arrow:스터디룸 예약을 원하신다면 눌러주세요:down_arrow:\n[스터디룸 예약 페이지로 이동하기](http://mcard.duksung.ac.kr:8080/PW/pw20_03.php):computer_mouse:"),
                     parse_mode='Markdown')


def cmd_task_buttons1(update, context):
    task_buttons1 = [
        [InlineKeyboardButton(' ', callback_data=30), InlineKeyboardButton('평일', callback_data=30), InlineKeyboardButton('토요일', callback_data=30)],
        [InlineKeyboardButton('일반도서실', callback_data=30), InlineKeyboardButton('9:00 ~ 21:00', callback_data=30), InlineKeyboardButton('9:00 ~ 13:00', callback_data=30)],
        [InlineKeyboardButton('노트북존', callback_data=30), InlineKeyboardButton('9:00 ~ 21:00', callback_data=30), InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('멀티미디어실', callback_data=30), InlineKeyboardButton('9:00 ~ 21:00', callback_data=30), InlineKeyboardButton('9:00 ~ 13:00', callback_data=30)],
        [InlineKeyboardButton('Play N Create', callback_data=30), InlineKeyboardButton('9:00 ~ 19:00', callback_data=30), InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('제2자유열람실', callback_data=30), InlineKeyboardButton('06:00 ~ 23:00', callback_data=30), InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('제1자유열람실', callback_data=30), InlineKeyboardButton('연중무휴 06:00 ~ 23:00', callback_data=30)],
        [InlineKeyboardButton('24시간 열람실/ 휴게실', callback_data=30), InlineKeyboardButton('연중무휴 24시간 ', callback_data=30)]
    ]

    reply_markup = InlineKeyboardMarkup(task_buttons1)
    context.bot.send_message(
        chat_id=update.effective_user.id,text='\U0001F4D5<b>학기 중</b> 도서관 운영시간 안내입니다.', reply_markup=reply_markup, parse_mode='HTML')

def cmd_task_buttons2(update, context):
    task_buttons1 = [
        [InlineKeyboardButton(' ', callback_data=30),InlineKeyboardButton('평일', callback_data=30),InlineKeyboardButton('토요일', callback_data=30)],
        [InlineKeyboardButton('일반도서실', callback_data=30),InlineKeyboardButton('9:00 ~ 17:00', callback_data=30),InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('노트북존', callback_data=30), InlineKeyboardButton('9:00 ~ 17:00', callback_data=30),InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('멀티미디어실', callback_data=30), InlineKeyboardButton('9:00 ~ 17:00', callback_data=30),InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('Play N Create', callback_data=30), InlineKeyboardButton('9:00 ~ 17:00', callback_data=30),InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('제2자유열람실', callback_data=30),InlineKeyboardButton('06:00 ~ 23:00', callback_data=30), InlineKeyboardButton('휴관', callback_data=30)],
        [InlineKeyboardButton('제1자유열람실', callback_data=30),InlineKeyboardButton('연중무휴 06:00 ~ 23:00', callback_data=30)],
        [InlineKeyboardButton('24시간 열람실/ 휴게실', callback_data=30),InlineKeyboardButton('연중무휴 24시간 ', callback_data=30)]
    ]
    reply_markup = InlineKeyboardMarkup(task_buttons1)
    context.bot.send_message(
        chat_id=update.effective_user.id,text='\U0001F4D5<b>방학 중</b> 도서관 운영시간 안내입니다.', reply_markup=reply_markup, parse_mode='HTML')

def cmd_task_buttons3(update, context):
    task_buttons2 = [
        [InlineKeyboardButton('도서관 운영시간 안내', callback_data=40)]
        , [InlineKeyboardButton('도서관 책 찾기', callback_data=41)]
        ,[InlineKeyboardButton('열람실 실시간 현황', callback_data=42)]
        , [InlineKeyboardButton('실시간 공지사항 확인', callback_data=43)]
    ]

    reply_markup = InlineKeyboardMarkup(task_buttons2)

    context.bot.send_message(
        chat_id=update.message.chat_id
        , text='궁금하신 정보를 클릭해주세요!'
        , reply_markup=reply_markup
        , parse_mode='HTML'
    )
    return

def cmd_task_buttons(update, context):

    task_buttons = [
        [InlineKeyboardButton('\U0001F50D학기 중', callback_data=52)]
        , [InlineKeyboardButton('\U0001F50D방학 중', callback_data=53)]
        ,[InlineKeyboardButton('취소', callback_data=54)]
    ]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text='<b>학기 중/방학 중</b> 궁금하신 도서관 시설의 운영시간 안내의 버튼을 클릭해주세요!'
        , reply_markup=reply_markup
        , parse_mode='HTML'
    )

def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id
        , action=ChatAction.TYPING
    )
    if data == '54':
        update.callback_query.bot.send_message(chat_id=update.callback_query.from_user.id,
                                               text='취소되었습니다! 다시 시작하려면 <b>/start</b>를 입력해주세요!',  parse_mode='HTML')
    else:
        if data == '40':
            cmd_task_buttons(update, context)
        elif data == '41':
            update.callback_query.bot.send_message(chat_id=update.callback_query.from_user.id,
                text='\U0001F4D5 <b>소장 도서 검색</b>을 시작합니다.\n검색할 \U0001F50D<b>키워드</b>를 입력해주세요',
                parse_mode=telegram.ParseMode.HTML)
            return BOOKSEARCH
        elif data == '42':
            seat_status(update, context)
        elif data == '43':
            update.callback_query.bot.send_message(chat_id=update.callback_query.from_user.id,
                text = '\U0001F4E2 <b>찾아보고 싶은 공지사항</b>이 있으신가요?\n검색하고 싶은 \U0001F50D<b>키워드</b>를 입력해주세요',
                parse_mode=telegram.ParseMode.HTML)
            return NOTICESEARCH
        elif data == '52':
            cmd_task_buttons1(update, context)
        elif data == '53':
            cmd_task_buttons2(update, context)

    return ConversationHandler.END

def main():
    bot = telegram.Bot(token=token)
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    task_buttons_handler = CommandHandler('start', cmd_task_buttons3)
    button_callback_handler = CallbackQueryHandler(cb_button)
    dp.add_handler(task_buttons_handler)

    search_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(cb_button), MessageHandler(Filters.text, classifyIntent)],
        states={
            BOOKSEARCH: [MessageHandler(Filters.text, bookSearchStart)],
            BOOKFEWRESULTS: [CallbackQueryHandler(BcheckSearchResult)],
            BOOKMANYRESULTS: [CallbackQueryHandler(BcheckSearchResult)],
            BOOKSETSEARCHOPTION: [CallbackQueryHandler(BcheckKeywordToAdd)],
            BOOKADDKEYWORD: [MessageHandler(Filters.text, bookAddSearch)],
            BOOKNORESULT: [CallbackQueryHandler(BcheckNoResult)],
            BOOKOTHER: [CallbackQueryHandler(guideOtherWay)],
            NOTICESEARCH: [MessageHandler(Filters.text, noticeSearchStart)],
            NOTICEFEWRESULTS: [CallbackQueryHandler(NcheckSearchResult)],
            NOTICEMANYRESULTS: [CallbackQueryHandler(NcheckSearchResult)],
            NOTICESETSEARCHOPTION: [CallbackQueryHandler(NcheckKeywordToAdd)],
            NOTICEADDKEYWORD: [MessageHandler(Filters.text, NoticeAddSearch)],
            NOTICENORESULT: [CallbackQueryHandler(NcheckNoResult)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(search_conv)
    dp.add_handler(button_callback_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()