import requests
import time
from bs4 import BeautifulSoup
import re
import DynamoDB
import DBDataConv
import decimal
from Web import KabutanAccess as kb
import csv
from datetime import datetime as dt

def convert_decimal(val,deli=','):
    return decimal.Decimal(val.replace(deli,''))

def check_value_convert(val):
    if val != '－':
        return convert_decimal(val)
    else:
        return None

def web_access_method_factory(url):
    kbtn = kb.KabutanAccess()
    kbtn.set_url(url)
    return kbtn

def finance_page_html_source(page_url,stock_code):
    kbtn = web_access_method_factory(page_url)
    params = {'code': stock_code}
    kbtn.set_params(params)
    bs = kbtn.send_request()
    data_dic = {}
    tbody = bs.find_all('table')[3].tbody
    tr = tbody.find_all('tr')
    finance = DynamoDB.finance.Finance()
    finance.initialize()
    for index in range(1, (len(tr)) - 2):
        Y_M = re.search(r'([0-9]+).([0-9]+)', tr[index].th.text)
        settlement = data_dic['closing_period'] = Y_M.group(0).replace('.', '')
        finance_info = finance.query(stock_code, settlement)

        td_tags = tr[index].find_all('td')

        amo_salse = check_value_convert(td_tags[0].text)
        if amo_salse == None: continue

        ope_profit = check_value_convert(td_tags[1].text)
        if ope_profit == None: continue

        ord_profit = check_value_convert(td_tags[2].text)
        if ord_profit == None: continue

        net_profit = check_value_convert(td_tags[3].text)
        if net_profit == None: continue

        share_profit = check_value_convert(td_tags[4].text)
        if share_profit == None: continue

        sto_distribution = check_value_convert(td_tags[5].text)
        if sto_distribution == None: continue

        if int(finance_info['Count']) < 1:
            response = finance.insert(stock_code,settlement,amo_salse,ope_profit,ord_profit,net_profit,share_profit,sto_distribution)
            if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                exit(1)
        else:
            db_finance = DBDataConv.conv_finance.Conv_Finance().DBData_to_List(finance_info)[0]
            if (db_finance[2] != float(ope_profit) or db_finance[3] != float(share_profit) or \
                db_finance[4] != float(ord_profit) or db_finance[5] != float(amo_salse) or \
                db_finance[6] != float(net_profit)):

                print ('Finance Update stock_code:{} settlement:{}'.format(stock_code,settlement))

                items = {':ope_profit':{'N': str(float(ope_profit))},
                         ':share_profit': {'N': str(float(share_profit))},
                         ':ord_profit': {'N': str(float(ord_profit))},
                         ':amo_salse': {'N': str(float(amo_salse))},
                         ':net_profit': {'N': str(float(net_profit))},
                        }

                response = finance.update(stock_code,settlement,items)
                if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                    exit(1)


def kabuka_page_html_source(page_url,stock_code):

    for page in range(1,2):
        kbtn = web_access_method_factory(page_url)
        params = {'code': stock_code, 'ashi': 'day', 'page':page}
        kbtn.set_params(params)
        bs = kbtn.send_request()
        table_tags = bs.find_all('table',{'class':'stock_kabuka1'})
        tr_tags = table_tags[0].find_all('tr')
        stock = DynamoDB.stock.Stock()
        stock.initialize()
        for index in range(1,len(tr_tags)-1):
            date = '20' + tr_tags[index].th.text
            date = date.replace('/', '')
            if int(stock.query(stock_code, date)['Count']) < 1:
                td_tags = tr_tags[index].find_all('td')
                ope_price = convert_decimal(td_tags[0].text)
                high_price = convert_decimal(td_tags[1].text)
                low_price = convert_decimal(td_tags[2].text)
                clo_price = convert_decimal(td_tags[3].text)
                response = stock.insert(stock_code,date,ope_price,high_price,low_price,clo_price)
                if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                    exit(1)



def csvfile():
    with open('../CSV_File/USD_JPY 過去データ.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(spamreader)
        print(header)
        usdjpy = DynamoDB.usdjpy.USDJPY()
        usdjpy.initialize()
        for row in spamreader:
            cal_day = dt.strptime(row[0], '%Y年%m月%d日').strftime('%Y%m%d')
            ope_price = convert_decimal(row[2])
            high_price = convert_decimal(row[3])
            low_price = convert_decimal(row[4])
            clo_price = convert_decimal(row[1])

            response = usdjpy.insert(cal_day,ope_price,high_price,low_price,clo_price)
            if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                exit(1)

def ni225_page_html_source(page_url):
    kbtn = web_access_method_factory(page_url)
    kbtn.create_headers()
    bs = kbtn.send_request()
    table_tags = bs.find_all('table', {'id': 'curr_table'})
    tr_tags = table_tags[0].find_all('tr')
    ni225 = DynamoDB.ni225.Ni225()
    ni225.initialize()
    for index in range(1, (len(tr_tags))):
        td_tags = tr_tags[index].find_all('td')
        cal_day = dt.strptime(td_tags[0].text, '%Y年%m月%d日').strftime('%Y%m%d')
        if int(ni225.query(cal_day)['Count']) < 1:
            clo_price = convert_decimal(td_tags[1].text)
            ope_price = convert_decimal(td_tags[2].text)
            high_price = convert_decimal(td_tags[3].text)
            low_price = convert_decimal(td_tags[4].text)

            response = ni225.insert(cal_day, ope_price, high_price, low_price, clo_price)
            if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                exit(1)

def usdjpy_page_html_source(page_url):
    kbtn = web_access_method_factory(page_url)
    kbtn.create_headers()
    bs = kbtn.send_request()
    table_tags = bs.find_all('table', {'id': 'curr_table'})
    tr_tags = table_tags[0].find_all('tr')
    usdjpy = DynamoDB.usdjpy.USDJPY()
    usdjpy.initialize()
    for index in range(1, (len(tr_tags))):
        td_tags = tr_tags[index].find_all('td')
        cal_day = dt.strptime(td_tags[0].text, '%Y年%m月%d日').strftime('%Y%m%d')
        if int(usdjpy.query(cal_day)['Count']) < 1:
            clo_price = convert_decimal(td_tags[1].text)
            ope_price = convert_decimal(td_tags[2].text)
            high_price = convert_decimal(td_tags[3].text)
            low_price = convert_decimal(td_tags[4].text)

            response = usdjpy.insert(cal_day, ope_price, high_price, low_price, clo_price)
            if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                exit(1)

page_type = {'finance':1, 'kabuka':2, 'ni225':3,'usd_jpy':4}
page_list=['https://kabutan.jp/stock/finance',\
           'https://kabutan.jp/stock/kabuka',\
           'https://jp.investing.com/indices/japan-ni225-historical-data',\
           'https://jp.investing.com/currencies/usd-jpy-historical-data'
           ]
param_list=['3543','3048','9437','8591']

for page,type in zip(page_list,range(1,len(page_list) + 1)):
    for param in param_list:
        if type == page_type['finance']:
            finance_page_html_source(page,param)
        elif type == page_type['kabuka']:
            kabuka_page_html_source(page,param)
        elif type == page_type['ni225']:
            ni225_page_html_source(page)
            break
        elif type == page_type['usd_jpy']:
            usdjpy_page_html_source(page)
            break
