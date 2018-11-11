from selenium import webdriver
from selenium.webdriver.common.keys  import Keys
driver=webdriver.Chrome()
driver.get("https://www.amazon.co.jp")
assert "Amazon" in driver.title
driver.find_element_by_id('twotabtextsearchbox').send_keys("python　プロフェッショナルプログラミング")
driver.find_element_by_id('twotabtextsearchbox').send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
