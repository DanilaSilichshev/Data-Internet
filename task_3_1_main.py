import requests
from bs4 import BeautifulSoup as bs
import re
from pymongo import MongoClient
from pymongo.errors import *
from vacancies_from_page import get_vacancies_from_page
from mongoDB_functions import check_and_create
url = "https://hh.kz"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/98.0.4758.102 Safari/537.36"}

client = MongoClient("localhost", 27017)

def get_vacancies(area):
    params = {"area": area, "fromSearchLine": True,
              "text": input("Введите специализацию для поиска: ")}

    response = requests.get(url + "/search/vacancy", params=params, headers=headers)
    if response.ok:
        dom = bs(response.text, "html.parser")
        if dom.find(text=f"По запросу «{params.get('text')}» ничего не найдено") is None:
            vacancies_list = list()
            all_pages = dom.find_all("a", {"class": "bloko-button", "data-qa": "pager-page"})
            if len(all_pages) == 0:
                last_page = 1
            else:
                last_page_elem = all_pages[len(all_pages) - 1]
                last_page = int(last_page_elem.find("span").get_text())
            for page_num in range(last_page):
                vacancies_list = get_vacancies_from_page(page_num, url, headers, params.get('area'), params.get('text'))
                for vacancy in vacancies_list:
                    title = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"}).get_text()
                    link = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"}).get("href")
                    employer = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).get_text()
                    address = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).get_text()
                    try:
                        salary_info = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"}).get_text()
                        salary_info_copy = salary_info.split()
                        min_salary, max_salary, currency = None, None, None
                        if "–" in salary_info:
                            salary_info_copy_2 = salary_info.split("–")
                            min_salary = re.sub(r"[^0-9]", "", salary_info_copy_2[0])
                            max_salary = re.sub(r"[^0-9]", "", salary_info_copy_2[1])
                            currency = salary_info_copy[len(salary_info_copy) - 1]
                        elif "от" in salary_info:
                            min_salary = re.sub(r"[^0-9]", "", salary_info[2:])
                            currency = salary_info_copy[len(salary_info_copy) - 1]
                        elif "до" in salary_info:
                            max_salary = re.sub(r"[^0-9]", "", salary_info[2:])
                            currency = salary_info_copy[len(salary_info_copy) - 1]
                    except:
                        min_salary, max_salary, currency = None, None, None
                    vacancy_dict = {
                        "title": title,
                        "employer": employer,
                        "address": address,
                        "min_salary": min_salary,
                        "max_salary": max_salary,
                        "currency": currency,
                        "link": link
                    }
                    check_and_create(vacancy_dict, client, "vacancies")
        else:
            print(f"По запросу «{params.get('text')}» ничего не найдено")
            get_vacancies(area)


get_vacancies(40)  # area = 40 - поиск по Казахстану
