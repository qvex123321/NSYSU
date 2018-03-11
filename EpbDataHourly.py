# -*- coding: utf-8 -*-
"""
to fetch air pollutant data from
http://selenium-python.readthedocs.io/index.html
"""
import time,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from html.parser import HTMLParser
global s
s= ""

#-- 將擷取的HTML資料存成字串s
class MyHTMLParser(HTMLParser):
    def handle_data(self,data):
        global s
        s = s+ data+"\n"

#--將data(抓下來的資料)轉成data_t(文字檔的格式)的函式，ctlb為第x個測項，max_item為該測站總共有多少測項+1
def data_input(data_t,data,ctlb,max_item):              
    tt = time.strftime("%Y/%m/%d", time.localtime())    #--tt=現在時間
    for i in range(len(data)):
        if data[i]== tt:                                
            for j in range(24):
                data_t[ctlb+j*max_item+1] = data[i+1+j] #--ctlb為第x個測項,i為指到data的第幾行,j為時間,max_item該測站最多有幾種測項+1;將data(抓下來的資料)轉成data_t

driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://taqm.epa.gov.tw/taqm/tw/EpbDataHourly.aspx")

#抓測站名稱(data_loc)和屬性值(ct109_num)
data_loc=[]
ct109_num=[]
data_select=driver.find_element_by_id("ctl09_ddlSite")
loc_tmp=data_select.text.split()
num_tmp=data_select.get_attribute("innerHTML").split('">')
for i in range(len(loc_tmp)):
    num_tmp[i]=str(num_tmp[i])[-3:]
    if str(num_tmp[i])[1].isdigit() == False:
        num_tmp[i]=str(num_tmp[i])[2]
    elif str(num_tmp[i])[0].isdigit() == False:
        num_tmp[i]=str(num_tmp[i])[1:]
num_tmp.pop()
for i in range(len(loc_tmp)):
    if loc_tmp[i][0] =="高":
	    data_loc.append(loc_tmp[i])
	    ct109_num.append(num_tmp[i])

#抓測項名稱(data_item)和屬性值(ct109lb)
data_item=[]
ct109lb=[]
for i in range(len(data_loc)):
    elem_sites = Select(driver.find_element_by_id("ctl09_ddlSite"))
    elem_sites.select_by_value(str(ct109_num[i]))
    time.sleep(1)
    data_select=driver.find_element_by_id("ctl09_ddlParam")
    item_tmp=data_select.text.split()
    lb_tmp=data_select.get_attribute("innerHTML").split('">')
    for j in range(len(item_tmp)):
        lb_tmp[j]=str(lb_tmp[j])[-2:]
        if str(lb_tmp[j])[0].isdigit() == False:
            lb_tmp[j]=str(lb_tmp[j])[1]
    lb_tmp.pop()   
    data_item.append(item_tmp)
    ct109lb.append(lb_tmp)
#將data輸出成.txt檔，i為第x個測站
def output(data,i):
    s= ""
    if os.path.isfile(data_loc[i]+".txt") == False:
        s = "日期,"
        for j in (range(len(data_item[i]))):
            s = s+data_item[i][j]
            s = s+','
    s = s +"\n"
    for j in range(24*(len(data_item[i])+1)):
        if (data[j] == None) or (data[j] == " "):			#--檢查是否為空值
            data[j] = "None"
        elif (data[j] == "NA") or (data[j] == "#"):
            data[j] = "NA"
        elif data[j][0] =="." :									#--檢查是否為空值
            data[j] = "0"+data[j]
        if j%(len(data_item[i])+1) == 0:					#--檢查是否列印完一行(日期+測項)
            s = s+'\n'+ data[j]
        else:
            if all(u'\u4e00' <= word<= u'\u9fff' for word in str(data[j]))==True:#--檢查是否為中文
                if len(data[j])==3:
                    s = s+", "+data[j]
                elif len(data[j])==2:
                    s = s+",   "+data[j]
                elif len(data[j])==1:
                    s = s+",     "+data[j]
            else:
                s = s+","+data[j]
    f = open(data_loc[i]+".txt","a+")
    f.write(s)
    f.close()
#抓取網站上的資料
for i in range(len(ct109_num)):
    data_t = [None]*24*18
    elem_sites = Select(driver.find_element_by_id("ctl09_ddlSite"))
    elem_sites.select_by_value(str(ct109_num[i]))
    time.sleep(1)
    for j in range(len(ct109lb[i])):
        elem_data = Select(driver.find_element_by_id("ctl09_ddlParam"))
        elem_data.select_by_value(str(ct109lb[i][j]))
        time.sleep(1)
        html = driver.page_source
        parser = MyHTMLParser()
        parser.feed(html)
        data = s.split("\n")
        data_input(data_t,data,j,len(ct109lb[i])+1)
        if j == (len(ct109lb[i])-1):
                    data_input(data_t,data,j+1,len(ct109lb[i])+1)
        s = ""
    for k in range(24):
        data_t[k*(len(ct109lb[i])+1)] = time.strftime("%Y/%m/%d", time.localtime()) + "/"+str(k).zfill(2)
    output(data_t,i)
driver.quit()
