#coding:utf-8
import unittest
from functools import reduce

from selenium import webdriver
from bs4 import BeautifulSoup
import pymongo

def setStart():
    driver = webdriver.PhantomJS('D:\\phantomjs-2.1.1\\bin\\phantomjs.exe')
    driver.get('http://www.douyu.com/directory/all')
    soup = BeautifulSoup(driver.page_source, 'xml')
    while True:
        show_data = soup.find('div', attrs={'class': 'items items01 item-data clearfix'})
        showpeople_list = []
        showpeoplename_list = []
        viewpeoplecount_list = []
        if driver.page_source.find('shark-pager-disable-next') != -1:
            break
        elem = driver.find_element_by_class_name('shark-pager-next')
        elem.click()
        for newPeople in show_data.find_all('li'):
            try:
                showname = newPeople.find('a', attrs={'class': 'play-list-link'}).get('title')
                showpeoplename = newPeople.find('span', attrs={'class': 'dy-name ellipsis fl'}).getText()
                viewpeoplecount_index = newPeople.find('span', attrs={'class': 'dy-num fr'}).getText()
                viewpeoplecount = split_str(viewpeoplecount_index)
                showpeople_list.append(showname)
                showpeoplename_list.append(showpeoplename)
                viewpeoplecount_list.append(viewpeoplecount)
            except AttributeError:
                print('Null')
        save_data(showpeople_list, showpeoplename_list, viewpeoplecount_list)
        if driver.page_source.find('shark-pager-disable-next') != -1:
            break
        elem = driver.find_element_by_class_name('shark-pager-next')
        elem.click()
        soup = BeautifulSoup(driver.page_source, 'xml')


def split_str(strs):
    c = int(strs.__len__())
    a = int(c-1)
    try:
       if strs.find('.') != -1:
           if strs[-1] == '万':
               return str2float(strs[0:a]) * 10000
       else:
           if strs[-1] == '万':
               return float(int(strs[0:a]) * 10000)
           else:
               if strs != '0' and strs != '':
                   return float(int(strs[0:a]))
               else:
                   return float(0)
    except ValueError:
        pass








def save_data(showname_list, showpeople_list, viewpeople_list):
    dict_list = []
    for i in range(0, showname_list.__len__()):
        list1 = ['ShowName', 'UserName', 'ViewCount']
        list2 = [showname_list[i], showpeople_list[i], viewpeople_list[i]]
        dict_iindex = dict(zip(list1, list2))
        dict_list.append(dict_iindex)
    client = pymongo.MongoClient('localhost', 27017)
    db_name = 'DouYu'
    db = client[db_name]
    collection = db['Show_Info']
    try:
        list_after = delete_similar(dict_list)
        collection.insert(list_after)
    except pymongo.errors.DuplicateKeyError:
        print('DuplicateKey')
    except Exception as e:
        print('e')
def delete_similar(list):
    list_afrter = []
    for i in list:
        if i not in list_afrter:
            list_afrter.append(i)
    return list_afrter
def str2float(s):
    lt = list(s)
    y = lt.__len__()
    fup = lt.index('.')
    v = y-fup-1
    lt.pop(fup)
    def a2int(x,y):
       return x*10+y
    def char2int(lt):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[lt]
    return (reduce(a2int, map(char2int, lt)))/(10**v)

if __name__ == '__main__':
    setStart()


