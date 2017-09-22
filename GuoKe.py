from bs4 import BeautifulSoup
import requests
import json
import pymongo
url = 'http://www.guokr.com/scientific/'
def sava_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    client = pymongo.MongoClient('localhost', 27017)
    db_name = 'GuoKe_Data'
    db = client[db_name]
    collection = db['Guoke_Science']
    web_data = requests.get(url, headers=headers)
    datas = json.loads(web_data.text)
    for data in datas['result']:
        collection.insert_one(data)
def start():
    urls = ['http://www.guokr.com/apis/minisite/article.json?retrieve_type=by_subject&limit=20&offset={}&_=1462252453410'
                .format(str(i)) for i in range(18, 98, 20)]
    for url in  urls:
        sava_data(url)
if __name__ == '__main__':
    start()