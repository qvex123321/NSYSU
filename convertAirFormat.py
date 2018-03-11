# -*- coding: utf-8 -*-
"""
$sudo easy_install pip
$sudo pip install xlrd
to convert a specific data type
"""

import sys,time
import glob,os
import xlrd # -- to directly open xls file

if __name__ == "__main__":
    infile_dir = os.getcwd()                                            # -- get infiles folder(folder which contain convertAirFormat.py) -- 獲得convertAirFormat.py所在的資料夾位置
    os.chdir(infile_dir)                                                # -- dir to infiles folder -- 指向該資料夾位置 
    infile_name=[""]
    fail=1
    for f in os.listdir('.'):                                           # -- get all file names -- 獲得該資料夾所有檔案的名稱     
        if os.path.isfile(f):
            infile_name.append(f)
    for index in range(len(infile_name)):
        for infile_name[index] in glob.glob("*.xls"):                   # -- get all *.xls files -- 只獲得資料夾內所有副檔名為.xls的檔案
            fail=0
            book = xlrd.open_workbook(infile_name[index])               # -- open and get the workbook named (infile_name[index]) -- 開啟並獲得名稱為(infile_name[index])工作簿
            work_sheet = book.sheet_by_index(0)                         # -- get the worksheet[0] in workbook -- 獲得工作簿中的索引值為0的工作表
            current_row = 1                                             # -- start from 1 -- 從第1行開始
            num_rows = work_sheet.nrows                                 # -- get worksheet row numbers  -- 獲得工作表中的總行數
        
            while current_row < num_rows:
                outfile_name = str(work_sheet.cell_value(current_row,1))+"_"+str(work_sheet.cell_value(current_row,2))+'.txt'    # -- name the output txt after station's name and test item's name -- 將輸出的文字檔命名為"(測站)_(測項)"
                outfile = open(outfile_name,'a+')                                               
                for j in range(0,24):
                    outfile.write(str(work_sheet.cell_value(current_row,0))+'/'+str(j).zfill(2)+',')    # -- write date/hour, -- 寫入(data)/(hour),
                    outfile.write(str(work_sheet.cell_value(current_row,j+3)))                          # -- write value -- 寫入(value)
                    outfile.write('\n')                                                                 
                current_row += 1
        break
        try:   
            outfile.close()                                             # -- close outfile -- 關掉該文字檔
        except:
            continue                                                 
    if fail == 1:
        print("Not found any .xls file! Please check .xls files and convertAirFormat.py in the same folder.")      
        time.sleep(5)
