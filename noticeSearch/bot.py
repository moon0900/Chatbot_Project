import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from noticeSearch import crawlingNotice as CrawlN

token = '5752050232:AAGnpg_A4lfUHtckrzLQaFSQwm1ZBVHIczM'
id = '5744498162'

# conversation states
NOTICESEARCH, NOTICEFEWRESULTS, NOTICEMANYRESULTS, NOTICESETSEARCHOPTION, NOTICEADDKEYWORD, NOTICENORESULT, NOTICEOTHER = range(7,14)

def noticeSearchGetInput(update, context):
    update.message.reply_text('\U0001F4E2 <b>찾아보고 싶은 공지사항</b>이 있으신가요?\n검색하고 싶은 \U0001F50D<b>키워드</b>를 입력해주세요', parse_mode=telegram.ParseMode.HTML)
    return NOTICESEARCH

def noticeSearchStart(update, context):
    if 'keyword' in context.user_data:
        chat_txt = context.user_data['keyword']
        del context.user_data['keyword']
    else:
        chat_txt = update.message.text
    update.message.reply_text('\U0001F50D<b>' + chat_txt + '</b>(으)로 검색합니다.',
                              parse_mode=telegram.ParseMode.HTML)
    result = CrawlN.startSearch(chat_txt)
    return_val = showSearchResult(update, context, result)
    return return_val

def showSearchResult(update, context, result):
    if result == 0:     # 검색결과 없음.
        buttons = [
            [InlineKeyboardButton('\U0001F50D다른 키워드로 검색', callback_data=1),InlineKeyboardButton('필요 없어요', callback_data=2)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '해당 키워드의 검색 결과가 존재하지 않습니다. <b>다른 키워드</b>로 검색해드릴까요?'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        return NOTICENORESULT
    elif result[0] < 6:    # 검색 결과 1건 이상 5건 이하
        items = result[1]
        buttons = []
        for i in items[:5]:
            buttons.append([InlineKeyboardButton(text='\U0001F4E2 '+i[0], url=i[1], callback_data=0)])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            f'관련된 공지사항은 총 <b>{result[0]}</b> 건이 있습니다.'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        buttons = [
            [InlineKeyboardButton('\U0001F50D다른 키워드로 검색', callback_data='another_query'), InlineKeyboardButton('필요없어요', callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '이 중에 찾으시는 내용이 없으시다면 <b>다른 키워드</b>로 검색할 수 있습니다.'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        return NOTICEFEWRESULTS

    else:    # 검색 결과 6건 이상
        items = result[1]
        buttons = []
        for i in items[:5]:
            buttons.append([InlineKeyboardButton(text='\U0001F4E2 '+i[0], url=i[1], callback_data=0)])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            f'관련된 공지사항은 총 <b>{result[0]}</b> 건이 있습니다. 그 중 상위 5개 공지사항입니다.'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        buttons = [
            [InlineKeyboardButton('\U0001F50D결과 내 추가 검색', callback_data='add_query'), InlineKeyboardButton('\U0001F50D다른 키워드로 검색', callback_data='another_query')]
            ,[InlineKeyboardButton('필요없어요', callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            f'이 중에 찾으시는 내용이 없으시다면 <b>{result[0]}</b> 건의 결과 내에서 <b>추가 검색</b>을 하거나 <b>다른 키워드</b>로 검색할 수 있습니다.'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        return NOTICEMANYRESULTS


def checkSearchResult(update, context):
    query = update.callback_query
    data = query.data
    #if data == '0':
    #    return ConversationHandler.END
    if data == 'add_query':
        buttons = [
            [InlineKeyboardButton('전체', callback_data='all'),InlineKeyboardButton('내용', callback_data='content'),InlineKeyboardButton('제목', callback_data='title')]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.callback_query.message.edit_text('어떤 \U0001F50D<b>키워드</b>를 추가하시겠습니까?', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        return NOTICESETSEARCHOPTION
    elif data == 'another_query':
        update.callback_query.message.edit_text('<b>다른 키워드</b>로 다시 공지를 검색합니다.', parse_mode=telegram.ParseMode.HTML)
        update.callback_query.bot.send_message(
            chat_id=update.callback_query.from_user.id, text='검색 \U0001F50D<b>키워드</b>를 입력해주세요.', parse_mode=telegram.ParseMode.HTML
        )
        return NOTICESEARCH
    elif data == 'no':
        update.callback_query.message.edit_text('알겠습니다. 공지사항 검색을 마칠게요.')
        return ConversationHandler.END

def checkKeywordToAdd(update, context):
    query = update.callback_query
    data = query.data
    context.user_data['selection'] = data
    option = {'all': '전체', 'content': '내용', 'title': '제목'}
    update.callback_query.message.edit_text(f'\U0001F50D<b>[{option[data]}] 검색 키워드</b>를 입력해주세요.', parse_mode=telegram.ParseMode.HTML)
    return NOTICEADDKEYWORD

def NoticeAddSearch(update, context):
    option = context.user_data['selection']
    chat_txt = update.message.text
    result = CrawlN.addSearchKeyword(option, chat_txt)
    return_val = showSearchResult(update, context, result)
    return return_val


def checkNoResult(update, context):
    query = update.callback_query
    data = query.data
    if data == "1":     # 다른 키워드로 검색
        update.callback_query.message.edit_text('<b>다른 키워드</b>로 다시 공지를 검색합니다.', parse_mode=telegram.ParseMode.HTML)
        update.callback_query.bot.send_message(
            chat_id=update.callback_query.from_user.id, text='검색 \U0001F50D<b>키워드</b>를 입력해주세요.', parse_mode=telegram.ParseMode.HTML
        )
        return NOTICESEARCH
    else:               # 추가 안내 필요 X
        update.callback_query.message.edit_text('알겠습니다. 공지사항 검색을 마칠게요.')
        return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('또 필요한 일이 있으면 불러주세요.')
    return ConversationHandler.END
