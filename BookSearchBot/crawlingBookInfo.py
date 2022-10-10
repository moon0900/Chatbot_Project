import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome('../chromedriver.exe')
driver.get('https://discover.duksung.ac.kr/#/')

def getBookInfo(i):
    elem = driver.find_element_by_css_selector('div.ikc-search-item:nth-child('+str(i)+') > div.ikc-item-info > ul > li:nth-child(1) > a')
    elem.click()
    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ikc-biblio-info > p > span')))
    bookType = elem.text
    bookInfo = driver.find_element_by_css_selector('div.ikc-biblio-info > ul')
    bookTitle = bookInfo.find_element_by_css_selector('li:nth-child(1) > span > a').text.split('/')
    bookPub = bookInfo.find_element_by_css_selector('li:nth-child(2) > span > span').text.split(',')
    result = {
        '자료유형': bookType,
        '도서명': bookTitle[0].strip(),
        '발행처': bookPub[0].split(':')[1].strip(),
        '발행년도': bookPub[1].strip()
    }
    if len(bookTitle) > 1:
        result['저자'] = bookTitle[1].strip()
    locList = []
    bookInfo = driver.find_elements_by_css_selector('tbody.ikc-item')
    for info in bookInfo:
        bookLoc = info.find_element_by_css_selector('tr:nth-child(1) > td:nth-child(2) > span:nth-child(2)').text
        bookNum = info.find_element_by_css_selector('tr:nth-child(1) > td:nth-child(3) > span.ikc-item-callno').text
        bookState = info.find_element_by_css_selector(
            'tr:nth-child(1) > td:nth-child(5) > span:nth-child(2) > span.ikc-item-status').text
        loc = {'소장위치': bookLoc, '청구기호': bookNum,'상태': bookState}
        locList.append(loc)
    result['소장정보'] = locList

    return result

def getTopItems():
    items = []
    elems = driver.find_elements_by_css_selector('div.ikc-search-item')[:5]
    for idx, elem in enumerate(elems):
        type = elem.find_element_by_css_selector('div.ikc-item-aside > div > label').text
        title = elem.find_element_by_css_selector(
            'div.ikc-item-info > ul > li:nth-child(1) > a.ikc-item-title > span').text
        writer = elem.find_elements_by_css_selector('div.ikc-item-info > ul > li.ikc-item-author > span')
        if len(writer) == 0:
            writer = -1
        else:
            writer = writer[0].text
        publisher = \
        elem.find_element_by_css_selector('div.ikc-item-info > ul > li.ikc-item-publication > span').text.split(':')[
            1].strip()
        item=(type, title, writer, publisher)
        items.append(item)
    return items


def startSearch(keyword):
    driver.get('https://discover.duksung.ac.kr/#/')
    elem = driver.find_element_by_id('keyword')
    elem.send_keys(keyword)    # 키워드 검색

    elem = driver.find_element_by_class_name('ikc-btn-search')
    elem.click()

    result = getSearchResult()

    return result

def getSearchResult():
    noresult, result = '', ''
    while(len(noresult)==0 and len(result)==0):
        noresult = driver.find_elements_by_css_selector('div.ikc-search-noresult.ikc-no-record > strong')
        if len(noresult) > 0:
            noresult = noresult[0].text
        result = driver.find_elements_by_css_selector('div.ikc-search-result-listup > p')
        if len(result) > 0:
            result = result[0].text

    if len(result) == 0:  # 검색 결과 없음
        return 0

    cntText = result.split()
    cntText = cntText[2].strip()  # 검색 결과 수

    if cntText == '1':
        return 1, getBookInfo(1)
    elif int(cntText.replace(',', '')) < 6:
        return 2, cntText, getTopItems()
    else:
        return 3, cntText, getTopItems()

def addKeywordSearch(option, input):
    detail_btn = driver.find_element_by_css_selector('div.ikc-search-topbtns > a')
    options = ('서명', '저자', '발행처')
    if detail_btn.text != '간략검색':
        detail_btn.click()
    if option < 4:
        ex_keyword = driver.find_elements_by_css_selector(
            'div.ikc-search-ex-keyword-wrap.col-lg-6.col-md-6 > div.ikc-search-ex-keyword:not(.ng-hide)')[-1]
        dropDown = Select(ex_keyword.find_element_by_css_selector('span:nth-child(2) > select'))
        dropDown.select_by_visible_text(options[option-1])
        ex_keyword = ex_keyword.find_element_by_css_selector('span.ikc-search-keyword > input')
        ex_keyword.send_keys(input)
    else:
        elem = driver.find_element_by_css_selector('div.ikc-date-picker.ikc-date-picker-from > span > span > input')
        elem.send_keys(input)
        driver.find_element_by_css_selector('div.ikc-search-ex-keyword-wrap.col-lg-6.col-md-6 > div.ikc-search-ex-keyword:not(.ng-hide) > span.ikc-search-keyword > input').click()
        elem = driver.find_element_by_css_selector('div.ikc-date-picker.ikc-date-picker-to > span > span > input')
        elem.send_keys(input)
    driver.find_element_by_css_selector('div.ikc-search-ex-btns > input.ikc-btn-search').click()
    time.sleep(0.5)
    result = getSearchResult()
    return result
