from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from getUpdateData import *
from unit.getEnv import getEnv
from sendData import setEnv

class UpdateTopic(unittest.TestCase):
    def setUp(self):
#        self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
        self.driver.implicitly_wait(30)
        self.base_url = "http://m.newsmth.net"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_update_topic(self):
        driver = self.driver
        driver.get("http://m.newsmth.net")
        driver.find_element_by_name("id").clear()
        driver.find_element_by_name("id").send_keys(getEnv("newsmthID").getEnv())
        driver.find_element_by_name("passwd").clear()
        driver.find_element_by_name("passwd").send_keys(getEnv("newsmthPW").getEnv())
        driver.find_element_by_css_selector("input.btn").click()
        time.sleep(10)

        for i in range(0, len(tmpUrlID)):
            print("http://m.newsmth.net/article/SoftwareTesting/post/%d" %tmpUrlID[i])
            driver.get("http://m.newsmth.net/article/SoftwareTesting/post/%d" %tmpUrlID[i])
            driver.find_element_by_name("content").clear()
            driver.find_element_by_name("content").send_keys("Updating by auto script\n")
            driver.find_element_by_css_selector("input.btn").click()
            time.sleep(20)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

tmpUrlID = []        
if __name__ == "__main__":
   setEnv("configure/login.txt")
   dataBasePath = "/home/licaijun/newsmthUpdate.db"
   sql = dataBase(dataBasePath)
   conn = sql.connectData()
   postTime = sql.getPostTime(conn, 1)

   nowDay = currentTime()
   startDay = datetime.datetime(int(nowDay[0]),int(nowDay[1]),int(nowDay[2]))
   for i in range(0, len(postTime)):
        topicTimeDetail = postTime[i][0].split('-')
        endDay = datetime.datetime(int(topicTimeDetail[0]),int(topicTimeDetail[1]),int(topicTimeDetail[2]))
        if ((startDay - endDay).days) > 7:
            sql.updatePageNum(conn,postTime[i][1])

   while(len(postTime) > 23):
        sql.updateMaxIdPageNum(conn, --len(postTime))
        time.sleep(2)
        postTime = sql.getPostTime(conn, 1)
        

   url="http://www.newsmth.net/nForum/board/SoftwareTesting?p=1?ajax"
   parseurl = parseTestUrl(url, dataBasePath)
   urlNum = parseurl.getTopicID()

   for sqlID in postTime:
        mark = 0
        for id in urlNum:
            if int(sqlID[1]) == int(id):
                mark += 1
        if (mark == 0):
            tmpUrlID.append(sqlID[1])

   tmpUrlID.reverse()
   if len(tmpUrlID) > 0:
        unittest.main()
