import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, handler
from telepot.namedtuple import InlineKeyboardMarkup as MU
from telepot.namedtuple import InlineKeyboardButton as BT
import seatstatus as ss
from emoji import emojize
from prettytable import from_csv
from telepot.loop import MessageLoop #봇구동
#내 봇 정보
telegram_id="5582480200"
BOT_TOKEN = '5753157012:AAHrwobIXCi44COC69wH-4SgJhoGlT_4yEM'
bot = telegram.Bot(token=BOT_TOKEN)
Duksae=open('Duksae2.png','rb')
from prettytable import PrettyTable

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

def button_show(update,context):
    btn1 = InlineKeyboardButton(text="1.도서검색기능",callback_data="1")
    btn2 = InlineKeyboardButton(text="2.도서관 이용 안내", callback_data="2")
    btn3 = InlineKeyboardButton(text="3.좌석현황", callback_data="3")
    btn4 = InlineKeyboardButton(text="4.공지사항", callback_data="4")
    task_buttons=[[btn1],[btn2],[btn3],[btn4]]

    reply_markup=InlineKeyboardMarkup(task_buttons)
    bot.send_photo(chat_id=telegram_id,photo=Duksae)
    context.bot.send_message(
        chat_id=telegram_id,
        text=emojize("안녕하세요:waving_hand: <b>덕성여자대학교 도서관봇</b>입니다 :slightly_smiling_face:\n                  원하시는 기능을 선택하세요!"),
        reply_markup=reply_markup,
    parse_mode='html'

    )
def seat_status():
    #0부터 10까지
    btn0 = InlineKeyboardButton(text=ss.Crawling(0),callback_data="5")
    btn1 = InlineKeyboardButton(text=ss.Crawling(1), callback_data="5")
    btn2 = InlineKeyboardButton(text=ss.Crawling(2), callback_data="5")
    btn3 = InlineKeyboardButton(text=ss.Crawling(3), callback_data="5")
    btn4 = InlineKeyboardButton(text=ss.Crawling(4), callback_data="5")
    btn5 = InlineKeyboardButton(text=ss.Crawling(5), callback_data="5")
    btn6 = InlineKeyboardButton(text=ss.Crawling(6), callback_data="5")
    btn7 = InlineKeyboardButton(text=ss.Crawling(7), callback_data="5")
    btn8 = InlineKeyboardButton(text=ss.Crawling(8), callback_data="5")
    btn9 = InlineKeyboardButton(text=ss.Crawling(9), callback_data="5")
    btn10 = InlineKeyboardButton(text=ss.Crawling(10), callback_data="5")

    seatstatus_buttons = [[btn0], [btn1],[btn2],[btn3],[btn4],[btn5],[btn6],[btn7],[btn8],[btn9],[btn10]]
    reply_markup = InlineKeyboardMarkup(seatstatus_buttons)
    bot.send_message(
        chat_id=telegram_id,
        text="안녕하세요 덕성여자대학교 도서관 알리미 봇입니다.",
        reply_markup=reply_markup
    )

def query_ans(update,context):
    query = update.callback_query
    data = query.data
    #user_text = update.message.text
    if data == "3":
        seat_status()
    else:
        context.bot.send_message("안녕")



#처음에 버튼을 보여주는
first_handler = CommandHandler('start', button_show)
button_callback_handler = CallbackQueryHandler(query_ans)

dispatcher.add_handler(first_handler)
dispatcher.add_handler(button_callback_handler)

#updater.start_polling()
updater.idle()


