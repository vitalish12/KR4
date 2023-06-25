import re


class Vacancy:
    """Класс вакансии"""
    def __init__(self, title, url, salary, description, salary_currency):
        """Инициализация экземпляра"""
        self.title = self.validate_title(title)
        self.url = self.validate_url(url)
        self.salary = salary
        self.description = self.validate_description(description)
        self.salary_currency = self.validate_salary_currency(salary_currency)

    @classmethod
    def from_dict(cls, data, source):
        """Формирует экземпляры вакансий из словарей с сайтов hh.ru и superjob.ru"""
# Получаем информацию с hh.ru
        if source == 'hh':
            title = data.get('name')
            url = data.get('alternate_url')
            salary_data = data.get('salary')
            if salary_data:
                if salary_data.get('from') is None:
                    salary = {'min': 0, 'max': salary_data.get('to')}
                elif salary_data.get('to') is None:
                    salary = {'min': salary_data.get('from'), 'max': 0}
                else:
                    salary = {'min': salary_data.get('from'), 'max': salary_data.get('to')}
                salary_currency = salary_data.get('currency')
            else:
                salary = "Отсутствует"
                salary_currency = "Не указано"
            work = data['snippet'].get('requirement')
# Получаем информацию с superjob.ru
        elif source == 'sj':
            title = data.get('profession')
            url = data.get('link')
            salary = {'min': data.get('payment_from'), 'max': data.get('payment_to')}
            work = data.get('candidat').replace('\n', '/')
            salary_currency = data.get('currency')
        else:
            raise ValueError(f"Invalid source: {source}")
        return cls(title, url, salary, work, salary_currency)

    @staticmethod
    def validate_title(title):
        """Проверяет названия вакансии"""
        if not title:
            raise ValueError("Title cannot be empty.")
        return title

    @staticmethod
    def validate_url(url):
        """Проверяет ссылку вакансии"""
        if not url.startswith("http"):
            raise ValueError("URL is not valid.")
        return url

    @staticmethod
    def validate_salary(salary):
        """Проверяет правильность зарплаты"""
        if not salary:
            return None
        pattern = r"(\d+\D*(\d+)?"
        match = re.match(pattern, salary)
        if match:
            salary_dict = {}
            if match.group(1):
                salary_dict['min'] = int(match.group(1))
            if match.group(2):
                salary_dict['max'] = int(match.group(2))
            return salary_dict
        else:
            raise ValueError(f"Некорректный формат зарплаты: {salary}")

    @staticmethod
    def validate_description(description):
        """Проверяет описание вакансии"""
        if not description:
            return None
        else:
            return description

    @staticmethod
    def validate_salary_currency(salary_currency):
        """Проверяет валюту зарплаты"""
        if not salary_currency:
            return None
        elif len(salary_currency) > 3:
            raise ValueError("Неккоректный код валюты")
        else:
            return salary_currency

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary['min'] < other.salary['min']

    def __str__(self):
        return f"""Вакансия: {self.title}, 
Ссылка: {self.url}, 
Зарплата от: {self.salary['min']}  Зарплата до: {self.salary['max']}
Валюта: {self.salary_currency}, 
Описание: {self.description}
"""
