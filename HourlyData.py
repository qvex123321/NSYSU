# -*- coding: utf-8 -*-
"""
to fetch air pollutant data from
http://selenium-python.readthedocs.io/index.html
"""
import time,os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# http://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx        	#　環保署
# http://taqm.epa.gov.tw/pm25/tw/HourlyData.aspx		#　環保署

global s
s = ""

# -- print
from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
                global s
                s = s + data+"\n"

driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx")
#抓測站名稱(data_loc)和屬性值(ct109_num)
data_loc=[]
ct109_num=[]
data_select=driver.find_element_by_id("ctl09_lbSite")
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
data_select=driver.find_element_by_id("ctl09_lbParam")
item_tmp=data_select.text.split()
lb_tmp=data_select.get_attribute("innerHTML").split('">')
for j in range(len(item_tmp)):
        lb_tmp[j]=str(lb_tmp[j])[-3:]
        if str(lb_tmp[j])[1].isdigit() == False:
                lb_tmp[j]=str(lb_tmp[j])[2]
        elif str(lb_tmp[j])[0].isdigit() == False:
                lb_tmp[j]=str(lb_tmp[j])[1:]
lb_tmp.pop()   
data_item=item_tmp
ct109lb=lb_tmp
ct109_lbitem_tmp=data_item

elem_sites = Select(driver.find_element_by_id("ctl09_lbSite"))	# -- to get Kaohsiung
elem_sites.deselect_all()                                       # -- deselect all
for i in range(len(ct109_num)):
        elem_sites.select_by_value(str(ct109_num[i]))
elem_data = Select(driver.find_element_by_id("ctl09_lbParam"))	# -- to get all
for i in range(len(ct109lb)):
        elem_data.select_by_value(str(ct109lb[i]))
elem = driver.find_element_by_id("ctl09_btnQuery")
elem.click()
time.sleep(8)
html = driver.page_source					# -- to parse the result
parser = MyHTMLParser()
parser.feed(html)

driver.quit()
#-------------------------------------------------------------------------------------------------------------
driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://taqm.epa.gov.tw/pm25/tw/HourlyData.aspx")
#抓測站名稱(data_loc)和屬性值(ct108_num)
data_loc=[]
ct108_num=[]
data_select=driver.find_element_by_id("ctl08_lbSite")
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
            ct108_num.append(num_tmp[i])
            data_loc.append(loc_tmp[i])

#抓測項名稱(data_item)和屬性值(ct108lb)
data_item=[]
ct108lb=[]
data_select=driver.find_element_by_id("ctl08_lbParam")
item_tmp=data_select.text.split()
lb_tmp=data_select.get_attribute("innerHTML").split('">')
for j in range(len(item_tmp)):
        lb_tmp[j]=str(lb_tmp[j])[-3:]
        if str(lb_tmp[j])[1].isdigit() == False:
                lb_tmp[j]=str(lb_tmp[j])[2]
        elif str(lb_tmp[j])[0].isdigit() == False:
                lb_tmp[j]=str(lb_tmp[j])[1:]
lb_tmp.pop()
item_tmp[0]=item_tmp[0]+" "+item_tmp[1]
item_tmp.pop(1)
data_item=item_tmp
ct108lb=lb_tmp

def data_input(data_t,data):
        times = ""
        path = ""
        item_num = -1
        loc = -1
        for i in range(len(data)):
                if (data[i]==""):
                        continue
                data_itch = data[i].split("：")
                if (data_itch[0] == "監測年月")|(data_itch[0] == "年月（監測時間）"):
                        times = str(str(data_itch[1]).split("，")[0])
                if data_itch[0] == "測站":
                        path = data_itch[1]
                        path=str(path.split("，")[0])
                        for j in range(len(data_loc)):
                                if str(data_loc[j])[-2:] == path:
                                        loc = j
                if data_itch[0] == "測項":
                        data_itch_dc = data_itch[1].split("（")
                        for j in range(len(data_item)):
                                if data_itch_dc[0]==data_item[j]:
                                        item_num = j
                                        break
                if data_itch[0] == "日期":
                        date = data[i+24+5].split("/")
                        times = times+"/"+date[1]
                        for j in range(24):
                                data_t[loc][j*24] = times+"/"+str(j).zfill(2)
                                data_t[loc][item_num+1+j*24] = data[24+1+i+j+5]
                if len(data_itch)<0:
                        break
                elif data_itch[0]== "\n":
                        times = ""
                        item_num = -1

def output(data):
        if not os.path.isdir("result"):
                os.mkdir("result")
        for i in range(len(data_loc)):
                s= ""

                if (os.path.isfile("result/"+data_loc[i]+".txt") == False):
                        s = "日期\t\t\t"
                        for j in range(len(data_item)):
                                s = s+str(data_item[j])
                                if (len(data_item[j])>7):
                                        s = s+"\t"
                                else:
                                        s = s+"\t\t"
                s = s +"\n"
                for j in range(576):
                        if(str(data[i][j])[0])==".":
                                data[i][j]="0"+str(data[i][j])
                        if j%24 == 0:
                                s = s+"\n"+ str(data[i][j])
                        else:
                                s = s+"\t\t"+str(data[i][j])
                f = open("result/"+data_loc[i]+".txt","a+")
                f.write(s)
                f.close()
   
#--get data----------------------------
elem_date = driver.find_element_by_id("ctl08_txtDateS")
elem_date.clear()
elem_date.send_keys(str(time.strftime("%Y/%m/%d", time.localtime())))
elem_ex = driver.find_element_by_xpath("//*[@id='ui-datepicker-div']/div[2]/button[2]")
elem_ex.click()
elem_sites = Select(driver.find_element_by_id("ctl08_lbSite"))	        # -- to get Kaohsiung
elem_sites.deselect_all()                                               # -- deselect all
for i in range(len(ct108_num)):                                    
        elem_sites.select_by_value(str(ct108_num[i]))                   # -- select by ct108_num[i]
for j in range(len(ct108lb)):
        elem_data = Select(driver.find_element_by_id("ctl08_lbParam"))	# -- to get all
        elem_data.select_by_value(ct108lb[j])                           # -- select by ct108lb[j]
        elem = driver.find_element_by_id("ctl08_btnQuery")
        elem.click()
        time.sleep(8)
        html = driver.page_source					# -- to parse the result
        parser = MyHTMLParser()
        parser.feed(html)
data_t=[]
for i in range(len(data_loc)):
        data_tmp=[None]*576
        data_t.append(data_tmp)                                         # -- data[len(ct108_num)][576]={None}
data = s.split("\n")
data_item=ct109_lbitem_tmp
for i in range(len(item_tmp)):
        data_item.append(item_tmp[i])
#data_item = ["SO2","CO","O3","PM10","NOx","NO","NO2","THC","NMHC","WIND_SPEED","WIND_DIREC","AMB_TEMP","PH_RAIN","RAIN_COND","RAINFALL","CH4","UVB","CO2","RH","WS_HR","WD_HR","PM2.5","PM2.5 原始值"]
#data_loc = ["大寮","小港","仁武","左營","林園","前金","前鎮","美濃","復興","楠梓","鳳山","橋頭"]

data_input(data_t,data)
output(data_t)
driver.quit()
