import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import randint


def get_vacancies_from_page(page, url, headers, area, text):
    params = {"area": area, "fromSearchLine": True, "hhtmFrom": "vacancy_search_list", "text": text, "page": page}

    response = requests.get(url + "/search/vacancy", params=params, headers=headers)
    sleep(randint(3, 10))
    if response.ok:
        dom = bs(response.text, "html.parser")
        vacancies_list = dom.find_all("div", {"class": "vacancy-serp-item vacancy-serp-item_redesigned"})
        return vacancies_list
