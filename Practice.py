import codecs
import os
import requests
import pymongo
from multiprocessing import Process
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250/'

# client = MongoClient('localhost', '27017')
# db_name = 'douban_movie'
# db = client[db_name]
# first = db['movie_common']

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1'
                      '+1_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content

    return data

def soup_html(html):
    soup = BeautifulSoup(html, 'lxml')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    movie_common_list = []
    movie_score_list = []
    movie_link_list = []
    movie_commonpeople_index = []
    movie_commonpeople_list = []
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'}).find('a')
        common_people = movie_li.find('div', attrs={'class': 'star'})
        for ssh in common_people.find_all('span'):
            movie_commonpeople_index.append(ssh.getText())
        try:
            movielink = detail['href']
            moviename = movie_li.find('span', attrs={'class': 'title'}).getText()
            commond = movie_li.find('span', attrs={'class': 'inq'}).getText()
            score = movie_li.find('span', attrs={'class': 'rating_num'}).getText()
        except AttributeError:
            print('Null')
        if movie_commonpeople_index.__len__() == 100:
            for i in range(0, 25):
                movie_commonpeople_list.append(int(split_str(movie_commonpeople_index[3 + 4 * i])))
        movie_name_list.append(moviename)
        movie_common_list.append(commond)
        movie_score_list.append(score)
        movie_link_list.append(movielink)
    nextPage = soup.find('span', attrs={'class': 'next'}).find('a')
    if nextPage:
        return movie_name_list, movie_common_list, movie_score_list, movie_link_list, movie_commonpeople_list, DOWNLOAD_URL + nextPage['href']
    return movie_name_list, movie_common_list, movie_score_list, movie_link_list, movie_commonpeople_list, None
def split_str(str):
    a = int(str.__len__())
    c = int(a-3)
    return str[0:c]
def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, common, score, link, common_people, url = soup_html(html)
            data_list = add_dict(movies, common, score, link, common_people)
            save_data(data_list)


def save_data(dict_list):
    client = pymongo.MongoClient('localhost', 27017)
    db_name = 'douban_movie_7'
    db = client[db_name]
    collection_set01 = db['movie_common']
    try:
       collection_set01.insert(dict_list)
    except pymongo.errors.DuplicateKeyError:
        print('DuplicateKey')
    except Exception as e:
        print('e')

def add_dict(movie_list, common_list, score_list, link_list,commonpeople_list):
    dict_list = []
    for i in range(0, movie_list.__len__()):
        list1 = ['Name', 'Common', 'Score', 'Link', 'CommonPeople']
        list2 = [movie_list[i], common_list[i], score_list[i], link_list[i], commonpeople_list[i]]
        dicti = dict(zip(list1, list2))
        dict_list.append(dicti)
    return dict_list
if __name__ == '__main__':
    main()