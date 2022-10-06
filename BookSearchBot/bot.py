import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
import crawlingBookInfo as cb

token = '봇 토큰'
id = '사용자 id'

# conversation states
SEARCH, FEWRESULTS, MANYRESULTS, SETSEARCHOPTION, ADDKEYWORD, NORESULT, OTHER = range(7)

def bookSearchGetInput(update, context):
    chat_id = update.message.chat_id
    chat_txt = update.message.text

    update.message.reply_text('도서 검색을 시작합니다.')
    update.message.reply_text('검색을 원하는 키워드를 입력해주세요')

    return SEARCH

def bookSearchStart(update, context):
    chat_id = update.message.chat_id
    chat_txt = update.message.text
    result = cb.startSearch(chat_txt)
    return_val = showSearchResult(update,context,result)
    return return_val

def showSearchResult(update, context, result):
    if result == 0:     # 검색결과 없음.
        update.message.reply_text('우리 도서관에 소장 중인 자료 중에선 해당하는 검색 결과가 없습니다.')
        buttons = [
            [InlineKeyboardButton('타대학 자료 이용', callback_data=1),InlineKeyboardButton('자료 구입 신청', callback_data=2)],
            [InlineKeyboardButton('필요 없어요', callback_data=3)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '타대학 자료 이용 방법이나 자료 구입 신청에 대해 안내해드릴까요?'
            , reply_markup=reply_markup
        )
        return NORESULT

    elif result[0] == 1:    # 검색결과 1건
        update.message.reply_text('총 1 건의 검색 결과가 존재합니다.\n해당 도서의 정보를 안내합니다.')
        info = result[1]
        msg = '도서명: '+info['도서명']+'\n저자: '+info['저자']+'\n발행처: '\
              +info['발행처']+'\n발행년도: '+info['발행년도']
        for item in info['소장정보']:
            msg += '\n------------------'
            msg += '\n소장위치: '+ item['소장위치']
            msg += '\n청구기호: ' + item['청구기호']
            msg += '\n상태: ' + item['상태']
        update.message.reply_text(msg)
        return ConversationHandler.END

    elif result[0] == 2:    # 검색 결과 2건 이상 5건 이하
        items = result[2]
        update.message.reply_text(result[1])
        msg = ''
        for idx, item in enumerate(items):
            msg += f'{idx+1}. ------------------------------\n'
            if item[2] != -1:
                msg += f'[{item[0]}]{item[1]}/{item[2]}/{item[3]}\n'
            else:
                msg += f'[{item[0]}]{item[1]}/{item[3]}\n'
        update.message.reply_text(msg)
        book_buttons = []
        for i in range(len(items)):
            book_buttons.append(InlineKeyboardButton(str(i+1), callback_data=i+1))
        buttons = [
            book_buttons,
            [InlineKeyboardButton('다른 키워드로 검색', callback_data='another_query')]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '이 중에 찾으시는 도서가 있으신가요?\n없으시다면 다른 키워드로 검색할 수 있습니다.'
            , reply_markup=reply_markup
        )
        return FEWRESULTS

    elif result[0] == 3:    # 검색 결과 6건 이상
        items = result[2]
        update.message.reply_text(result[1])
        msg = ''
        for idx, item in enumerate(items):
            msg += f'{idx+1}. ------------------------------\n'
            if item[2] != -1:
                msg += f'[{item[0]}]{item[1]}/{item[2]}/{item[3]}\n'
            else:
                msg += f'[{item[0]}]{item[1]}/{item[3]}\n'
        update.message.reply_text(msg)
        book_buttons=[]
        for i in range(5):
            book_buttons.append(InlineKeyboardButton(str(i+1), callback_data=i+1))
        buttons = [
            book_buttons,
            [InlineKeyboardButton('결과 내 추가 검색', callback_data='add_query')],
            [InlineKeyboardButton('다른 키워드로 검색', callback_data='another_query')]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            '이 중에 찾으시는 도서가 있으신가요?\n없으시다면 검색 결과 내에서 추가 검색을 진행하거나 다른 키워드로 검색할 수 있습니다.'
            , reply_markup=reply_markup
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
        update.callback_query.message.edit_text('해당 도서의 정보를 안내합니다.')
        msg = '도서명: ' + info['도서명'] + '\n저자: ' + info['저자'] + '\n발행처: ' \
              + info['발행처'] + '\n발행년도: ' + info['발행년도']
        for item in info['소장정보']:
            msg += '\n------------------'
            msg += '\n소장위치: ' + item['소장위치']
            msg += '\n청구기호: ' + item['청구기호']
            msg += '\n상태: ' + item['상태']
        update.callback_query.bot.send_message(
            chat_id=update.callback_query.from_user.id, text=msg
        )
        return ConversationHandler.END
    elif data == 'add_query':
        buttons = [
            [InlineKeyboardButton('도서명', callback_data=1),InlineKeyboardButton('저자', callback_data=2)],
            [InlineKeyboardButton('발행처', callback_data=3),InlineKeyboardButton('발행년도', callback_data=4)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.callback_query.message.edit_text('어떤 키워드를 추가하시겠습니까?', reply_markup=reply_markup)
        return SETSEARCHOPTION
    else:
        update.callback_query.message.edit_text('다른 키워드로 도서 검색을 시작합니다.')
        update.callback_query.bot.send_message(
            chat_id=update.callback_query.from_user.id, text='검색 키워드를 입력해주세요.'
        )
        return SEARCH

def checkKeywordToAdd(update, context):
    query = update.callback_query
    data = query.data
    data = int(data)
    context.user_data['selection'] = data
    option = ('도서명', '저자', '발행처')
    if data < 4:
        update.callback_query.message.edit_text(f'[{option[data-1]}] 검색 키워드를 입력해주세요.')
    else:
        update.callback_query.message.edit_text('찾으시는 자료의 발행년도를 입력해주세요.')
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
            [InlineKeyboardButton('대출', callback_data=1), InlineKeyboardButton('열람', callback_data=2),InlineKeyboardButton('원문복사', callback_data=3)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.callback_query.message.edit_text('우리 도서관에 없는 자료는 타대학을 방문하여 해당 자료를 열람 및 대출할 수 있으며 방문하지 않고 복사신청하여 우편으로 받을 수도 있습니다.\n'
                                                '이 중 어떤 서비스를 안내해드릴까요?', reply_markup=reply_markup)
        return OTHER

    elif data == "2":   # 자료구입신청
        update.callback_query.message.edit_text('<자료 구입 신청 방법>\n'
                                                '1. 온라인 검색 신청 : 알라딘 홈페이지에서 도서를 검색하여 구입을 신청합니다.\n'
                                                '2. 직접 입력 신청 : 직접 도서 정보를 입력하여 구입을 신청합니다.\n\n'
                                                '아래의 링크로 이동하여 온라인 검색 신청 또는 직접 입력 신청 버튼을 누르면 됩니다.(로그인이 필요합니다.)\n'
                                                '자료 구입 신청 URL : https://discover.duksung.ac.kr/#/service/request\n\n'
                                                '※ 신청 자료가 국내서라면 1~2주의 기간이 소요되고, 국외서나 멀티미디어 자료라면 4~8주의 기간이 소요됩니다.\n\n'
                                                '※ 다음과 같은 자료는 구입이 제한 될 수 있습니다:\n'
                                                '판타지소설, 로맨스소설, 무협지, 개인 학습용 도서(수험서, 문제집 등), 중고등학생용 도서, 만화종류, 잡지 등 정기간행물'
                                                )
        return ConversationHandler.END

    else:               # 추가 안내 필요 X
        update.callback_query.message.edit_text('도서 검색 기능을 종료합니다.')
        return ConversationHandler.END

def guideOtherWay(update, context):
    query = update.callback_query
    data = query.data
    if data == "1":         # 타대학 자료 대출
        update.callback_query.message.edit_text('<타대학 도서 대출 방법>\n'
                                                '[대출 규정]\n'
                                                ' - 우리 도서관에 있는 책이나, 단행본이 아닌 도서는 신청할 수 없습니다.\n'
                                                ' - 대출 권수: 3권\n'
                                                ' - 대출일: 15일\n'
                                                ' - 연장: 1회 7일\n'
                                                ' - 연체료: 1일당 500원\n\n'
                                                '[신청 방법]\n'
                                                '1. www.riss.kr에서 회원가입 및 자료신청권한을 설정하고 우리 도서관 소속 이용자임을 인증 받아야 합니다.\n'
                                                ' - 학부생 및 일반대학원 학생: 도서관 3층 정기간행물실 안내데스크에서 학생증을 통해 인증\n'
                                                ' - 특수대학원학생(운니동 캠퍼스): Fax(02-901-8089)나 이메일(per_library@duksung.ac.kr)로 학생증 이미지를 송부 후, 전화(02-901-8098)로 확인\n\n'
                                                '2. 소속 이용자 인증 후엔 KERIS 상호대차 서비스를 이용하여 단행본 대출 서비스를 신청합니다.\n'
                                                ' - 자세한 이용 방법은 다음 URL에서 확인: http://www.riss.kr/etc/file/WILL_USER_GUIDE.pdf \n\n'
                                                '3. 신청한 자료는 3~4일 뒤 문자로 안내 받은 후 해당 도서관에 직접 찾아가 수령하거나 우리 도서관 대출 데스크에서 수령할 수도 있습니다.\n'
                                                ' - 신청 도서관에서 수령: 해당 도서관 대출 데스크에서 수령\n'
                                                '   ※ 신청 시 \'서동도협(대출)\' 표시가 있는 도서관을 선택, 비고란에 방문대출을 신청한다고 기재\n'
                                                ' - 우리 도서관에서 수령: 3층 정기간행물실 데스크에서 수령(왕복택배비 5,000원 지불)\n')
        return ConversationHandler.END
    elif data == "2":       # 타대학 자료열람
        update.callback_query.message.edit_text('<타대학 도서 자료 열람 방법>\n'
                                                '[학생증(교직원증)만 지참하면 열람 가능한 대학]\n'
                                               ' - 경인교대, 서울교대, 서동도협 10개 대학(광운대, 국민대, 대진대, 동덕여대, 명지대, 삼육대, 상명대, 서울여대, 성신여대, 한성대)\n\n'
                                               '[이외 전국대학도서관]\n'
                                               '1. 타대학도서관열람의뢰서 아래 URL에서 발급을 신청해야 합니다.(로그인 필요)\n'
                                               ' - 신청 URL: https://discover.duksung.ac.kr/#/mylibrary/olv/add\n'
                                               ' - 원활한 승인을 위해 방문 3일 전에 신청 요망\n'
                                               ' - 바로 승인 받고자 하는 경우, 신청 후 도서관 개관시간 내에 참고도서실(901-8097)로 전화 요망\n\n'
                                               '2. 아래 URL에서 신청현황 조회 및 열람의뢰서 출력이 가능합니다.(로그인 필요)\n'
                                               ' - 신청현황 조회 및 출력 URL: https://discover.duksung.ac.kr/#/mylibrary/olv/result\n\n'
                                               '3. 학생증(교직원증)을 지참하고 열람의뢰서를 해당도서관에 제출한 후 자료를 열람할 수 있습니다.')
        return ConversationHandler.END
    else:                   # 원문복사
        update.callback_query.message.edit_text('<타대학 자료 원문복사 방법>\n'
                                                '[이용 전 확인 사항]\n'
                                                ' - 모든 자료는 인쇄본 형태로 제공되며, 정기간행물실로 방문하여 복사 비용을 지불 후 수령합니다.\n'
                                                ' - 공급 방법에 따라 금액 차이가 있습니다.\n'
                                                ' - 통지 후 30일 경과 자료 미수령 시 서비스 이용이 제한될 수 있습니다.\n'
                                                ' - 단행본, 학위논문은 전권의 50%미만을 복사할 수 있습니다.(저작권법 의거)\n'
                                                ' - 연속간행물은 수록 논문기사(article) 1건 단위로 신청합니다.\n\n'
                                                '[KERIS 또는 SCIENCE ON에서 신청]\n'
                                                '1. KERIS 또는 SCIENCE ON 중 원하는 자료가 있는 사이트에서 회원 가입 및 소속 이용자 인증을 받습니다.\n'
                                                ' - 학부생 및 일반대학원 학생: 도서관 3층 정기간행물실 안내데스크에서 학생증을 통해 인증\n'
                                                ' - 특수대학원학생(운니동 캠퍼스): Fax(02-901-8089)나 이메일(per_library@duksung.ac.kr)로 학생증 이미지를 송부 후, 전화(02-901-8098)로 확인\n\n'
                                                '2. 자료를 검색하고 원문복사를 신청합니다.\n\n'
                                                '3. 자료 도착 통지를 받으면 정기간행물실로 방문하여 자료를 수령합니다.\n\n'
                                                '[사서를 통한 신청]\n'
                                                '1. 아래 URL에서 원문복사를 신청할 수 있습니다.(로그인 필요)\n'
                                                ' - 신청 URL: https://discover.duksung.ac.kr/#/mylibrary/dds/add\n\n'
                                                '2. 아래 URL에서 원문복사 현황을 조회할 수 있습니다.(로그인 필요)\n'
                                                ' - 원문복사 현황조회 URL: https://discover.duksung.ac.kr/#/mylibrary/dds/result/\n\n'
                                                '3. 자료 도착 통지를 받으면 정기간행물실로 방문하여 자료를 수령합니다.')
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
    #dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
