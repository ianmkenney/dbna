#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import time

asuid = raw_input("Enter your ASU ID: ")
asupass = raw_input("Enter your ASU Password: ")

filename = sys.argv[1]
print("Writing Task IDs to: {0}".format(filename))

driver = webdriver.Firefox()

driver.get("https://www.teamwork.com/launchpad/login?continue=/launchpad/welcome")
driver.find_element(By.LINK_TEXT, "Single Sign On (SSO)").click()
driver.find_element_by_id("loginemail").send_keys("pwberner@asu.edu")
driver.find_element_by_xpath("/html/body/div/div[1]/section/div[2]/div/div/div/form/div[2]/button/span").click()

time.sleep(3)

driver.find_element_by_id("username").send_keys(asuid)
driver.find_element_by_id("password").send_keys(asupass)
driver.find_element_by_class_name("submit").click()

raw_input("Press Any Key to Continue")

driver.get("https://clas.teamwork.com/#projects/568138/tasks")

raw_input("Select A Task List, then Press Enter")

# load completed in general
driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/div[1]/div[1]/section/div[1]/div[1]/div/div[2]/a/span").click()

# we want the thing
base = "/html/body/table/tbody/tr/td[2]/div[1]/div[1]/section/div[1]/div[1]/div/div[4]/div[{0}]/div[1]/div[2]/p/a"

xpath_by_index = lambda index : base.format(index)
loadplease = lambda : driver.find_element_by_class_name('moreData').click()
get_id = lambda elem : elem.get_attribute("href").split("/")[-1]

completed_ids = []

index = 2
while True:
    xpath = xpath_by_index(index)
    try:
        completed_ids.append(get_id(driver.find_element_by_xpath(xpath)))
    except:
        try:
            time.sleep(4)
            loadplease()
            time.sleep(4)
            completed_ids.append(get_id(driver.find_element_by_xpath(xpath)))
        except:
            break
    index += 1 

with open(filename, 'w') as f:
    for elem in completed_ids:
        f.write("{0}\n".format(elem))
