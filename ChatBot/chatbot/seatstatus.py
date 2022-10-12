from selenium import webdriver
import pandas as pd
import os.path

def Crawling():
    browser = webdriver.Chrome('./chromedriver.exe')
    browser.get("http://mcard.duksung.ac.kr:8080/PW/pw20.php")
    #time.sleep(3)
    table = browser.find_element_by_class_name('default')
    tbody = table.find_element_by_tag_name('tbody')
    rows = tbody.find_elements_by_tag_name('tr')
    # location은 열람실명, using은 사용/총좌석, left는 잔여석이다
    list_location = []
    list_using =[]
    list_left = []
    #나중에 출력할 문자열들을 저장할 변수
    seat_status=""

    #1행(시설 이름)에 접근하여 텍스트로 뽑아오기)
    for index, value in enumerate(rows):
        body = value.find_elements_by_tag_name('td')[0]
        list_location.append(body.text)
    #2행(사용/총좌석수)에 접근하여 텍스트로 뽑아오기
    using = browser.find_elements_by_xpath('//*[@id="divtext"]/a')
    for index, value in enumerate(using):
        list_using.append(value.text)

    '''tr>td[2]에 접근을 해야한다. 하지만 tr에는 td[0]까지 밖에 없음 즉 빈 값이 존재해서 
    for문으로 접근했을 때 오류가 발생하기 때문에 try-catch문으로 오류를 회피해준다'''
    #3행(잔여 좌석)에 접근하여 텍스트로 뽑아오기
    for index, value in enumerate(rows):
        try:
            body = value.find_elements_by_tag_name('td')[2]
            list_left.append(body.text)
        except:
            pass
    browser.close()
    #리스트 빈 요소 삭제하기
    list_location = list(filter(None, list_location))
    list_left = list(filter(None, list_left))
    # 1부터 9까지는 열람실 11부터13까지는 스터디룸 15부터17까지는 PCZone
    # print(list_location[1:10])

    #append가 아닌이유?리스트를 하나 씩 출력하기 어렵다.print문을 이용할게 아니라 bot.sendmessage()함수에서는..

    return list_left
