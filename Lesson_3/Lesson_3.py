from pymongo import MongoClient
from pprint import pprint
from vacancies import find_vacancies

client = MongoClient('localhost', 27017)
db = client['users_db_280']
users = db.users280

print('Введите название вакансии: ')
name = input()
name = name.replace(' ', '+')
print('Сколько страниц просматривать? ')
page = int(input())

vacancies = find_vacancies(name, page)

users.insert_many(vacancies)

print('Введите минимальную заработную плату: ')
salary = input()
selected_vacancies = users.find({'min_salary': {'$gt': 70000}})
for doc in selected_vacancies:
    pprint(doc)
