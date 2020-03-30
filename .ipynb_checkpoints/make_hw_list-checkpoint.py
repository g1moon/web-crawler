from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd 
import time
import os


# chromedriver = './chromedriver.exe' 

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(0.5)

time.sleep(0.5)

url = "http://ecampus.kangnam.ac.kr/"
print(url)

driver.get(url)

#-----------------------------
#정보입력
id_bar = driver.find_element_by_name('username') #name in element
id_bar.clear()
#################
id_bar.send_keys('')
##################

pw_bar = driver.find_element_by_name('password')
pw_bar.clear()
###############
pw_bar.send_keys('')  #input the user password
###############
pw_bar.send_keys(Keys.RETURN) #enter_key
#------------------------------------------

bs = BeautifulSoup(driver.page_source, 'html.parser')
#-----------------------------------------------
lec_urls = bs.select('#region-main > div > div.progress_courses > div.course_lists > ul > li> div > a')
lec_urls = [lec_url.get('href') for lec_url in lec_urls][1:]
#--------------------------------
hw_urls = [f'http://ecampus.kangnam.ac.kr/mod/assign/index.php?id={lec_url[-5:]}' for lec_url in lec_urls]
#---------------------------

lec_names = ['소프트웨어개론', '가상현실개론', 'UNiX서버', '확률통계', '데이터베이스응용']
cnt = 0

dic = {}
Subject_list = []
Week_list = []
Assignment_list = []
State_list = []
Url_list = []
Deadline_list = []

for hw_url in hw_urls:
    
    driver.get(hw_url)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    rows_len = len(bs.select('#region-main > div > table > tbody')[0].select('tr'))

    
    for i in range(0, rows_len):
        if '미제출' in bs.select('#region-main > div > table > tbody')[0].select('tr')[i].text:
            row = bs.select('#region-main > div > table > tbody')[0].select('tr')[i].text.strip() 
            temp_row = row.split('\n')            
            
            Subject_list.append(lec_names[cnt])
            Week_list.append(temp_row[0].strip().replace(' ',''))
            Assignment_list.append(temp_row[1])
            State_list.append(temp_row[3] ) 
            Url_list.append(hw_url)
            Deadline_list.append(temp_row[2])


            dic['Subject'] = Subject_list
            dic['week'] =Week_list
            dic['Assignment']= Assignment_list
            dic['State'] = State_list
            dic['DeadLine'] = Deadline_list
            dic['Url'] = Url_list
    cnt = cnt + 1


                    
df = pd.DataFrame(dic)

df.to_excel('./data/to_do_list.xlsx')

os.system('open ./data/to_do_list.xlsx')

df