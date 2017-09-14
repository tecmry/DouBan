import codecs

import requests
import pymongo
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250/'

# client = MongoClient('localhost', '27017')
# db_name = 'douban_movie'
# db = client[db_name]
# first = db['movie_common']

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content

    return data

def soup_html(html):
    soup = BeautifulSoup(html, 'lxml')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    movie_common_list = []
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        try:
            moviename = movie_li.find('span', attrs={'class': 'title'}).getText()
            commond = movie_li.find('span', attrs={'class': 'inq'}).getText()
        except AttributeError:
            print('Null')
        movie_name_list.append(moviename)
        movie_common_list.append(commond)
    nextPage = soup.find('span', attrs={'class': 'next'}).find('a')
    if nextPage:
        return movie_name_list, movie_common_list, DOWNLOAD_URL + nextPage['href']
    return movie_name_list, movie_common_list , None

def common_html(html):
    soup = BeautifulSoup(html, 'lxml')
    common_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    common_list = []
    for common_li in common_list_soup.find_all('li'):
        detail = common_li.find('div', attrs={'class': 'hd'})
        try:
            commond = common_li.find('span', attrs={'class': 'inq'}).getText()
        except AttributeError:
            print('Null')
        common_list.append(commond)
    nextPage = soup.find('span', attrs={'class': 'next'}).find('a')
    if nextPage:
        return common_list, DOWNLOAD_URL + nextPage['href']
    return common_list, None



def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, common, url = soup_html(html)
            data_list = add_dict(movies, common)
            save_data(data_list)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))

def save_data(dict_list):
    client = pymongo.MongoClient('localhost', 27017)
    db_name = 'douban_movie'
    db = client[db_name]
    collection_set01 = db['movie_common']
    try:
       collection_set01.insert(dict_list)
    except pymongo.errors.DuplicateKeyError:
        print('DuplicateKey')
    except Exception as e:
        print('e')
def add_dict(movie_list, common_list):
    dict_list = []
    for i in range(0, movie_list.__len__()):
        list1 = ['Name', 'Common']
        list2 = [movie_list[i], common_list[i]]
        dicti = dict(zip(list1, list2))
        dict_list.append(dicti)
    return dict_list
if __name__ == '__main__':
    main()