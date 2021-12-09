#!/usr/bin/env python
# encoding: utf-8
'''

@Author         : xd
@Date           : 2021-12-08 23:24
@Description    : Fofa Crawl by page number.

'''
import argparse
import ast
import base64
import json
import re
import time
from xlrd import open_workbook
from xlutils.copy import copy
import requests
import xlwt

fields = ['domain', 'host', 'ip', 'port', 'title', 'server', 'protocol', 'banner', 'city', 'region']
headers = {}
page = 0
fragile = []


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


def get_shengji(str, num):
    list = []
    try:
        r = requests.get(url="http://xzqh.mca.gov.cn/map", timeout=5, verify=False)
        shengji = re.search(r'value=\'\[\{.*\}\]', r.text).group().split('\'')
        shengji = json.loads(shengji[1])
        code = ''
        for i in shengji:
            if str in i['cName']:
                code = i['code']
                break
        num += 3
        code = code[:num]
        for i in shengji:
            if code in i['code'][:num]:
                list.append(i['cName'])
        return list
    except Exception:
        pass


# 获取某一页数据
def get(be64, page, filename):
    url = "https://api.fofa.so/v1/search?qbase64=%s&full=false&pn=%s&ps=10" % (be64.decode(), page)
    excel_list = []
    f = open('./log/%s.log' % filename, 'a')
    try:
        r = requests.get(url=url, headers=headers, timeout=10)
        data = r.json()['data']['assets']
        if data == []:
            f.write('\n--- There are %s pages in all ---\n' % (page - 1))
            print('\n--- There are %s pages in all ---' % (page - 1))
            f.close()
            return 1
        for i in data:
            list = []
            for j in fields:
                list.append(i[j])
            excel_list.append(list)
    except Exception:
        query = base64.b64decode(be64)
        f.write('\n--- %s Load page 11 exception ---\n' % page)
        f.close()
        print('\n--- %s Load page 11 exception ---' % page)
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
def rule(query):
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


def asset(city, province):
    global page
    parameter = get_shengji(city, province)
    print("Looking for vulnerable targets")
    print(fragile)
    print("The city list:")
    print(parameter)
    filename = '%s' % int(time.time())
    excel(filename)
    for parameter1 in parameter:
        for parameter2 in fragile:
            query = 'title="%s"&&title="%s"&&country="CN"&&region!="HK"' % (parameter1, parameter2)
            f = open('./log/%s.log' % filename, 'a')
            f.write("query: %s\n\n" % query)
            f.close()
            print("query: %s\n" % query)
            query_base64 = base64.b64encode(query.encode(encoding='utf-8'))
            val = 0
            for i in range(1, page):
                if get(query_base64, i, filename) != 0:
                    val = i
                    break
            page -= val - 1


def main():
    logo()
    parser = argparse.ArgumentParser(description='Fofa Crawl by page number.')
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Please enter a query statement. e.g: -q \"app=\'Landray-OA系统\'&&country=\'CN\'\"",
        metavar='')
    parser.add_argument(
        "-c",
        "--city",
        type=str,
        help="Please enter a query statement. e.g: -c \"city\"",
        metavar='')
    parser.add_argument(
        "-p",
        "--province",
        type=int,
        help="0 is province, 1 is city,default=True e.g: -p 0",
        default=0,
        metavar='')
    args = parser.parse_args()

    # 获取用户输入
    query = args.query
    city = args.city
    province = args.province

    # 获取config配置
    global page
    global fragile

    config = open('config', encoding='utf-8').read().split('\n')
    pattern = re.compile('fofa_token=.*?;')
    Authorization = pattern.search(config[0])[0][:-1].split('=')[1]
    Size = config[1].split('=')[1]
    headers['Authorization'] = Authorization
    page = int(int(Size) / 10) + 1
    page = page if int(Size) % 10 == 0 else page + 1
    fragile = config[2].split('=')[1]
    fragile = ast.literal_eval(fragile)

    if not query is None and not city is None:
        print("q and c cannot be used at the same time.....")
        return
    elif not query is None:
        query = query.replace("'", "\"")
        rule(query)
    elif not city is None:
        asset(city, province)
    else:
        print("syntax error....")


if __name__ == "__main__":
    main()
