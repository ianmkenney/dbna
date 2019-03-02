#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import sys
import time

filename = sys.argv[1]

ids = []

with open(filename, 'r') as f:
    for line in f:
        ids.append(line.strip())

driver = webdriver.Firefox()

driver.get("https://www.teamwork.com/launchpad/login?continue=/launchpad/welcome")
driver.find_element(By.LINK_TEXT, "Single Sign On (SSO)").click()
driver.find_element_by_id("loginemail").send_keys("pwberner@asu.edu")
driver.find_element_by_xpath("/html/body/div/div[1]/section/div[2]/div/div/div/form/div[2]/button/span").click()

raw_input("press any key")

taskurlbase = "https://clas.teamwork.com/#tasks/{0}"

columns = ["taskid", "category", "country", "state", "city", "varname", "comment"]
df = pd.DataFrame(columns=columns)

urlbyid      = lambda index : taskurlbase.format(index)
_category    = lambda : driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/div/div[2]/div[2]/div/div/p[1]/a").text
_getlocation = lambda : tuple([i.strip() for i in driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/div/div[2]/div[2]/div/div/p[2]/a").text.split(">")])
_varname     = lambda : driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/div[1]/div[1]/section/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/p/span").text.split("-")[-1].strip()
_comment     = lambda : driver.find_element_by_id("taskComments").text

for i in ids:
    url = urlbyid(i)
    driver.get(url)
    time.sleep(3)
    try:
        category = _category()
        if not driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/div/div[2]/div[2]/div/div/h3[2]").text == u'Parent Task':
            continue
    except:
        time.sleep(5)
        driver.find_element_by_id("sidebarToggle").click()
    
    if not driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/div/div[2]/div[2]/div/div/h3[2]").text == u'Parent Task':
        continue
    category = _category()
    country, state, city = _getlocation()
    varname = _varname()
    comment = _comment()
    df = df.append(pd.DataFrame([[i,category, country, state, city, varname, comment]], columns=columns))

df.to_csv(filename.replace(".txt", ".csv"),sep="|", encoding='utf-8',index=False)
