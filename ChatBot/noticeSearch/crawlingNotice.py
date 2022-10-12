"""
공지사항 크롤링
pip install urllib3 필요

"""
import urllib
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome('./chromedriver.exe')

def getURL(all='', content='', title='', max=5):
    url = f'https://discover.duksung.ac.kr/#/bbs/notice?offset=0&max={max}'
    if all != '':
        encoded = urllib.parse.quote(all)
        url +=f'&all={encoded}'
    if content != '':
        encoded = urllib.parse.quote(content)
        url += f'&content={encoded}'
    if title != '':
        encoded = urllib.parse.quote(title)
        url += f'&title={encoded}'
    return url

def editURLAttr(url, option, keyword):
    attrs = url.split('&')
    if '&'+option+'=' in url:
        for idx, attr in enumerate(attrs[2:]):
            if attr[:len(option)] == option:
                attrs[idx+2] += urllib.parse.quote(' '+keyword)
                break
    else:
        attrs.append(option+'='+urllib.parse.quote(keyword))
    url = '&'.join(attrs)
    return url

def startSearch(keyword):
    url = getURL(all=keyword)
    driver.get(url)
    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ikc-tablelist-listup > p > strong')))
    totalCnt = elem.text
    while (totalCnt == ''):
        totalCnt = driver.find_element_by_css_selector('div.ikc-tablelist-listup > p > strong').text
    totalCnt = int(totalCnt)
    if totalCnt == 0:
        return 0
    result = getResult()
    return totalCnt, result

def getResult():
    elems = driver.find_elements_by_css_selector('table.ikc-tablelist > tbody > tr')
    result = []
    for elem in elems:
        title = elem.text.split()
        dates = title[-1]
        title = ' '.join(title[1:-1])
        if ']' in title:
            title = title.split(']')
            title = ']'.join(title[1:]).strip()
        title += ' | '+dates
        href = elem.find_element_by_css_selector('td.ikc-contents > span:nth-child(2) > span > a').get_attribute('href')
        result.append((title, href))
    return result

def addSearchKeyword(option, keyword):
    url = driver.current_url
    url = editURLAttr(url, option, keyword)
    driver.get(url)
    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ikc-tablelist-listup > p > strong')))
    totalCnt = elem.text
    while(totalCnt == ''):
        totalCnt =driver.find_element_by_css_selector('div.ikc-tablelist-listup > p > strong').text
    totalCnt = int(totalCnt)
    if totalCnt == 0:
        return 0
    result = getResult()
    return totalCnt, result

