from bs4 import BeautifulSoup
import requests
import re
import pymongo
url = 'https://gavbus123.com'
def download_page(index_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1'
                      '+1_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(index_url, headers=headers).content
    return data
def soup_html(html):
    soup = BeautifulSoup(html, 'lxml')
    movie_list = soup.find('div', attrs={'id': 'waterfall'})
    movie_name_list = []
    movie_link_list = []
    for item in movie_list.find_all('div'):
        try:
            movie_link_index = item.find('a', attrs = {'class': 'movie-box'})
            movie_name = item.find('div', attrs={'class': 'photo-frame'}).find('img')
            name = movie_name.get('title')
            movie_link = str(url) + str(movie_link_index.get('href'))
            movie_name_list.append(name)
            movie_link_list.append(movie_link)

        except AttributeError:
            print('Null Error')
    dict_list = set_dict(movie_name_list, movie_link_list)
    save_data(dict_list)
def set_dict(name_list, link_list):
    dict_list = []
    for i in range(name_list.__len__()):
        list1 = ['Name', 'Link']
        list2 = [name_list[i], link_list[i]]
        dicti = dict(zip(list1, list2))
        dict_list.append(dicti)
    return dict_list
def save_data(dict_list):
    client = pymongo.MongoClient('localhost', 27017)
    db_name = 'Yellow_Movie'
    db = client[db_name]
    collection_set01 = db['movie_info_1']
    try:
       collection_set01.insert(dict_list)
    except pymongo.errors.DuplicateKeyError:
        print('DuplicateKey')
    except Exception as e:
        print('e')
def start():
    urls = ['https://gavbus123.com/page/{}'.format(str(i))for i in range(1,50)]
    for url in urls:
        html = download_page(url)
        soup_html(html)
if __name__ == '__main__':
    start()