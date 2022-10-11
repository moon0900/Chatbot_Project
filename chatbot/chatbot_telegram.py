
import telegram
from telegram.ext import Updater
from telegram.ext import  MessageHandler, Filters



hello_message = ('안녕하세요 덕성여대 도서관봇입니다:)\n',
                 '필요하신 서비스의 번호를 입력해주세요\n',
                 '1.도서검색기능\n',
                 '2.도서관 이용 안내(이용시간 및 시설안내)\n',
                 '3.좌석현황(열람실, 스터디룸, PC)\n',
                 '4.공지사항\n',
                 '5.신착자료/추천도서\n',
                 '6.My library(대출/연장/예약)\n',
                 '7.FAQ\n',
                 )
id="5582480200"
TOKEN = '5753157012:AAHrwobIXCi44COC69wH-4SgJhoGlT_4yEM'
bot = telegram.Bot(token=TOKEN)
bot.sendMessage(chat_id=id, text='안녕하세요 덕성여대 도서관봇입니다:)\n'
                                 '필요하신 서비스의 번호를 입력해주세요\n'
                                 '1.도서검색기능\n'
                                 '2.도서관 이용 안내(이용시간 및 시설안내)\n'
                                 '3.좌석현황(열람실, 스터디룸, PC)\n'
                                 '4.공지사항\n'
                                 '5.신착자료/추천도서\n'
                                 '6.My library(대출/연장/예약)\n'
                                 '7.FAQ\n',)

"""
Updater은 실질적인 일을 하는 모통, use_context=True,가 있는데
버전관련 부분
dispatcher은 updater에 기능을 하나씩 붙여주는 역할
start_pooling()은 텔레그램부터 업데이트를 받아오는 일을
하는 것
"""
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

def handler(update, context):
    user_text = update.message.text
    if user_text=="3":
        bot.send_message(chat_id=id, text="어 그래 안녕")
    elif user_text == "뭐해":
        bot.send_message(chat_id=id, text="그냥 있어")

"""
echo함수는 기존 start 함수와는 다를게 없다
다만 handler가 MessageHandler이다.
MessageHandler의 첫번째 인자가 
텍스트를 받되 명령어로 지정된 텍스트는 제외한다는 것이다.
"""
echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)

"""내 대화 id 알아내기
updates = bot.getUpdates()
for u in updates:
    print(u.message)
    """

