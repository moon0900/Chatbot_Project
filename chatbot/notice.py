from selenium import webdriver
#/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div/div/div[5]/table/tbody[1]/tr[1]/td[2]/span[2]

def Notice_crawling():
    browser = webdriver.Chrome("C:/Users/rmfls/PycharmProjects/chromedriver_win32/chromedriver.exe")
    browser.get("https://discover.duksung.ac.kr/#/bbs/notice?offset=0&max=20")
    tbody = browser.find_element_by_css_selector('#goto-content > div > div > div > div:nth-child(5) > table > tbody:nth-child(3)')
    rows = tbody.find_elements_by_tag_name('tr')
    notice_location=[]
    # goto-content > div > div > div > div:nth-child(5) > table > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(2)
    i=1
    while(i<7):
        address = ('// *[ @ id = "goto-content"] / div / div / div / div[5] / table / tbody[1] / tr[' + str(i) + '] / td[2] / span[2] / span / a / \
                                           span[2]')
        print(browser.find_element_by_xpath(address).text)
        i+=1


Notice_crawling()