import requests
from lxml import html
from time import sleep
from random import randint
from parse_info import handle_link
from pymongo import MongoClient
from pymongo.errors import *

# from mongoDB_functions import check_and_create

client = MongoClient("localhost", 27017)
url = "https://news.mail.ru"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/98.0.4758.102 Safari/537.36"}

response = requests.get(url, headers=headers)
if response.ok:
    dom = html.fromstring(response.text)
    dom.make_links_absolute(url)
    news_links = dom.xpath("//a[@class='link link_flex']//@href")
    news_info = list()
    for new_link in news_links:
        sleep(randint(1, 5))
        new = handle_link(new_link, headers)
        db = client["news"]
        id_field = hash(new.get("new_title"))
        if db.general_news.find_one({"_id": id_field}) is None:
            db.general_news.insert_one({
                "_id": id_field,
                "title": new.get("new_title"),
                "reference": new.get("new_reference"),
                "publication_datetime": new.get("new_publication_datetime"),
                "link": new.get("new_link")
            })
