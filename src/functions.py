import json

from src.vacancy import Vacancy
from src.vacancy_manager import VacancyManager
from src.api import HeadHunterAPI, SuperJobAPI
import os

secret_key = os.getenv('SUPER_JOB_API_KEY')


def filter_vacancies(vacancies, filter_words):
    """Фильтрует вакансии по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered_vacancies = []
    for vacancy in vacancies:
        vacancy_info = f"{vacancy.title} {vacancy.description}"
        if any(word.lower() in vacancy_info.lower() for word in filter_words):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_vacancies(vacancies):
    """Сортирует вакансии по зарплата по убыванию"""
    return sorted(vacancies, key=lambda v: (v.salary['min'] or 0, v.salary['max'] or 0), reverse=True)


def get_top_vacancies(vacancies, n):
    """Возвращает необходимое количество вакансий сверху"""
    return vacancies[:n]


def print_vacancies(vacancies):
    """Печатает информацию о вакансиях в консоль"""
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")


def user_interaction():
    """Получает информацию от пользователя, выдает нужную информацию с учетом запроса пользователя"""
# Создаем экземпляры классов для работы с API
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI(secret_key)
    vacancy_manager = VacancyManager('vacancies.json')

# Получаем информацию от пользователя
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

# Получаем список вакансий с сайтов
    hh_vacancies = hh_api.get_vacancies(search_query)
    superjob_vacancies = superjob_api.get_vacancies(search_query)

# Формируем экземпляры классов с учетом запрошенной информации от пользователя
    for vac_data in hh_vacancies:
        vacancy = Vacancy.from_dict(vac_data, 'hh')
        vacancy_manager.add_vacancy(vacancy)
    for vac_data in superjob_vacancies:
        vacancy = Vacancy.from_dict(vac_data, 'sj')
        vacancy_manager.add_vacancy(vacancy)

# Выдаем информацию об отсутствии вакансий
    if not vacancy_manager.get_vacancies():
        print("Нет вакансий, соответствующих заданным критериям.")
        return

# Фильтруем вакансии по ключевым словам введеными пользователем
    filtered_vacancies = filter_vacancies(vacancy_manager.get_vacancies(), filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответсвующих заданным критериям.")
        return

# Сортируем вакансии и получаем необходимое количество вакансий сверху списка
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

# Выводим информацию в консоль
    print_vacancies(top_vacancies)

