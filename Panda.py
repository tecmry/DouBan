import requests
import json
import pymongo
from bs4 import BeautifulSoup
from selenium import webdriver

def sava_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    client = pymongo.MongoClient('localhost', 27017)
    db_name = 'Panda'
    db = client[db_name]
    collection = db['Panda_Show']
    web_data = requests.get(url, headers=headers)
    data = json.loads(web_data.text)
    data_index = data['data']
    items = data_index['items']
    showname_list = []
    showtype_list = []
    showusername_list = []
    for item_index in items:
        show_name = item_index['name']
        classification_dict = item_index['classification']
        userinfo_dict = item_index['userinfo']
        show_type = classification_dict['cname']
        show_username = userinfo_dict['nickName']
        showname_list.append(show_name)
        showtype_list.append(show_type)
        showusername_list.append(show_username)
    lista = add_list(showname_list, showtype_list, showusername_list)
    try:
       collection.insert(lista)
    except pymongo.errors.DuplicateKeyError:
        print('DuplicateKey')
    except Exception as e:
        print('e')
def add_list(showname_list, showtype_list, showusername_list):
    dict_list = []
    for i in range(showusername_list.__len__()):
        list1 = ['ShowName', 'ShowType', 'ShowUserName']
        list2 = [showname_list[i], showtype_list[i], showusername_list[i]]
        dict1 = dict(zip(list1,list2))
        dict_list.append(dict1)
    return dict_list
def get_Count():
    driver = webdriver.PhantomJS('D:\\phantomjs-2.1.1\\bin\\phantomjs.exe')
    driver.get('https://www.panda.tv/all')
    soup = BeautifulSoup(driver.page_source, 'xml')
    counts = soup.find('div', attrs={'class': 'page-component'})
    href = counts.find_all('a', attrs = {'href': '#'})
    page_list = []
    for item in href:
        page_list.append(item.getText())
    i = page_list.__len__()
    get_Data(int(page_list[int(i)-3]))
def get_Data(count):
    urls = ['https://www.panda.tv/live_lists?status=2&order=person_num&token=&pageno={}&pagenum=120&_=1505741935610'
                . format(str(i)) for i in range(1, count)]
    for url in urls:
        sava_data(url)

if __name__ == '__main__':
    get_Count()

