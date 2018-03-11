# -*- coding: utf-8 -*-
"""
to fetch air pollutant data from
http://selenium-python.readthedocs.io/index.html
"""

import sys,time,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from html.parser import HTMLParser

global s
s = ""

driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://taqm.epa.gov.tw/taqm/tw/PamsDaily.aspx")

class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
                global s
                s = s + data+"\n"

#抓測站名稱(data_loc)和屬性值(select_sites)
data_select=driver.find_element_by_id("ctl09_ddlSite")
data_loc=data_select.text.split()
select_sites=data_select.get_attribute("innerHTML").split('">')
for i in range(len(data_loc)):
    select_sites[i]=str(select_sites[i])[-3:]
    if str(select_sites[i])[1].isdigit() == False:
        select_sites[i]=str(select_sites[i])[2]
    elif str(select_sites[i])[0].isdigit() == False:
        select_sites[i]=str(select_sites[i])[1:]
select_sites.pop()

# 照上式抓測項(data_items)和屬性值(select_items)
#select_items = [1]
#data_items = ["Ethane"]
data_select=driver.find_element_by_id("ctl09_ddlParam")
data_items=data_select.text.split()
select_items=data_select.get_attribute("innerHTML").split('">')
for i in range(len(data_items)):
    select_items[i]=str(select_items[i])[-3:]
    if str(select_items[i])[1].isdigit() == False:
        select_items[i]=str(select_items[i])[2]
    elif str(select_items[i])[0].isdigit() == False:
        select_items[i]=str(select_items[i])[1:]
select_items.pop()

# -- 年月:2016/06~nowDate
select_dates = []
nowdate=time.strftime("%Y/%m").split("/")
for i in range(2016,int(nowdate[0])+1):
        if i==int(nowdate[0]):
                for j in range(1,int(nowdate[1])+1):
                        select_dates.append(''.join(str(i)+"/"+str(j).zfill(2)))
        elif i==2016:
                for j in range(6,13):
                        select_dates.append(''.join(str(i)+"/"+str(j).zfill(2))) 
        else:
                for j in range(1,13):
                        select_dates.append(''.join(str(i)+"/"+str(j).zfill(2)))
"""
if os.path.isfile("tmp.txt"):
        f = open("tmp.txt",'a+',encoding='utf-8')
else:
        f = open("tmp.txt",'w+',encoding='utf-8')
"""
#f = open("tmp.txt",'w+',encoding='utf-8')
k=0
for query_site in select_sites:
        # -- 測站
        fail=0
        while fail<3:
                try:
                        elem_sites = Select(driver.find_element_by_id("ctl09_ddlSite"))
                        elem_sites.select_by_value(query_site)
                        time.sleep(2)
                        break
                except:
                        fail=fail+1
                        time.sleep(5)
        if fail==3:
                print("There is a problem with the connection.Please make sure the network environment is functional and retry.")
                break
        for i in range(len(select_items)):
                # -- 測項
                fail=0
                while fail<3:
                        try:
                                elem_data = Select(driver.find_element_by_id("ctl09_ddlParam"))
                                elem_data.select_by_value(str(select_items[i]))
                                time.sleep(2)
                                break
                        except:
                                fail=fail+1
                                time.sleep(5)
                if fail==3:
                        break
                for query_month in select_dates:
                        # -- 年月
                        s = ""
                        if os.path.isfile(data_loc[k]+".txt") == False:
                                s = "日期,"
                                for j in (range(len(data_items))):
                                        s = s+data_items[j]
                                        s = s+','
                                s = s + "標註"
                        s = s +"\n"
                        f = open(str(data_loc[k])+".txt",'a+',encoding='utf-8')
                        f.write(s)
                        s = ""
                        query_result = []
                        elem_dates = Select(driver.find_element_by_id("ctl09_ddlYM"))
                        try:
                                elem_dates.select_by_value(query_month)
                        except:
                                continue
                        time.sleep(2)
                        html = driver.page_source
                        parser = MyHTMLParser()
                        parser.feed(html)
                        data = s.split("\n")
                        for j in range(len(data)):
                                if data[j].startswith(query_month) and len(data[j].split('/'))>2:
                                        result_tmp=data[j:j+5]
                                        result_tmp.remove(data_loc[k])
                                        result_tmp.remove(data_items[i])
                                        query_result.append(','.join(result_tmp))
                                        #query_result.append(','.join(data[j:j+5]))
                                else:
                                        pass
                        f.write('\n'.join(query_result)+'\n')
        k=k+1                
        if fail==3:
                print("There is a problem with the connection.Please make sure the network environment is functional and retry.")
                break
driver.quit()
f.close()
