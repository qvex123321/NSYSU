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
s = ""

query_result = []
final_table = {}

# -- 測站:愛國
select_sites = ["11"]
# -- 測項
ct109lb = [1] #,2,3,4,5,6,7,8,9,10,11,14,31,33,38]
data_item = ["SO2"] #,"CO","O3","PM10","NOx","NO","NO2","THC","NMHC","WIND_SPEED","WIND_DIREC","AMB_TEMP","CH4","PM2.5","RH"]
# -- 年月
past_year = ["2016/05"] #,"2016/06","2016/07","2016/08","2016/09","2016/10","2016/11","2016/12","2017/01","2017/02","2017/03","2017/04","2017/05","2017/06"]

class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
                global s
                #print(data)
                s = s + data+"\n"

driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://taqm.epa.gov.tw/taqm/tw/EpbDataHourly.aspx")
for query_site in select_sites:
        # -- 測站
        elem_sites = Select(driver.find_element_by_id("ctl09_ddlSite"))
        elem_sites.select_by_value(query_site)
        time.sleep(1)

        for i in range(len(ct109lb)):
                # -- 測項
                elem_data = Select(driver.find_element_by_id("ctl09_ddlParam"))
                elem_data.select_by_value(str(ct109lb[i]))
                time.sleep(1)
                # -- 年月
                for query_month in past_year:        
                        elem_sites = Select(driver.find_element_by_id("ctl09_ddlYM"))
                        try:
                                elem_sites.select_by_value(query_month)
                        except:
                                continue
                
                        time.sleep(2)

                        html = driver.page_source
                        parser = MyHTMLParser()
                        parser.feed(html)
                        data = s.split("\n")
                
                        for j in range(len(data)):
                                if data[j].startswith(query_month):
                                        query_result.append(data[j:j+25])
                        
                        for each_day in range(1,len(query_result)):
                                for each_hour in range(24):
                                        day_hour_key = query_result[each_day][0] + "/" + str(each_hour)

                                        if day_hour_key in final_table:
                                                final_table[day_hour_key].append(query_result[each_day][each_hour+1])
                                        else:
                                                final_table[day_hour_key] = [query_result[each_day][each_hour+1]]
                
                        s = ""
                        query_result = []
driver.quit()

# -- print
f = open("地方監測站小時值.txt","a+")
for key in final_table.keys():
        result_line = key + ‘,’ + ‘,’.join(final_table[key])
        f.write(result_line+'\n')
f.close()




