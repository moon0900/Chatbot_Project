from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
import time
import  os
browser = webdriver.Chrome("C:/Users/rmfls/PycharmProjects/chromedriver_win32/chromedriver.exe")
browser.get("http://mcard.duksung.ac.kr:8080/PW/pw20.php")
time.sleep(3)
table = browser.find_element_by_class_name('default')
tbody = table.find_element_by_tag_name('tbody')
rows = tbody.find_elements_by_tag_name('tr')
#location은 열람실명, using은 사용/총좌석, left는 잔여석이다
list_location=[]
list_using=browser.find_elements_by_xpath('//*[@id="divtext"]/a')
list_left=[]
text=""
for index, value in enumerate(rows):
    body = value.find_elements_by_tag_name('td')[0]
    list_location.append(body.text)
for index, value in enumerate(rows):
    try:
        body = value.find_elements_by_tag_name('td')[2]
        list_left.append(body.text)
    except:
        pass

using=browser.find_elements_by_xpath('//*[@id="divtext"]/a')
list_using=[]
for index, value in enumerate(using):
    list_using.append(value.text)

list_location=list(filter(None,list_location))
list_left=list(filter(None,list_left))
#1부터 9까지는 열람실 11부터13까지는 스터디룸 15부터17까지는 PCZone
#print(list_location[1:10])
readingroom={'loc':list_location[1:10],'using':list_using[1:10],'left':list_left[1:10]}
studyroom={'loc':list_location[11:14],'using':list_using[11:14],'left':list_left[11:14]}
pcroom={'loc':list_location[15:18],'using':list_using[15:18],'left':list_left[15:18]}

i=0
while i < 9:
    print(readingroom['loc'][i],"의 사용/좌석 수는",list_using[i],"이고 현재 잔여좌석은",readingroom['left'][i],"입니다.")
    i=i+1
i=0
while i < 3:
    print(studyroom['loc'][i],"의 사용/좌석 수는",list_using[i+9],"이고 현재 잔여좌석은",studyroom['left'][i],"입니다.")
    i=i+1
i=0
while i < 9:
    print(readingroom['loc'][i],"의 사용/좌석 수는",list_using[i],"이고 현재 잔여좌석은",readingroom['left'][i],"입니다.")
    i=i+1
i=0
while i < 3:
    print(pcroom['loc'][i],"의 사용/좌석 수는",list_using[i+12],"이고 현재 잔여좌석은",pcroom['left'][i],"입니다.")
    i=i+1









