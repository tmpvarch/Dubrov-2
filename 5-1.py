import csv
import re
from var_dump import var_dump as vd_print


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name, published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class DataSet:
    def __init__(self, file_name, vacancies_objects):
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


trash = {'<.*?>': '', '\s+': ' '}

def clear_trash(string):
    clean_string = string
    for key, value in trash.items():
        clean_string = re.sub(key, value, clean_string.strip())
    return clean_string

def clear_n(string):
    return ', '.join(string.split("\n"))

def clear_fields(array):
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

def str_to_list(string):
    return string.split(', ')


def convert_to_classes(keys, values):
    full_list = []
    for element in values:
        dictionary = dict(zip(keys, element))
        salaries = Salary(dictionary["salary_from"], dictionary["salary_to"], dictionary["salary_gross"], dictionary["salary_currency"])
        vacancy_obj = Vacancy(dictionary["name"], dictionary["description"], str_to_list(dictionary["key_skills"]), dictionary["experience_id"],
                              dictionary["premium"], dictionary["employer_name"], salaries, dictionary["area_name"], dictionary["published_at"])
        full_list.append(vacancy_obj)
    return full_list


def get_inputs():
    set_file = input('Введите название файла: ')
    set_filter = input('Введите параметр фильтрации: ')
    set_sort = input('Введите параметр сортировки: ')
    set_order = input('Обратный порядок сортировки (Да / Нет): ')
    set_range = input('Введите диапазон вывода: ')
    set_columns = input('Введите требуемые столбцы: ')

    return set_file, set_filter, set_sort, set_order, set_range, set_columns


def make_titles(file):
    try:
        get_titles = next(file)
        return get_titles
    except StopIteration:
        print("Пустой файл")
        exit()


def main():
    file_name, filter_set, sort_by, order, output_range, columns = get_inputs()
    csv_file = csv.reader(open(file_name, encoding='utf-8-sig'), delimiter=",")
    titles = make_titles(csv_file)
    fields = clear_fields([l for l in csv_file if len(l) == len(titles) and l.count("") == 0])
    vacancies = convert_to_classes(titles, fields)

    vd_print(DataSet(file_name, vacancies))


if __name__ == "__main__":
    main()
