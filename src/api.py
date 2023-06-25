import requests
from abc import ABC, abstractmethod


class AbstractJobAPI(ABC):
    """Абстрактный класс для обработки информации с API"""
    def __init__(self, base_url):
        """Инициализация класса"""
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_term):
        """Абстрактный метод для получения вакансий"""
        pass


class HeadHunterAPI(AbstractJobAPI):
    """Класс для получения информации с сайта hh.ru"""
    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")

    def get_vacancies(self, search_term):
        """Получает вакансии с сайта hh.ru"""
        items = []
        # Получение информации с 5 страниц по 10 результатов на странице
        for i in range(5):
            response = requests.get(self.base_url,
                                    params={'text': search_term, 'per_page': 10, 'page': i, 'only_with_salary': True})
            if response.status_code == 200:
                vacancies = response.json().get('items', [])
                # Получение вакансий только с валютой равной Рублю
                for vacancy in vacancies:
                    if vacancy.get('salary').get('currency') == "RUR":
                        items.append(vacancy)
            else:
                break
        return items


class SuperJobAPI(AbstractJobAPI):
    """Класс для получения информации с сайта superjob.ru"""
    def __init__(self, secret_key):
        super().__init__("https://api.superjob.ru/2.0/vacancies/")
        self.headers = {'X-Api-App-Id': secret_key}

    def get_vacancies(self, search_term):
        """Получает вакансии с сайта superjob.ru"""
        items = []
        seen_vacancies = set()
# Получение информации с 5 страниц по 10 результатов на странице
        for i in range(5):
            response = requests.get(self.base_url,
                                    headers=self.headers,
                                    params={'keyword': search_term, 'no_agreement': 1, 'count': 10, 'page': i})
            if response.status_code == 200:
                vacancies = response.json().get('objects', [])
                # Получение вакансий только с валютой равной Рублю
                for vacancy in vacancies:
                    if vacancy['profession'] not in seen_vacancies and vacancy['currency'] == "rub":
                        items.append(vacancy)
                        seen_vacancies.add(vacancy['profession'])
            else:
                break
        return items
