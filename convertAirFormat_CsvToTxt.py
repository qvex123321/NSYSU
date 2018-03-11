# -*- coding: utf-8 -*-
"""
$sudo easy_install pip
$sudo pip install xlrd
to convert a specific data type
"""

import sys,time
import glob,os
#import xlrd # -- to directly open xls file
import csv

if __name__ == "__main__":
    infile_dir = os.getcwd()                                            # -- get infiles folder(folder which contain convertAirFormat.py) -- 獲得convertAirFormat.py所在的資料夾位置
    os.chdir(infile_dir)                                                # -- dir to infiles folder -- 指向該資料夾位置 
    infile_name=[""]
    fail=1
    for fi in os.listdir('.'):                                           # -- get all file names -- 獲得該資料夾所有檔案的名稱     
        if os.path.isfile(fi):
            infile_name.append(fi)
    for index in range(len(infile_name)):
        for infile_name[index] in glob.glob("*.csv"):
            fail=0 
            with open(infile_name[index]) as f:
                f_csv = csv.reader(f)
                headers = next(f_csv)
                for row in f_csv:
                    outfile=open(row[1]+"_"+row[2]+".txt","a+")
                    for i in range(0,24):
                        outfile.write(str(row[0])+"/"+str(i).zfill(2)+',')
                        outfile.write(str(row[i+3]))
                        outfile.write("\n")
        break
        try:   
            outfile.close()                                             # -- close outfile -- 關掉該文字檔
        except:
            continue                                                 
    if fail == 1:
        print("Not found any .csv file! Please check .csv files and convertAirFormat_CsvToTxt.py in the same folder.")      
        time.sleep(5)
