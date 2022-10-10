import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
import crawlingBookInfo as cb

token = '봇 토큰'
id = '사용자 id'

# conversation states
SEARCH, FEWRESULTS, MANYRESULTS, SETSEARCHOPTION, ADDKEYWORD, NORESULT, OTHER = range(7)

def bookSearchGetInput(update, context):
    update.message.reply_text('\U0001F4D5 <b>소장 도서 검색</b>을 시작합니다.\n검색할 \U0001F50D<b>키워드</b>를 입력해주세요', parse_mode=telegram.ParseMode.HTML)
    return SEARCH

def bookSearchStart(update, context):
    chat_txt = update.message.text
    result = cb.startSearch(chat_txt)
    return_val = showSearchResult(update,context,result)
    return return_val

def getEmojiForBookType(bookType):
    if 'e-Book' in bookType or 'E-Journal' in bookType or 'Web-DB' in bookType:
        emoji = '\U0001F4BB'
    elif 'CD' in bookType or 'DVD' in bookType:
        emoji = '\U0001F4BF'
    elif '간행물' in bookType or '기사' in bookType:
        emoji = '\U0001F4F0'
    elif '논문' in bookType:
        emoji = '\U0001F4C4'
    elif '비디오' in bookType:
        emoji = '\U0001F4FC'
    elif '카세트' in bookType:
        emoji = '\U0001F5AD'
    elif 'LP' in bookType:
        emoji = '\U0001F3B5'
    elif '슬라이드' in bookType:
        emoji = '\U0001F5BC'
    else:
        emoji = '\U0001F4D5'
    return emoji

def showSearchResult(update, context, result):
    if result == 0:     # 검색결과 없음.
        update.message.reply_text('해당 키워드의 검색 결과가 <b>없습니다.</b>', parse_mode=telegram.ParseMode.HTML)
        buttons = [
            [InlineKeyboardButton('\U0001F3EB타대학 자료 이용', callback_data=1),InlineKeyboardButton('\U0001F4DD자료 구입 신청', callback_data=2)],
            [InlineKeyboardButton('필요 없어요', callback_data=3)]       #\U0000274C
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '우리 도서관에서 소장하고 있지 않은 자료는 <b>구입 신청</b>을 하거나 <b>타대학 도서관</b>에서 이용할 수 있습니다. 안내해드릴까요?'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        return NORESULT

    elif result[0] == 1:    # 검색결과 1건
        update.message.reply_text('총 <b>1</b> 건의 검색 결과가 존재합니다.\n해당 도서의 정보를 안내합니다.', parse_mode=telegram.ParseMode.HTML)
        info = result[1]
        msg = '<b>자료유형</b> | ' + info['자료유형'] + '\n<b>서명</b> | ' + info['도서명']
        if '저자' in info:
            msg += '\n<b>저자</b> | ' + info['저자']
        msg += '\n<b>발행사항</b> | ' + info['발행처'] + ', ' + info["발행년도"]
        for item in info['소장정보']:
            msg += '\n\n\U0001F4CC <b>소장위치</b> | ' + item['소장위치']
            msg += '\n\U0001F4CC <b>청구기호</b' \
                   '' \
                   '> | ' + item['청구기호']
            msg += '\n\U0001F4CC <b>상태</b> | ' + f'<b>{item["상태"]}</b>'
        update.message.reply_text(msg, parse_mode=telegram.ParseMode.HTML)
        return ConversationHandler.END

    elif result[0] == 2:    # 검색 결과 2건 이상 5건 이하
        cntText, books = result[1], result[2]
        update.message.reply_text(f'총 <b>{cntText}</b> 건의 검색 결과가 존재합니다.', parse_mode=telegram.ParseMode.HTML)
        buttons = []
        for idx, book in enumerate(books):
            bookType = getEmojiForBookType(book[0])
            btnText = bookType + book[1] + '\n' + ' | ' + book[2]
            if len(book) > 3:
                btnText += ' | ' + book[3]
            buttons.append([InlineKeyboardButton(btnText, callback_data=idx + 1)])
        buttons.append([InlineKeyboardButton('\U0001F50D다른 키워드로 검색', callback_data='another_query')])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '이 중에서 찾으시는 도서가 있으신가요? 없으시다면 <b>다른 키워드로 검색</b>할 수 있습니다.'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        return FEWRESULTS

    elif result[0] == 3:    # 검색 결과 6건 이상
        cntText, books = result[1], result[2]
        update.message.reply_text(f'총 <b>{cntText}</b> 건의 검색 결과가 존재합니다.', parse_mode=telegram.ParseMode.HTML)
        buttons=[]
        for idx, book in enumerate(books):
            bookType = getEmojiForBookType(book[0])
            btnText = bookType + book[1] + '\n' + ' | '+book[2]
            if len(book) > 3:
                btnText += ' | '+book[3]
            buttons.append([InlineKeyboardButton(btnText, callback_data=idx+1)])
        buttons.append([InlineKeyboardButton('\U0001F50D결과 내 추가 검색', callback_data='add_query'), InlineKeyboardButton('\U0001F50D다른 키워드로 검색', callback_data='another_query')])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            f'상위 5 건 중에 찾으시는 도서가 있으신가요? 없으시다면 <b>{cntText}</b> 건의 결과 내에서 <b>추가 검색</b>을 진행하거나 <b>다른 키워드로 검색</b>할 수 있습니다.'
            , reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML
        )
        return MANYRESULTS

