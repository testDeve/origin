from Web import HttpAccess as ha
import requests
from bs4 import BeautifulSoup

class KabutanAccess(ha.HttpAccess):

    def set_url(self, url):
        self.url = url
        self.params = None
        self.headers = None

    def set_params(self,params):
        self.params = params

    def reset_params(self):
        self.params = None

    def set_headers(self,headers):
        self.headers = headers

    def reset_headers(self,headers):
        self.headers = None

    def create_headers(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }

    def send_request(self):
        print(self.url,self.params,self.headers)
        if self.params != None and self.headers != None:
            html_source = requests.get(url=self.url, params=self.params, headers=self.headers)
        elif self.params == None and self.headers != None:
            html_source = requests.get(url=self.url, headers=self.headers)
        elif self.params != None and self.headers == None:
            html_source = requests.get(url=self.url, params=self.params)
        else:
            html_source = requests.get(url=self.url)

        html_text = html_source.text
        bs = BeautifulSoup(html_text, "html.parser")
        return bs

if __name__ == '__main__':
    kbtn = KabutanAccess()
    params = {'code': '3543', 'ashi': 'day', 'page': '1'}
    kbtn.set_url('https://kabutan.jp/stock/finance')
    kbtn.set_params(params)
    bs = kbtn.send_request()
    print(bs)