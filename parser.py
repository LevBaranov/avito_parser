import random
import requests

from bs4 import BeautifulSoup

class Parser():
    '''Наша рабочая лошадка'''

    def __init__(self, url):
        self.url = url

    def get_proxy():
        proxy = requests.get(
            'https://gimmeproxy.com/api/getProxy?country=RU&get=true&supportsHttps=true&protocol=http')
        proxy_json = json.loads(proxy.content)
        if proxy.status_code != 200 and 'ip' not in proxy_json:
            raise RequestException
        else:
            return proxy_json['ip'] + ':' + proxy_json['port']

    def get_html(self, proxy=None):
        USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv)',
            'Mozilla/5.0 (X11; Linux i686; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        ]
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        proxy_list = [get_proxy()]
        proxies = {
            'http': 'http://91.195.130.237:8080',
            'https': 'https://91.195.130.237:8080'
        }
        response = requests.get(self.url, headers=headers, proxies=proxies, timeout=20)

        self.html = BeautifulSoup(response.content, 'lxml')
        return self.html 
    
    def __repr__(self):
        return "Parser('%s')" % (self.url)

if __name__ == '__main__':
    url = 'https://www.avito.ru/kazan/igry_pristavki_i_programmy/igrovye_pristavki-ASgBAgICAUSSAsoJ?q=ps4+pro'
    parser = Parser(url)
    response = parser.get_html() #, headers=headers, proxies=proxies, timeout=Config.REQUEST_TIMEOUT)

    print(response)