def cancel(update, context):
    update.message.reply_text('또 필요한 일이 있으면 불러주세요.')
    return ConversationHandler.END

# 기타 메시지에 대한 챗봇의 답변 패턴
def echo(update, context):
    chat_id = update.message.chat_id
    chat_txt = update.message.text
    update.message.reply_text('죄송합니다. 무슨 말인지 모르겠어요.')

def checkSearchResult(update, context):
    query = update.callback_query
    data = query.data
    if len(data) == 1:
        data = int(data)
        info = cb.getBookInfo(data)
        update.callback_query.message.edit_text('해당 도서의 소장 정보를 안내합니다.')
        msg = '<b>자료유형</b> | ' + info['자료유형'] + '\n<b>서명</b> | ' + info['도서명']
        if '저자' in info:
            msg += '\n<b>저자</b> | ' + info['저자']
        msg += '\n<b>발행사항</b> | ' + info['발행처'] + ', ' + info["발행년도"]
        for item in info['소장정보']:
            msg += '\n\n\U0001F4CC <b>소장위치</b> | ' + item['소장위치']
            msg += '\n\U0001F4CC <b>청구기호</b' \
                   '' \
                   '> | ' + item['청구기호']
            msg += '\n\U0001F4CC <b>상태</b> | ' + f'<b>{item["상태"]}</b>'
        update.callback_query.bot.send_message(
            chat_id=update.callback_query.from_user.id, text=msg, parse_mode=telegram.ParseMode.HTML
        )
        return ConversationHandler.END
    elif data == 'add_query':
        buttons = [
            [InlineKeyboardButton('\U0001F4D5도서명', callback_data=1),InlineKeyboardButton('\U0001F464저자', callback_data=2)],
            [InlineKeyboardButton('\U0001F5A8발행처', callback_data=3),InlineKeyboardButton('\U0001F4C6발행년도', callback_data=4)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.callback_query.message.edit_text('어떤 \U0001F50D<b>키워드</b>를 추가하시겠습니까?', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        return SETSEARCHOPTION
    else:
        update.callback_query.message.edit_text('다른 키워드로 소장 도서를 검색합니다.\n검색 \U0001F50D<b>키워드</b>를 입력해주세요.', parse_mode=telegram.ParseMode.HTML
        )
        return SEARCH

def checkKeywordToAdd(update, context):
    query = update.callback_query
    data = query.data
    data = int(data)
    context.user_data['selection'] = data
    option = ('도서명', '저자', '발행처')
    if data < 4:
        update.callback_query.message.edit_text(f'\U0001F50D<b>[{option[data-1]}] 검색 키워드</b>를 입력해주세요.', parse_mode=telegram.ParseMode.HTML)
    else:
        update.callback_query.message.edit_text('찾으시는 자료의 \U0001F50D<b>발행년도</b>를 입력해주세요.', parse_mode=telegram.ParseMode.HTML)
    return ADDKEYWORD

def bookAddSearch(update, context):
    option = context.user_data['selection']
    chat_txt = update.message.text
    if option == 4:
        chat_txt = re.sub(r'[^0-9]', '', chat_txt)
    result = cb.addKeywordSearch(option, chat_txt)
    return_val = showSearchResult(update, context, result)
    return return_val

def checkNoResult(update, context):
    query = update.callback_query
    data = query.data
    if data == "1":     # 타대학 자료 이용
        buttons = [
            [InlineKeyboardButton('\U0001F4DA대출', callback_data=1), InlineKeyboardButton('\U0001F4D6열람', callback_data=2),InlineKeyboardButton('\U0001F4D1원문복사', callback_data=3)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.callback_query.message.edit_text('우리 도서관에 없는 자료는 타대학을 방문하여 자료를 <b>열람</b> 및 <b>대출</b>할 수 있으며 <b>방문하지 않고 복사신청</b>하여 우편으로 받을 수도 있습니다.\n'
                                                '이 중 어떤 서비스를 안내해드릴까요?', reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        return OTHER

    elif data == "2":   # 자료구입신청
        update.callback_query.message.edit_text(
            '<b>&lt자료 구입 신청&gt</b>\n\n'
            '아래의 URL에서 <b>온라인 검색 신청</b> 또는 <b>직접 입력 신청</b>을 할 수 있습니다.\n'
            '\U0001F517 URL: https://discover.duksung.ac.kr/#/service/request\n\n'
            '\U0001F449 <b>온라인 검색 신청</b>: 알라딘 홈페이지에서 도서를 검색하여 신청\n'
            '\U0001F449 <b>직접 입력 신청</b>: 직접 도서 정보를 입력하여 신청'
             , parse_mode=telegram.ParseMode.HTML)
        return ConversationHandler.END

    else:               # 추가 안내 필요 X
        update.callback_query.message.edit_text('알겠습니다. 소장 도서 검색을 마칠게요.')
        return ConversationHandler.END

def guideOtherWay(update, context):
    query = update.callback_query
    data = query.data
    if data == "1":         # 타대학 자료 대출
        update.callback_query.message.edit_text(
            '<b>&lt타대학 도서 대출&gt</b>\n'
            '\U0001F4D5 단행본 <b>3권</b>을 <b>15일</b>간 대출 가능\n'
            '\U0001F4D5 <b>1회 7일</b> 연장 가능\n'
            '\U0001F4D5 연체료는 <b>1일당 500원</b>\n\n'
            '\U0001F449 <b>KERIS 상호대차 서비스에서 단행본 대출 서비스를 신청</b>\n'
            ' - 처음 이용 시 www.riss.kr에서 회원가입, 자료신청권한 설정, 소속 인증이 필요합니다.(아래 URL에서 안내)\n'
            '\U0001F449 <b>신청 자료 수령</b>\n'
            ' - 신청 도서관 또는 우리 도서관에서 수령할 수 있습니다.(아래 URL에서 안내)\n\n'
            '\U0001F517 안내 URL: https://discover.duksung.ac.kr/#/service/other-college/ill'
            , parse_mode=telegram.ParseMode.HTML)
        return ConversationHandler.END
    elif data == "2":       # 타대학 자료열람
        update.callback_query.message.edit_text(
            '<b>&lt타대학 방문 자료 열람&gt</b>\n\n'
            '\U0001F449 <b>학생증(교직원증)만 지참하면 열람 가능한 대학</b>\n'
            ' - 경인교대, 서울교대, 서동도협 10개 대학(광운대, 국민대, 대진대, 동덕여대, 명지대, 삼육대, 상명대, 서울여대, 성신여대, 한성대)\n'
            '\U0001F449 <b>이외 전국대학도서관</b>\n'
            ' - 열람의뢰서와 학생증(교직원증)을 지참해야합니다. 아래 URL에서 열람의뢰서 발급을 신청할 수 있습니다.\n\n'
            '\U0001F517 안내 및 신청 URL: https://discover.duksung.ac.kr/#/service/other-college/olv'
            , parse_mode=telegram.ParseMode.HTML)
        return ConversationHandler.END
    else:                   # 원문복사
        update.callback_query.message.edit_text(
            '<b>&lt원문복사 신청&gt</b>\n\n'
            '\U0001F449 <b>KERIS</b> 또는 <b>SCIENCE ON</b>을 통한 신청은 해당 사이트 회원 가입 및 소속 인증 절차가 필요합니다. 인증방법은 아래 URL에서 안내하고 있습니다.\n'
            '\U0001F449 <b>사서를 통한 신청</b>은 아래 URL에서 신청할 수 있습니다.\n\n'
            '\U0001F517 안내 및 신청 URL: https://discover.duksung.ac.kr/#/service/other-college/dds'
            , parse_mode=telegram.ParseMode.HTML)
        return ConversationHandler.END

def main():
    bot = telegram.Bot(token=token)
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, bookSearchGetInput)],

        states={
            SEARCH: [MessageHandler(Filters.text, bookSearchStart)],
            FEWRESULTS:  [CallbackQueryHandler(checkSearchResult)],
            MANYRESULTS: [CallbackQueryHandler(checkSearchResult)],
            SETSEARCHOPTION: [CallbackQueryHandler(checkKeywordToAdd)],
            ADDKEYWORD: [MessageHandler(Filters.text, bookAddSearch)],
            NORESULT: [CallbackQueryHandler(checkNoResult)],
            OTHER: [CallbackQueryHandler(guideOtherWay)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
