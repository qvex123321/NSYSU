import time,os

global s

from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
                global s 
                s = s + data+"\n"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
while(1):
        if time.strftime("%H:%M")== "00:10":
                s = ""
                t = time.strftime("%Y/%m/")+str(int(time.strftime("%d"))-1)
                driver = webdriver.Chrome("chromedriver.exe")
                driver.get("http://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx")
                cts = ["51","58","49","54","52","56","57","47","71","53","50","48"]
                ctlb = ["1","2","3","4","5","6","7","8","9","10","11","14","21","22","23","31","34","36","38","143","144"]
                ct = ["美濃","橋頭","仁武","鳳山","大寮","林園","楠梓","左營","前金","前鎮","小港","復興"]
                lb = ["SO2","CO","O3","PM10","NOx","NO","NO2","THC","NMHC","WIND_SPEED","WIND_DIREC","AMB_TEMP","PH_RAIN","RAIN_COND","RAINFALL","CH4","UVB","CO2","RH","WS_HR","WD_HR","PM2.5","PM2.5 原始值"]
                elem_sites = driver.find_element_by_id("ctl09_txtDateS")
                elem_sites.clear()
                elem_sites.send_keys(t)
                elem_sites = driver.find_element_by_xpath("//*[@id='ui-datepicker-div']/div[2]/button[2]")
                elem_sites.click()
                elem_sites = driver.find_element_by_id("ctl09_txtDateE")
                elem_sites.clear()
                elem_sites.send_keys(t)
                elem_sites = driver.find_element_by_xpath("//*[@id='ui-datepicker-div']/div[2]/button[2]")
                elem_sites.click()
                elem_sites = Select(driver.find_element_by_id("ctl09_lbSite"))
                elem_sites.deselect_all()
                for i in range(len(cts)):
                        elem_sites.select_by_value(cts[i])
                elem_data = Select(driver.find_element_by_id("ctl09_lbParam"))
                for i in range(len(ctlb)):
                        elem_data.select_by_value(ctlb[i])
                elem_data = Select(driver.find_element_by_id("ctl09_lbParam"))
                elem = driver.find_element_by_id("ctl09_btnQuery")
                elem.click()
                time.sleep(8)
                html = driver.page_source
                parser = MyHTMLParser()
                parser.feed(html)
                driver.quit()
                driver = webdriver.Chrome("chromedriver.exe")
                driver.get("http://taqm.epa.gov.tw/pm25/tw/HourlyData.aspx")

                ctlb = ["150","33"]
                for i in range(len(ctlb)):
                        elem_sites = driver.find_element_by_id("ctl14_txtDateS")
                        elem_sites.clear()
                        elem_sites.send_keys(t)
                        elem_sites = driver.find_element_by_xpath("//*[@id='ui-datepicker-div']/div[2]/button[2]")
                        elem_sites.click()
                        elem_sites = driver.find_element_by_id("ctl14_txtDateE")
                        elem_sites.clear()
                        elem_sites.send_keys(t)
                        elem_sites = driver.find_element_by_xpath("//*[@id='ui-datepicker-div']/div[2]/button[2]")
                        elem_sites.click()
                        elem_sites = Select(driver.find_element_by_id("ctl14_lbParam"))
                        elem_sites.select_by_value(ctlb[i])
                        elem_sites = Select(driver.find_element_by_id("ctl14_lbSite"))
                        elem_sites.deselect_all()
                        for i in range(len(cts)):
                                elem_sites.select_by_value(cts[i])
                        elem = driver.find_element_by_id("ctl14_btnQuery")
                        elem.click()
                        time.sleep(8)
                        html = driver.page_source
                        parser = MyHTMLParser()
                        parser.feed(html)
                driver.quit()
                data = [[None]*576 for i in range(12)]
                s = s.split("\n")
                sn = 0
                ln = 0
                for i in range(len(s)):
                        s_sp1 = s[i].split("：")
                        if(s_sp1[0] == "測站") :
                                sit = s_sp1[1][:-1]
                                for j in range(len(ct)):
                                        if sit == ct[j]:
                                                sn = j
                                                continue
                        if(s_sp1[0] == "測項"):
                                s_sp2 = s_sp1[1].split("（")
                                for j in range(len(lb)):
                                        if s_sp2[0] == lb[j]:
                                                ln = j
                                                continue
                        if(s_sp1[0]=="日期"):
                                for j in range(24):
                                        data[sn][1+ln+j*24] = str(s[i+30+j])

                if not os.path.isdir("result"):
                        os.mkdir("result")
                for i in range(12):
                        st = ""
                        f = ""
                        if not os.path.isfile(ct[i]+".txt"):
                                f = open("result/"+ct[i]+".txt","a+")
                                st = "日期\t\t\t"
                                for j in range(len(lb)):
                                        st = st + lb[j]
                                        if j == (len(lb)-1):
                                                break
                                        elif len(lb[j])<8:
                                                st = st+"\t\t"
                                        else:
                                                st = st+"\t"
                        else:
                                f = open("result/"+ct[i]+".txt","a+")
                        for j in range(576):
                                if (j%24 == 0):
                                        st = st+"\n"
                                        data[i][j] = t + "/" + str(int(j/24))
                                if data[i][j] == None:
                                        data[i][j] = "None"
                                st = st+data[i][j] + "\t\t"
                        f.write(st)
                        f.close()
        time.sleep(59)
