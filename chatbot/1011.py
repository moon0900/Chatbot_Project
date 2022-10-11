import prettytable
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, handler
from telepot.namedtuple import InlineKeyboardMarkup as MU
from telepot.namedtuple import InlineKeyboardButton as BT
import seatstatus as ss
from telepot.loop import MessageLoop #봇구동
from prettytable import from_csv
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
#내 봇 정보
telegram_id="5582480200"
BOT_TOKEN = '5753157012:AAHrwobIXCi44COC69wH-4SgJhoGlT_4yEM'
bot = telegram.Bot(token=BOT_TOKEN)
Duksae=open('Duksae.png','rb')

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
        text="안녕하세요 덕성여자대학교 도서관 알리미 봇입니다.\t 원하시는 정보를 클릭해주세요 :)",
        reply_markup=reply_markup

    )
def seat_status(update,context):
    #0부터 10까지
    with open("seatstatusef.csv", "r") as fp:
        x = from_csv(fp)
    #x.set_style(markdown)
    x.set_style(prettytable.MARKDOWN)


    #reply_markup = InlineKeyboardMarkup(seatstatus_buttons)
    context.bot.sendMessage(chat_id=update.message.chat_id, text=str(x))


def query_ans(update,context):
    query = update.callback_query
    data = query.data
    #user_text = update.message.text
    if data == "3":
        seat_status()
    else:
        context.bot.send_message("안녕")



#처음에 버튼을 보여주는
first_handler = CommandHandler('start', seat_status)
button_callback_handler = CallbackQueryHandler(query_ans)

dispatcher.add_handler(first_handler)
dispatcher.add_handler(button_callback_handler)

#updater.start_polling()
updater.idle()


