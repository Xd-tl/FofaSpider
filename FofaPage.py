#!/usr/bin/env python
# encoding: utf-8
'''

@Author         : xd
@Date           : 2021-12-08 23:24
@Description    : Fofa Crawl by page number.

'''
import argparse
import base64
import re
import time
from xlrd import open_workbook
from xlutils.copy import copy
import requests
import xlwt

headers = {}
fields = ['domain', 'host', 'ip', 'port', 'title', 'server', 'protocol', 'banner', 'city', 'region']

def logo():
    print("""
          
                                            .-'''-.                     
                 _______                   '   _    \                   
                 \  ___ `'.              /   /` '.   \                  
                  ' |--.\  \       _.._ .   |     \  '   _.._           
                  | |    \  '    .' .._||   '      |  '.' .._|          
   ____     _____ | |     |  '   | '    \    \     / / | '       __     
  `.   \  .'    / | |     |  | __| |__   `.   ` ..' /__| |__  .:--.'.   
    `.  `'    .'  | |     ' .'|__   __|     '-...-'`|__   __|/ |   \ |  
      '.    .'    | |___.' /'    | |                   | |   `" __ | |  
      .'     `.  /_______.'/     | |                   | |    .'.''| |  
    .'  .'`.   `.\_______|/      | |                   | |   / /   | |_ 
  .'   /    `.   `.              | |                   | |   \ \._,\ '/ 
 '----'       '----'             |_|                   |_|    `--'  `"  
                                                            Author : xd
                                                             CSDN  : https://blog.csdn.net/xd_2021
          """)
def excel(path):
    f = xlwt.Workbook()
    Sheet = f.add_sheet(u'Sheet', cell_overwrite_ok=True)  # 创建sheet
    # 将数据写入第 i 行，第 j 列
    for j in range(0, len(fields)):
        Sheet.write(0, j, fields[j])
    f.save("%s.xls" % path)
    f.save("./log/%s.xls.bak" % path)


def To_excel(list, path):
    try:
        r_xls = open_workbook('./log/%s.xls.bak' % path)
        row = r_xls.sheets()[0].nrows
        excel = copy(r_xls)
        table = excel.get_sheet(0)
        for data in list:
            for i in range(0, len(fields)):
                table.write(row, i, data[i])
            row += 1
        excel.save('./log/%s.xls.bak' % path)
        try:
            excel.save('%s.xls' % path)
        except Exception:
            pass
        return 0
    except Exception:
        return 1


# 获取某一页数据
def get(be64, page, filename):
    url = "https://api.fofa.so/v1/search?qbase64=%s&full=false&pn=%s&ps=10" % (be64.decode(), page)
    excel_list = []
    f = open('./log/%s.log' % filename, 'a')
    try:
        r = requests.get(url=url, headers=headers, timeout=10)
        data = r.json()['data']['assets']
        if data == []:
            f.write('\n--- There are %s pages in all ---\n' % page)
            print('\n--- There are %s pages in all ---' % page)
            f.close()
            return 1
        for i in data:
            list = []
            for j in fields:
                list.append(i[j])
            excel_list.append(list)
    except Exception:
        query = base64.b64decode(be64)
        f.write('\n--- %s Exception request ---\n' % query.decode())
        f.close()
        print('\n--- %s Exception request ---' % query.decode())
        return -1
    if To_excel(excel_list, filename) == 0:
        f.write('[+] Page %s loads into Excel\n' % page)
        print('[+] Page %s loads into Excel' % page)
    else:
        f.write('[+] Page %s failed to load into Excel\n' % page)
        print('[+] Page %s failed to load into Excel' % page)
    f.close()
    return 0


# 查询
def rule(query, page):
    query_base64 = base64.b64encode(query.encode(encoding='utf-8'))
    filename = '%s' % int(time.time())
    excel(filename)
    f = open('./log/%s.log' % filename, 'a')
    f.write("query: %s\n\n" % query)
    f.close()
    print("query: %s\n" % query)
    for i in range(1, page):
        if get(query_base64, i, filename) != 0:
            break


def main():
    logo()
    parser = argparse.ArgumentParser(description='Fofa Crawl by page number.')
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Please enter a query statement. e.g: -q \"app=\'Landray-OA系统\'&&country=\'CN\'\"",
        metavar='')
    args = parser.parse_args()
    query = args.query
    query = query.replace("'", "\"")
    config = open('config').read().split('\n')
    pattern = re.compile('fofa_token=.*?;')
    Authorization = pattern.search(config[0])[0][:-1].split('=')[1]
    Size = config[1].split('=')[1]
    headers['Authorization'] = Authorization
    page = int(int(Size) / 10) + 1
    page = page if int(Size) % 10 == 0 else page + 1
    rule(query, page)


if __name__ == "__main__":
    main()
