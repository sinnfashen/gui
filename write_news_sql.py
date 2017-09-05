# -*- coding:utf8 -*-
"""
Created on Sat May 13 23:17:41 2017

@author: Administrator
"""
#  import module
import os
import re
import csv
import shutil
import pandas as pd
import sqlite3 as lite
import pandas.io.sql as pd_sql

def file_move(truedir, mpath):
    x = truedir.replace(mpath, '')
    divs = x.split('\\')[1:]
    dict = "newspaper"
    for div in divs[:-1]:
        dict = os.path.join(dict, div)
        try:
            os.mkdir(dict)
        except FileExistsError:
            pass
    dict = os.path.join(os.getcwd(), dict, divs[-1])
    shutil.copyfile(truedir, dict)

        # get all the file with name and position
def get_file_name(dir):
    file_name = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            try:
                if file[-4:] == ".pdf":
                    if file.find(' ') != -1:
                        f = os.path.join(root, file)
                        os.rename(f, os.path.join(root, file.replace(' ', '')))
                        file = file.replace(' ', '')
                    f = os.path.join(root, file)
                    os.system('pdftotext.exe -enc UTF-8 -table {}'.format(f))
                    file = '{}.txt'.format(file[:-4])
                    f = os.path.join(root, file)
                    parent, gupiao = os.path.split(root)
                    parent, gongsi = os.path.split(parent)
                    a = {}
                    a["position"] = f
                    a["root"] = root
                    a["file"] = file
                    a["gongsi"] = gongsi
                    a["gupiao"] = gupiao
                    file_name.append(a)
            except:
                pass
    return file_name


# from file get newspaper, year, month, day, banmian, zuozhe
# from file get newspaper, year, month, day, banmian, zuozhe
def get_infor(file_name, mpath):
    file_infor = []
    for file in file_name:
        position = file["position"]
        f = open(position, "r", encoding='UTF-8')

        try:
            line = f.readline()
            i = 0
            while ("/" not in line) and i < 7:
                line = f.readline()
                i = i + 1
        except:
            pass

        f.close()
        file_move(file['position'], mpath)
        file['position'] = file['position'].replace(mpath, 'H:\\newspaper')

        try:
            line = line.strip()
            #            line = line.strip().decode('utf8').encode('gb2312')

            file["infor"] = line
        except:
            pass

        # get newspaper, year, month, day, banmian
        try:
            #            print line
            infor = line.split('/')
            file["newspaper"] = infor[0]
            file["year"] = infor[1]
            file["month"] = infor[2]
            file["day"] = infor[3]
            file["banmian"] = infor[4]
        except:
            pass

        # get zuozhe
        try:
            file["zuozhe"] = file["file"].split('_')[-1][0:-4]
        except:
            pass

        # get title_docu
        try:
            file["title_docu"] = "".join(file["file"].split('_')[0:-1])
        except:
            pass

        file_infor.append(file)
    return file_infor


# cleanig use in dataframe
def replace_year(word):
    word = str(word)
    word = re.sub("\年$", "", word)
    return word


def replace_month(word):
    word = str(word)
    word = re.sub("\月$", "", word)
    return word


def replace_day(word):
    word = str(word)
    word = re.sub("\日$", "", word)

    return word


def replace_gupiao(number):
    number = str(number)
    while len(number) < 6:
        number = re.sub("^", "0", number)
    return number


# write the infor to sql
def write_sql(file_infor, m):
    table = pd.DataFrame(file_infor)
    try:
        table['year'] = table['year'].apply(lambda x: replace_year(x))
    except:
        pass

    try:
        table['month'] = table['month'].apply(lambda x: replace_month(x))
    except:
        pass

    try:
        table['day'] = table['day'].apply(lambda x: replace_day(x))
    except:
        pass

    try:
        table['gupiao'] = table['gupiao'].apply(lambda x: replace_gupiao(x))
    except:
        pass

    cnx = lite.connect('You_Database.db')
    cnx.text_factory = str
    try:
        sql_df = table.loc[:,
                 ['banmian', 'day', 'file', 'gongsi', 'gupiao', 'month', 'newspaper', 'position', 'root', 'title_docu',
                  'year', 'zuozhe']]
        pd.io.sql.to_sql(sql_df, name='You_Gongsi', con=cnx, if_exists='append')
    except:
        print(m + 'fail to load')


def main(mpath):
#    mpath = "H:\\newspaper" # 此处写报纸所在的整个文件夹位置，一层为1,2,3...，二层为股票编号。
#    spath = "C:\\Users\\Administrator\\Desktop" #此处为csv存放的位置，子文件夹为1.csv,2.csv...
    if mpath[-9:] != "newspaper":
        raise EnvironmentError
    files = os.listdir(mpath)
    for file in files:
        m = os.path.join(mpath, file)
        #        s = os.path.join(spath,file)+'.csv'
        file_name = get_file_name(m)
        file_infor = get_infor(file_name, mpath)
        write_sql(file_infor, m)

if __name__ == "__main__":
    main("C:\\Users\\54926\\Documents\\GitHub\\gui\\newspaper")










