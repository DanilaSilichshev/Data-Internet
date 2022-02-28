def check_and_create(elem, client, db_title):
    db = client[db_title]
    vacancies = db.vacancies
    id_field = hash(elem.get("title") + elem.get("employer") + elem.get("address"))
    if vacancies.find_one({"_id": id_field}) is None:
        min_salary = None if elem.get("min_salary") is None else float(elem.get("min_salary"))
        max_salary = None if elem.get("max_salary") is None else float(elem.get("max_salary"))
        vacancies.insert_one({
            "_id": id_field,
            "title": elem.get("title"),
            "employer": elem.get("employer"),
            "address": elem.get("address"),
            "min_salary": min_salary,
            "max_salary": max_salary,
            "currency": elem.get("currency"),
            "link": elem.get("link")
        })


def select_greater(client, db_title):
    db = client[db_title]
    vacancies = db.vacancies
    return vacancies.find({"$or": [{"min_salary": {"$gt": float(input("Введите число для сравнения с минимальной "
                                                                      "зарплатой: "))}},
                                   {"max_salary": {"$gt": float(input("Введите число для сравнения с максимальной "
                                                                      "зарплатой: "))}}]})
