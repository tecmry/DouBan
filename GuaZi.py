from bs4 import BeautifulSoup
import requests
def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1'
                      '+1_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data
def soup_html(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)
    Car_list = soup.find('ul', attrs={'class': 'carlist clearfix js-top'})
    Car_name_list = []
    Car_price_list = []
    Car_time_list = []
    Car_local_list = []
    # for li in Car_list.find_all('li'):
    #     try:
    #         name = li.find('div', attrs={'class': 't'}).getText()
    #         print(name)
    #         Car_name_list.append(name)
    #     except AttributeError:
    #         print('Null')
def start():
    urls = ['https://www.guazi.com/www/buy/o{}/#bread'.format(str(i)) for i in range(0, 20, 1)]
    for url in urls:
        html = download_page(url)
        soup_html(html)
if __name__ == '__main__':
    start()