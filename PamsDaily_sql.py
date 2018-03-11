# -*- coding: utf-8 -*-
"""
to fetch air pollutant data from
http://selenium-python.readthedocs.io/index.html
"""
#import MySQLdb
import pymysql
import sys,time,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from html.parser import HTMLParser

global s
s = ""

class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
                global s
                s = s + data+"\n"

if __name__ =='__main__':
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get("http://taqm.epa.gov.tw/taqm/tw/PamsDaily.aspx")
        #db = MySQLdb.connect(host="localhost",user="root", passwd="password", db="databasename")
        #db.set_character_set('utf8')
        db = pymysql.connect(host="localhost",user="root", passwd="password", db="databasename", charset='utf8')
        cursor = db.cursor()
        

        #select_sites=["1"]
        #data_loc=["萬華"]
        
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
        
        # -- 測項:Ethane
        #select_items = [1]
        #data_items = ["Ethane"]
        
        # 抓測項(data_items)和屬性值(select_items)
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

        k=0
        table_name=[]
        #table_name=""
        for query_site in select_sites:
        # -- 測站-now total:12
                fail=0
                just_create=False
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
                # -- 測項-now total:55
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
                                """
                                if os.path.isfile(data_loc[k]+".txt") == False:
                                        s = "日期,"
                                        for j in (range(len(data_items))):
                                                s = s+data_items[j]
                                                s = s+','
                                        s = s + "標註"
                                s = s +"\n"
                                f = open(str(data_loc[k])+".txt",'a+',encoding='utf-8')
                                f.write(s)
                                """
                                query_result = []
                                try:
                                        elem_dates = Select(driver.find_element_by_id("ctl09_ddlYM"))
                                        elem_dates.select_by_value(query_month)
                                except:
                                        continue
                                time.sleep(2)
                                html = driver.page_source
                                parser = MyHTMLParser()
                                parser.feed(html)
                                data = s.split("\n")
                                row=0
                                for j in range(len(data)):
                                        if data[j].startswith(query_month) and len(data[j].split('/'))>2:
                                                result_tmp=data[j:j+5]
                                                result_tmp.remove(data_loc[k])
                                                result_tmp.remove(data_items[i])
                                                query_result.append(','.join(result_tmp))
                                                #query_result.append(','.join(data[j:j+5]))

                                                table_name=query_month[0:4]+'_'+data_loc[k]
                                                
                                                try:
                                                        #--加入測項至欄位
                                                        sql_add="""%s float"""%(str(data_items[i]))
                                                        cursor.execute("alter table "+table_name+" add column "+sql_add)
                                                        just_create=True
                                                except:
                                                        try:
                                                                #用select選取要新增的範圍
                                                                sql_select=""" SELECT * FROM """
                                                                cursor.execute(sql_select+table_name)

                                                        except:
                                                                #--創建名為"table_name"(年份_測站)的表
                                                                sql_create="""(
                                                                                日期 char(15) not null,
                                                                                %s float,
                                                                                PRIMARY KEY (`日期`))"""%(str(data_items[i]))
                                                                cursor.execute("create table "+table_name+sql_create)
                                                                just_create=True
                                                                
                                                #cursor.execute("SELECT 日期,Ethane FROM "+table_name)                                                                       cursor.execute(sql_select+table_name)
                                                sql_data = cursor.fetchall()
                                                
                                                if (just_create!=True):
                                                        #調整時間(列)
                                                        while(sql_data[row][0]!=result_tmp[0]):
                                                                if(int(sql_data[row][0][5:7])<int(query_month[-2:])):
                                                                        row=row+2
                                                                elif(int(sql_data[row][0][5:7])==int(query_month[-2:])):
                                                                        if(int(sql_data[row][0][-2:])<int(result_tmp[0][-2:])):
                                                                                row=row+1
                                                                        elif(int(sql_data[row][0][-2:])>int(result_tmp[0][-2:])):
                                                                                row=row-1
                                                        #確認相同或空值
                                                        if(sql_data[row][1]=='null' or float(sql_data[row][1])!=float(result_tmp[1])):
                                                                if(result_tmp[2]=="無效"):
                                                                        sql_insert="""(日期,%s) values('%s','-1')"""%(str(data_items[i]),str(result_tmp[0]))
                                                                        sql_update=""" %s='-1' where 日期='%s'"""%(str(data_items[i]),str(result_tmp[0]))
                                                                        
                                                                else:
                                                                        sql_insert="""(日期,%s) values('%s','%f')"""%(str(data_items[i]),str(result_tmp[0]),float(result_tmp[1]))
                                                                        sql_update=""" %s='%f' where 日期='%s'"""%(str(data_items[i]),float(result_tmp[1]),str(result_tmp[0]))
                                                                try:
                                                                        cursor.execute("insert into "+table_name+sql_insert)
                                                                except:

                                                                        sql_update=""" %s='%f' where 日期='%s'"""%(str(data_items[i]),float(result_tmp[1]),str(result_tmp[0]))
                                                                        cursor.execute("update "+table_name+" set "+sql_update)

                                                #若表為剛建立或加入測項
                                                else:
                                                        try:
                                                                if(result_tmp[2]=="無效"):
                                                                        sql_insert="""(日期,%s) values('%s','-1')"""%(str(data_items[i]),str(result_tmp[0]))
                                                                        sql_update=""" %s='-1' where 日期='%s'"""%(str(data_items[i]),str(result_tmp[0]))
                                                                else:
                                                                        sql_insert="""(日期,%s) values('%s','%f')"""%(str(data_items[i]),str(result_tmp[0]),float(result_tmp[1]))
                                                                        sql_update=""" %s='%f' where 日期='%s'"""%(str(data_items[i]),float(result_tmp[1]),str(result_tmp[0]))
                                                                cursor.execute("insert into "+table_name+sql_insert)
                                                                #print("insert into "+table_name+sql_insert)
                                                        except:
                                                                try:
                                                                        #sql_update=""" %s='%f' where 日期='%s'"""%(str(data_items[i]),float(result_tmp[1]),str(result_tmp[0]))
                                                                        cursor.execute("update "+table_name+" set "+sql_update)                                                                except:
                                                                        pass
                                                db.commit()
                        else:
                                pass

                                #f.write('\n'.join(query_result)+'\n')
                k=k+1                
                if fail==3:
                        print("There is a problem with the connection.Please make sure the network environment is functional and retry.")
                        break
        driver.quit()
        db.close()
        #f.close()
