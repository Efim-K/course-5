import requests
from requests import JSONDecodeError
from src.exeptions import HeadHunterAPIException


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter и получения данных по компаниям и вакансиям
    """

    def __init__(self, list_id: list) -> None:
        self.__list_id = list_id

    def __get_employer(self, pk: int) -> dict:
        """
        Получение названия компании
        """
        url = f'https://api.hh.ru/employers/{pk}/'
        params = {'per_page': 10, 'sort_by': 'by_vacancies_open'}
        response = requests.get(url, params=params)
        is_allowed = self.__check_status(response)
        if not is_allowed:
            raise HeadHunterAPIException(f'Ошибка заброса данных:{response.status_code}, {response.text} ')
        try:
            response = requests.get(url, params=params)
            employer = response.json()
        except JSONDecodeError:
            raise HeadHunterAPIException(f'Ошибка получения данных JSON: {response.text}')
        return {
            'employer_id': employer['id'],
            'employer_name': employer['name'],
            'alternate_url': employer['alternate_url']
        }

    def __load_vacancies(self, pk: str) -> list[dict]:
        """
        Получение списка вакансий в формате json по id компании
        """
        url = 'https://api.hh.ru/vacancies/'
        params = {'per_page': 20, 'employer_id': pk}
        response = requests.get(url, params=params)
        is_allowed = self.__check_status(response)
        if not is_allowed:
            raise HeadHunterAPIException(f'Ошибка заброса данных:{response.status_code}, {response.text} ')
        try:
            response = requests.get(url, params=params)
            vacancies = response.json()['items']
        except JSONDecodeError:
            raise HeadHunterAPIException(f'Ошибка получения данных JSON: {response.text}')
        return vacancies

    @staticmethod
    def __check_status(response) -> bool:
        """"
        Проверка статуса запроса url
        """
        return response.status_code == 200

    def get_employers_list(self):
        """
        Получаем список компаний
        """
        employers_list = []
        for pk in self.__list_id:
            employers_list.append(self.__get_employer(pk))
        return employers_list

    def get_vacancies_list(self):
        """
        Получаем данные о вакансиях компаний
        """
        employers_list = self.get_employers_list()
        vacancies_list = []
        for employer in employers_list:
            vacancies_list.extend(self.__load_vacancies(employer['employer_id']))
        return vacancies_list
