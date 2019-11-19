import requests
import time
from bs4 import BeautifulSoup
import re
from DynamoDB import Stock as Stock
from DynamoDB import Finance as Finance
import decimal

def convert_decimal(val,deli=','):
    return decimal.Decimal(val.replace(deli,''))

def check_value_convert(val):
    if val != '－':
        return convert_decimal(val)
    else:
        return None

def send_request(page_url,params=None,headers=None):

    if params != None and headers != None:
        html_source = requests.get(url=page_url, params=params, headers=headers)
    elif params == None and headers != None:
        html_source = requests.get(url=page_url, headers=headers)
    elif params != None and headers == None:
        html_source = requests.get(url=page_url, params=params)
    else:
        html_source = requests.get(url=page_url)

    html_text = html_source.text
    bs = BeautifulSoup(html_text, "html.parser")
    return bs

def finance_page_html_source(page_url,stock_code):
    params = {'code': stock_code}
    bs = send_request(page_url,params=params)
    data_dic = {}
    tbody = bs.find_all('table')[3].tbody
    tr = tbody.find_all('tr')
    finance = Finance.Finance()
    finance.initialize()
    for index in range(1, (len(tr)) - 2):
        Y_M = re.search(r'([0-9]+).([0-9]+)', tr[index].th.text)
        settlement = data_dic['closing_period'] = Y_M.group(0).replace('.', '-')
        if int(finance.query(stock_code, settlement)['Count']) < 1:
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

            response = finance.insert(stock_code,settlement,amo_salse,ope_profit,ord_profit,net_profit,share_profit,sto_distribution)
            if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                exit(1)

def kabuka_page_html_source(page_url,stock_code):

    for page in range(1,6):
        params = {'code': stock_code, 'ashi': 'day', 'page':page}
        bs = send_request(page_url,params=params)
        table_tags = bs.find_all('table',{'class':'stock_kabuka1'})
        tr_tags = table_tags[0].find_all('tr')
        stock = Stock.Stock()
        stock.initialize()
        for index in range(1,len(tr_tags)-1):
            date = '20' + tr_tags[index].th.text
            date = date.replace('/', '-')
            if int(stock.query(stock_code, date)['Count']) < 1:
                td_tags = tr_tags[index].find_all('td')
                ope_price = convert_decimal(td_tags[0].text)
                high_price = convert_decimal(td_tags[1].text)
                low_price = convert_decimal(td_tags[2].text)
                clo_price = convert_decimal(td_tags[3].text)
                response = stock.insert(stock_code,date,ope_price,high_price,low_price,clo_price)
                if int(response['ResponseMetadata']['HTTPStatusCode']) != 200:
                    exit(1)

def ni225_page_html_source(page_url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
    bs = send_request(page_url,headers=headers)
    print(bs)
    return None


page_type = {'finance':1, 'kabuka':2, 'ni225':3}
page_list=['https://kabutan.jp/stock/finance','https://kabutan.jp/stock/kabuka','https://jp.investing.com/indices/japan-ni225-historical-data']
param_list=['3543','3048','9437','8591']

for page,type in zip(page_list,range(1,len(page_list) + 1)):
    for param in param_list:
        if type == page_type['finance']:
            print('finance')
            #finance_page_html_source(page,param)
        elif type == page_type['kabuka']:
            print('kabuka')
            # kabuka_page_html_source(page,param)
        elif type == page_type['ni225']:
            ni225_page_html_source(page)
            break

