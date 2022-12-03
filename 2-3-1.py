import csv
import re
from var_dump import var_dump as vd_print


class Salary:
    """Класс для представления зарплаты.

    Attributes:
        salary_from (int): Нижняя граница вилки оклада
        salary_to (int): Верхняя граница вилки оклада
        salary_gross (int): Оклад до вычета налогов
        salary_currency (int): Валюта оклада
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """Инициализирует объект Salary, выполняет конвертацию для целочисленных полей.

        Args:
            salary_from (str or int or float): Нижняя граница вилки оклада
            salary_to (str or int or float): Верхняя граница вилки оклада
            salary_gross (str or int or float): Оклад до вычета налогов
            salary_currency (str or int or float): Валюта оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class Vacancy:
    """Класс для представления вакансий

    Attributes:
        name (str): Название
        description (str): Описание
        key_skills (str): Навыки
        experience_id (str): Опыт работы
        premium (str): Премиум-вакансия
        employer_name (str): Компания
        salary (str): Оклад
        area_name (str): Название региона
        published_at (str): Дата и время публикации вакансии
    """
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name, published_at):
        """Инициализирует объект Salary, выполняет конвертацию для целочисленных полей.

        Args:
            name (str): Название
            description (str): Описание
            key_skills (str): Навыки
            experience_id (str): Опыт работы
            premium (str): Премиум-вакансия
            employer_name (str): Компания
            salary (str): Оклад
            area_name (str): Название региона
            published_at (str): Дата и время публикации вакансии
        """
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
    """Класс для представления набора данных

    Attributes:
        file_name (str): Название файла
        vacancies_objects (Vacancy): Данные вакансий

    """
    def __init__(self, file_name, vacancies_objects):
        """Инициализирует объект DataSet, выполняет конвертацию для целочисленных полей.

        Args:
            file_name (str): Название файла
            vacancies_objects (Vacancy): Данные вакансий
        """
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


trash = {'<.*?>': '', '\s+': ' '}

def clear_trash(string):
    """Функция для отчищения строк от html-тегов.


    Args:
         string (str): Строкач

    Функция возвращает данные типа str
    """
    clean_string = string
    for key, value in trash.items():
        clean_string = re.sub(key, value, clean_string.strip())
    return clean_string

def clear_n(string):
    """Функция для удаления \n из строк

    Args:
        string (str): Строка

    Функция возвращает данные типа str
    """
    return ', '.join(string.split("\n"))

def clear_fields(array):
    """Функция для удаления html-тегов и \n из строк, находящихся в списке.

    Args:
        array (list): Массив

    Функция возвращает данные типа list
    """
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
    """Функция для разделения строки на элементы списка.

    Args:
        string (str): Строка

    Функция возвращает данные типа list
    """
    return string.split(', ')


def convert_to_classes(keys, values):
    """Функция для распределения keys и values по классам Vacancy и Salary.

    Args:
        keys (list): в данный аргумент передаются заголовки столбиков
        values (list):  в этот аргумент передаётся информация по вакансиям

    Функция возвращает данные типа list
    """
    full_list = []
    for element in values:
        dictionary = dict(zip(keys, element))
        salaries = Salary(dictionary["salary_from"], dictionary["salary_to"], dictionary["salary_gross"], dictionary["salary_currency"])
        vacancy_obj = Vacancy(dictionary["name"], dictionary["description"], str_to_list(dictionary["key_skills"]), dictionary["experience_id"],
                              dictionary["premium"], dictionary["employer_name"], salaries, dictionary["area_name"], dictionary["published_at"])
        full_list.append(vacancy_obj)
    return full_list


def get_inputs():
    """Функция, которая принимает входные данные.

    При ее вызове к ней на вход не поступают никакие аргументы.

    Функция возвращает данные типа str
    """
    set_file = input('Введите название файла: ')
    set_filter = input('Введите параметр фильтрации: ')
    set_sort = input('Введите параметр сортировки: ')
    set_order = input('Обратный порядок сортировки (Да / Нет): ')
    set_range = input('Введите диапазон вывода: ')
    set_columns = input('Введите требуемые столбцы: ')

    return set_file, set_filter, set_sort, set_order, set_range, set_columns


def make_titles(file):
    """Функция для создания листа заголовок по следующей строчке csv-файла.

    Args:
        file (str): Название файла

    При вызове данной функции она попытается создать и вернуть заголовки стоблцов из csv-файла в виде
    данных типа list. Если на вход поступает пустой файл, то может выйти ошибка StopIteration, при ловле
    которой программа выдаёт, что на вход поступил пустой файл, после чего работа программы заканчивается.
    """
    try:
        get_titles = next(file)
        return get_titles
    except StopIteration:
        print("Пустой файл")
        exit()


def main():
    """Основная функция, которая будет вызвана при запуске программы.

    Данная функция ничего не принимает в качестве аргументов и ничего возвращает.
    """
    file_name, filter_set, sort_by, order, output_range, columns = get_inputs()
    csv_file = csv.reader(open(file_name, encoding='utf-8-sig'), delimiter=",")
    titles = make_titles(csv_file)
    fields = clear_fields([l for l in csv_file if len(l) == len(titles) and l.count("") == 0])
    vacancies = convert_to_classes(titles, fields)

    vd_print(DataSet(file_name, vacancies))


if __name__ == "__main__":
    main()
