import csv
import re

trash = { '<.*?>' : '', '\s+': ' ' }
translation = {
    'name' : 'Название',
    'description' : 'Описание',
    'key_skills' : 'Навыки',
    'experience_id' : 'Опыт работы',
    'premium' : 'Премиум-вакансия',
    'employer_name' : 'Компания',
    'salary_from' : 'Нижняя граница вилки оклада',
    'salary_to' : 'Верхняя граница вилки оклада',
    'salary_gross' : 'Оклад указан до вычета налогов',
    'salary_currency' : 'Идентификатор валюты оклада',
    'area_name' : 'Название региона',
    'published_at' : 'Дата и время публикации вакансии',
    'False' : 'Нет',
    'True' : 'Да'
}

def clear_trash(string):
    clean_string = string
    for key, value in trash.items():
        clean_string = re.sub(key, value, clean_string.strip())
    return clean_string

def clear_n(string):
    return ', '.join(string.split("\n"))

def clear_array(array):
    cleared_array = []
    for sub_array in array:
        transport = []
        for string in sub_array:
            if '\n' in string:
                string = clear_n(string)
            string = clear_trash(string)
            transport.append(string)
        cleared_array.append(transport)
    return cleared_array

def formatter(sub):
    for index, item in enumerate(sub):
        if item in translation:
            sub[index] = translation[item]
    return sub

def print_vacancies(keys, values):
    for element in values:
        dictionary = dict(zip(keys, formatter(element)))
        for key, value in dictionary.items():
            print("{0}: {1}".format(key, value))
        print()


vacancies = open(input(), encoding='utf-8-sig')
csv_file = csv.reader(vacancies, delimiter=",")

collums = [translation[item] for item in next(csv_file)]
info = [line for line in csv_file if len(line) == len(collums) and line.count("") == 0]
info = clear_array(info)

print_vacancies(collums, info)