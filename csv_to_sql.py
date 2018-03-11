# -*- coding: utf-8 -*-

#import MySQLdb #--in python2.7
import pymysql #--in python3.6


import sys,time
import glob,os
import csv

if __name__ == "__main__":
    #--connect to sql database --連接sql資料庫
    #db = MySQLdb.connect(host="localhost",user="root", passwd="password", db="dbname")
    #db.set_character_set('utf8')
    db = pymysql.connect(host="localhost",user="root", passwd="password", db="dbname", charset='utf8')
    cursor = db.cursor()
    #dir to infiles folder --指向該資料夾位置 
    infile_dir = os.getcwd()                                            
    os.chdir(infile_dir)                                                
    infile_name=[""]
    fail=1
    #--get all file names --獲得該資料夾所有檔案的名稱  
    for fi in os.listdir('.'):                                              
        if os.path.isfile(fi):
            infile_name.append(fi)
    #--do files extensions are ".csv" --按照資料夾內的所有檔案名稱副檔名為.csv做處理
    for index in range(len(infile_name)):
        for infile_name[index] in glob.glob("*.csv"):
            fail=0
            j=0
            k=0
            date_done=[]
            item=[]
            row_count=0
            print(infile_name[index])
            with open(infile_name[index]) as f:
                f_csv = csv.reader(f)
                #--count the number of max rows and items in files--數文件內有多少列和有多少測項
                for count in f_csv:
                    row_count+=1
                    if(count[2] not in item):
                        item.append(count[2])
                item.pop(0)
                if item[-1]=="":
                    item.pop()
                #--determine column size,new row size,and temp list size by item size --用測項大小決定欄位數、新的列數，和暫存陣列大小
                maxcol=len(item)+1
                size=row_count/(len(item))*24
                f.seek(0)
                headers = next(f_csv)
                data_t =[""]*int(size)*(maxcol+1)
                #--chage format and store data in temp list(data_t),and i=hour,k=date,j=item --存放資料至暫存陣列(data_t)並更改格式，決定資料表名稱，i為小時，k為天數，j為測項
                for row in f_csv:
                    if(j==0):
                        table_name=row[0][:4]+"_"+row[1]
                        #outfile=open(row[0][:4]+"_"+row[1]+".txt","a+")
                    j=j+1
                    for i in range(0,24):
                        if(j!=0 and (j%(maxcol+1))==0):
                            j=1
                            k=k+1
                        if(j==1):
                            data_t[i*(maxcol+1)+k*24*(maxcol+1)]+=str(row[0])+"/"+str(i+1).zfill(2)
                        try:
                            data_t[i*(maxcol+1)+k*24*(maxcol+1)+j]+=str(row[i+3])
                        except:
                            data_t[i*(maxcol+1)+k*24*(maxcol+1)+j]+='-1'
                #--fix data might occur error,chage them as '-1'--將資料中有會使插入出錯的部分修改為'-1'
                for i in range(len(data_t)):
                    if(data_t[i][-1:]=='x' or data_t[i][-1:]=='#' or data_t[i][-1:]=='*' or data_t[i]=='NR' or data_t[i]=='NA' or data_t[i]=="" or data_t[i]==''):
                        data_t[i]='-1'
                #--create table and insert data --創建資料表並插入資料
                sql_create="""(日期 char(15) not null,PRIMARY KEY (`日期`)"""
                sql_insert="""(日期"""
                #print(item)
                #print(len(item))
                for i in range(len(item)):
                    if(str(item[i])=="PM2.5"):
                        sql_create=sql_create+",`%s` float"%(str(item[i]))
                        sql_insert=sql_insert+",`%s`"%(str(item[i]))
                    else:
                        sql_create=sql_create+",%s float"%(str(item[i]))
                        sql_insert=sql_insert+",%s"%(str(item[i]))
                sql_create=sql_create+")"
                sql_insert=sql_insert+") values("
                sql_insert_origin=sql_insert
                cursor.execute("create table if not exists "+table_name+sql_create)
                for i in range(int(len(data_t)/(maxcol+1))):
                    row=data_t[i*(maxcol+1):i*(maxcol+1)+(maxcol)]
                    sql_insert=sql_insert_origin
                    try:
                        for j in range(maxcol):
                            if j==0:
                                sql_insert=sql_insert+"'%s'"%(str(row[j]))
                                if str(row[j])=='-1':
                                    break
                            else:
                                sql_insert=sql_insert+",'%f'"%(float(row[j]))
                        sql_insert=sql_insert+")"
                        cursor.execute("insert into "+table_name+sql_insert)
                    except:
                        pass
                db.commit()

                """txt
                for i in range(len(data_t)):
                    if(i!=0 and i%17==0):
                        outfile.write("\n"+str(data_t[i]))
                    else:
                        outfile.write(str(data_t[i]))
                """
        break
    """txt
    try:   
        outfile.close()                                             # -- close outfile -- 關掉該文字檔
    except:
        pass
    """
    if fail == 1:
        print("Not found any .csv file! Please check .csv files and csv_to_sql.py in the same folder.")      
        time.sleep(5)
    
    # --關閉連線
    db.close()

