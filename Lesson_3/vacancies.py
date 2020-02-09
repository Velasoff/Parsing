from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests

def find_vacancies(name, page):

    main_link = 'https://hh.ru/'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    vacancies = []
    for i in range(page):
        response = requests.get(main_link + f'search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={name}&page={i}', headers=header).text
        html = bs(response, 'lxml')
        vacancies_block = html.find('div', {'class': 'vacancy-serp'})
        vacancies_list = vacancies_block.findChildren(recursive=False)
        for vacancy in vacancies_list:
            vacancy_data = {}
            main_info = vacancy.find('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
            if main_info is not None:
                salary = main_info.find('div', {'class': 'vacancy-serp-item__compensation'})
                if salary is None:
                    min_salary = 'None'
                    max_salary = 'None'
                else:
                    salary = salary.getText()[0:-5].replace("\xa0", '').replace('-', ' ')
                    if salary.find('от') == 0:
                        min_salary = int(salary[3:])
                        max_salary = 'None'
                    elif salary.find('до') == 0:
                        min_salary = 'None'
                        max_salary = int(salary[3:])
                    else:
                        min_salary, max_salary = [int(i) for i in salary.split(' ')]
                main_info = main_info.findChild()
                vacancy_name = main_info.getText()
                vacancy_text = main_info.getText
                vacancy_link = str(vacancy_text)[str(vacancy_text).find('http'):str(vacancy_text).find('target=')-2]
            else:
                continue
            vacancy_data['name'] = vacancy_name
            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = main_link
            vacancies.append(vacancy_data)

    main_link='https://www.superjob.ru/'
    for i in range(page):
        response = requests.get(main_link + f'vacancy/search/?keywords={name}&geo[c][0]=1&page={i}', headers=header).text
        html = bs(response, 'lxml')
        vacancies_block = html.findAll('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
        for vacancy in vacancies_block:
            vacancy_data = {}
            vacancy_name = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
            salary = vacancy.find('span', {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()
            if salary == 'По договорённости':
                min_salary = 'None'
                max_salary = 'None'
            else:
                salary = salary[0:-1].replace("\xa0", '').replace('—', ' ')
                if salary.find('от') == 0:
                    min_salary = int(salary[2:])
                    max_salary = 'None'
                elif salary.find('до') == 0:
                    min_salary = 'None'
                    max_salary = int(salary[2:])
                else:
                    min_salary, max_salary = [int(i) for i in salary.split(' ')]
            vacancy_text = vacancy.getText
            vacancy_link = main_link + str(vacancy_text)[str(vacancy_text).find('href="/vakansii')+7:str(vacancy_text).find('target=', str(vacancy_text).find('href="/vakansii')) - 2]

            vacancy_data['name'] = vacancy_name
            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = main_link
            vacancies.append(vacancy_data)
    return vacancies
