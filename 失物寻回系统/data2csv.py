# -*- coding: utf-8 -*-
import csv

# 将数据输出到CSV文件
def printf(csvname, title, content):
    with open(csvname+".csv",'w',newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(title)
        #print(content)
        writer.writerows(content)
        csvfile.close()