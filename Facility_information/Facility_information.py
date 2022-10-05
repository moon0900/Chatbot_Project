# buttons_bot.py
import time

import telegram
import telepot as telepot
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, handler

BOT_TOKEN = '토큰'
bot = telegram.Bot(BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher
updater.start_polling()
telegram_id = '아이디'
info_message = '''시작하려면 /start를 입력해주세요'''
bot.sendMessage(chat_id=telegram_id, text=info_message)

def cmd_task_buttons1():

    task_buttons1 = [
        [InlineKeyboardButton('일반도서실', callback_data=5)],
        [InlineKeyboardButton('노트북존', callback_data=6)],
        [InlineKeyboardButton('멀티미디어실', callback_data=7)],
        [InlineKeyboardButton('play n create', callback_data=8)],
        [InlineKeyboardButton('제1자유열람실', callback_data=9)],
        [InlineKeyboardButton('제2자유열람실', callback_data=10)],
        [InlineKeyboardButton('24시간 열람실/ 휴게실', callback_data=11)]
    ]
    reply_markup = InlineKeyboardMarkup(task_buttons1)
    bot.send_message(chat_id=telegram_id, text='궁금한 시설을 클릭해주세요.', reply_markup=reply_markup)



def cmd_task_buttons(update, context):

    task_buttons = [
        [InlineKeyboardButton('운영시간 안내', callback_data=1)]
        , [InlineKeyboardButton('대출가능 책수 및 대출 방법', callback_data=2)]
        , [InlineKeyboardButton('연체로 인한 벌칙 안내 및 반납 방법', callback_data=3)]
        ,[InlineKeyboardButton('취소', callback_data=4)]
    ]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id
        , text='궁금하신 도서관 시설 안내에 대하여 버튼을 클릭하거나 직접 물어봐주세요!'
        , reply_markup=reply_markup
    )



def cb_button(update, context):
    query = update.callback_query
    data = query.data


    context.bot.send_chat_action(
        chat_id=update.effective_user.id
        , action=ChatAction.TYPING
    )

    if data == '4':
        context.bot.edit_message_text(
            text='작업이 취소되었습니다.'
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
    else:

        if data == '1':
            cmd_task_buttons1()

        elif data == '2':
            bot.send_message(telegram_id, """<대출가능 책수>\n학부생 : 8책, 대학원생/조교 : 15책, 교수: 40책, 외래교수/직원: 20책, 휴학생/졸업생/교류대생/평생교육원: 3책
                                            \n<대출방법>\nstep 1. 도서관 홈페이지에서 자료검색\nstep 2. 일반도서실(1층)에서 자료 선택\nstep 3. 대출카운터(2층)에 책과 함께 학생증 제시\nstep 4. 대출도서와 반납예정일을 모니터로 확인""")

        elif data == '3':
            bot.send_message(telegram_id,"""<연체로 인한 벌칙 안내>\n1. 연체도서가 있는 경우해당 이용자 대출 정지 \n2. 연체일수의 2배만큼 대출이 정지 \n3. 졸업예정일 30일 전 미반납 시 졸업증명서 발급 불가
                                            \n<반납 방법>\n1. 대출카운터 반납대에 책을 제출\n2. 무인반납함 이용 안내""")
            loan_return()
        elif data == '5':
            bot.send_message(telegram_id,'<학기중>\n평일 : 9:00 ~ 21:00, 토요일 : 9:00 ~ 13:00\n<방학중>\n평일 : 9:00 ~ 17:00, 토요일 : 휴관')
        elif data == '6':
            bot.send_message(telegram_id,'<학기중>\n평일 : 9:00 ~ 21:00, 토요일 : 휴관\n<방학중>\n평일 : 9:00 ~ 17:00, 토요일 : 휴관')
        elif data == '7':
            bot.send_message(telegram_id, '<학기중>\n평일 : 9:00 ~ 21:00, 토요일 : 9:00 ~ 13:00\n<방학중>\n평일 : 9:00 ~ 17:00, 토요일 : 휴관')
        elif data == '8':
            bot.send_message(telegram_id, '<학기중>\n평일 : 9:00 ~ 19:00, 토요일 : 휴관\n<방학중>\n평일 : 9:00 ~ 17:00, 토요일 : 휴관')
        elif data == '9':
            bot.send_message(telegram_id, '연중무휴 06:00 ~ 23:00')
        elif data == '10':
            bot.send_message(telegram_id, '<학기중>\n06:00 ~ 23:00\n<방학중>\n휴관')
        elif data == '11':
            bot.send_message(telegram_id, '연중무휴 24시간')


# 동작확인 위한 코드 (추후 수정 예정)
def operating_time():
    time.sleep(5)
    print('.')


def number_books():
    time.sleep(5)
    print('.')

def loan_return():
    time.sleep(5)
    print('.')


def overdue_penalty():
    time.sleep(3)
    print('.')


# 시나리오 업데이트 예정
def handler1(update, context):
    user_text = update.message.text
    if user_text == "반납":
        bot.send_message(telegram_id, text="1. 대출카운터 반납대에 책을 대출 or 2. 무인반납함 이용")  # 답장 보내기
    elif user_text == "대출":
        bot.send_message(telegram_id, text="1. 도서관 홈페이지에서 자료 검색\n2. 일반도서실에서 자료서 선택\n3. 대출카운터에 책과 함께 학생증 제시\n4. 대출도서와 반납예정일을 모니터로 확인 ")  # 답장 보내기
    elif user_text == "노트북존 운영시간 알려줘":
        bot.send_message(telegram_id, text="<학기중>\n평일 : 9:00 ~ 21:00, 토요일 : 휴관\n<방학중>\n평일 : 9:00 ~ 17:00, 토요일 : 휴관")


task_buttons_handler = CommandHandler('start', cmd_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)



dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)



echo_handler = MessageHandler(Filters.text, handler1)
dispatcher.add_handler(echo_handler)


updater.idle()

