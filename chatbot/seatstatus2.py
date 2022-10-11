from selenium import webdriver
import pandas as pd
import os.path
from openpyxl.styles import Alignment
import prettytable

def Crawling():
    browser = webdriver.Chrome("C:/Users/rmfls/PycharmProjects/chromedriver_win32/chromedriver.exe")
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
    #리스트 빈 요소 삭제
    list_location = list(filter(None, list_location))
    list_left = list(filter(None, list_left))
    # 1부터 9까지는 열람실 11부터13까지는 스터디룸 15부터17까지는 PCZone
    # print(list_location[1:10])
    readingroom = {'loc': list_location[1:12], 'using': list_using[1:10], 'left': list_left[1:12]}
    studyroom = {'loc': list_location[13:15], 'using': list_using[13:15], 'left': list_left[13:15]}
    pcroom = {'loc': list_location[15:12], 'using': list_using[15:18], 'left': list_left[15:18]}
    #append가 아닌이유?리스트를 하나 씩 출력하기 어렵다.print문을 이용할게 아니라 bot.sendmessage()함수에서는..
    #seat_status+=readingroom['loc'][i]+"의 잔여좌석 수 : "+readingroom['left'][i]+"\n"
    table = prettytable.PrettyTable()
    table.field_names = [" "+"열람실명"+" ", '잔여']
    table.add_row(["제1자유열람실A",readingroom['left'][0]])
    table.add_row(['제1자유열람실B',readingroom['left'][1]])
    table.add_row(['집중형 학습공간A',readingroom['left'][2]])
    table.add_row(['개인 학습공간 B',readingroom['left'][3]])
    table.add_row(['24시 열람실',readingroom['left'][4]])
    table.add_row(['노트북실',readingroom['left'][5]])
    table.add_row(['제1자유열람실C',readingroom['left'][6]])
    table.add_row(['제1자유열람실D',readingroom['left'][7]])
    table.add_row(['노트북존',readingroom['left'][8]])
    table.add_row(['개방형 학습공간 I C',readingroom['left'][9]])
    table.add_row(['개방형 학습공간Ⅱ D',readingroom['left'][10]])
    table.set_style(prettytable.DEFAULT)
    print(table)


    #return seat_status
Crawling()
