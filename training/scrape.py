# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

driver=webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.amazon.co.jp")
assert "Amazon" in driver.title
x=input("本の名前を入力してください：")
driver.find_element_by_id('twotabsearchtextbox').send_keys(x)
driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
print("ok")

driver.find_element_by_xpath('//*[@id="result_0"]/div/div[3]/div[1]/a').click()
sleep(5)
print(driver.current_url)
print("yeah")

with open('scra.html','w') as a:
    print(driver.current_url)
    a.write(driver.page_source)
driver.close() 
