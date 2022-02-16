import json
import requests

'''The Article Search API is used to look up The New York Times articles by keywords'''
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

APIKEY = input("Введите ключ API: ")
category = "education"
filter = "discrimination"
params = {"q": category, "fq": filter, "api-key": APIKEY}

response = requests.get(url, params=params)
if response.ok:
    response_data = response.json()  # по умолчанию API возвращает только 10 статей, однако узел 'meta' в ответе
    # содержит их общее количество
    print(f"Количество найденных статей в газете The New York Times по теме '{category}', связанной с "
          f"'{filter}' = {response_data.get('response').get('meta').get('hits')}")

    with open('articles_result.json', 'w') as file:
        json.dump(response_data, file)
