import csv
import re
from prettytable import PrettyTable

table = PrettyTable(
    hrules=True,
    align="l",
)
trash = { '<.*?>' : '', '\s+': ' ' }
translation = {
    'name' : 'Название',
    'description' : 'Описание',
    'key_skills' : 'Навыки',
    'experience_id' : 'Опыт работы',
    'premium' : 'Премиум-вакансия',
    'employer_name' : 'Компания',
    'salary_from' : 'Оклад',
    'area_name' : 'Название региона',
    'published_at' : 'Дата публикации вакансии'
}
format_dict = {
    'False' : 'Нет',
    'True' : 'Да',
    "noExperience" : "Нет опыта",
    "between1And3" : "От 1 года до 3 лет",
    "between3And6" : "От 3 до 6 лет",
    "moreThan6" : "Более 6 лет",
    "AZN" : "Манаты",
    "BYR" : "Белорусские рубли",
    "EUR" : "Евро",
    "GEL" : "Грузинский лари",
    "KGS" : "Киргизский сом",
    "KZT" : "Тенге",
    "RUR" : "Рубли",
    "UAH" : "Гривны",
    "USD" : "Доллары",
    "UZS" : "Узбекский сум"
}
no_pass = ['salary_to', 'salary_gross', 'salary_currency']

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
        if item in format_dict:
            sub[index] = format_dict[item]
        if index == 2:
            sub[index] = sub[index].replace(', ', '\n')
    return sub

def format_money(cash):
    cash = int(cash.replace('.0', ''))
    return f'{format(cash, ",d").replace(",", " ")}'

def format_value(diction):
    if diction['salary_gross'] == "Да":
        taxes = "Без вычета налогов"
    elif diction['salary_gross'] == "Нет":
        taxes = "С вычетом налогов"
    return f'{format_money(diction["salary_from"])} - {format_money(diction["salary_to"])}' \
           f' ({diction["salary_currency"]}) ({taxes})'

def extract_date(date):
    y_m_d = date.split('T')
    d_m_y = y_m_d[0].split('-')
    return f'{d_m_y[2]}.{d_m_y[1]}.{d_m_y[0]}'

def make_vacancies(keys, values):
    new_values = []
    for element in values:
        element = [i[:100] + '...' if len(i) > 100 else i for i in formatter(element)]
        new_jobs = {}
        jobs = dict(zip(keys, element))
        for key, value in jobs.items():
            if key[:6] == 'salary':
                if key in no_pass:
                    continue
                value = format_value(jobs)
            if key == "published_at":
                value = extract_date(value)
            new_jobs[key] = value
        new_values.append(new_jobs.values())
    return new_values

vacancies = open('vacancies_big.csv', encoding='utf-8-sig')
csv_file = csv.reader(vacancies, delimiter=",")
try:
    collums = next(csv_file)
except StopIteration:
    print("Пустой файл")
    exit()

info = [line for line in csv_file if len(line) == len(collums) and line.count("") == 0]
info = clear_array(info)
if len(info) == 0:
    print('Нет данных')
else:
    t_collums = [translation[i] for i in collums if i not in no_pass]
    for name in t_collums:
        table.max_width[name] = 20
    t_info = make_vacancies(collums, info)
    table.field_names = t_collums
    table.add_rows(t_info)
    table.add_autoindex('№')

    print(table)

# print("Пустой файл")
# print("Нет данных")