from src.API_HH import HeadHunterAPI
from src.config import config
from src.dbmanager import DB_Manager
from src.functions import create_database, save_data_in_database


def main():
    # ID компаний
    list_id = [5354417, 876074, 1521497, 2291325, 1409231, 2268880, 4080, 2666179, 28275, 4217204]
    hh = HeadHunterAPI(list_id)
    # employers = hh.get_employers_list()
    # vacancies = hh.get_vacancies_list()

    params = config()
    db_name = 'coursework5'
    create_database(db_name, params)
    # save_data_in_database(db_name, employers, vacancies, params)

    # data_base = DB_Manager(db_name, params)
    # choice = input('1 - список всех компаний и кол-во вакансий у каждой компании\n'
    #                '2 - список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию\n'
    #                '3 - среднюю зарплату по вакансиям\n'
    #                '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
    #                '5 - список вакансий, в названии которых содержится ключевое слово\n')
    # if choice == '1':
    #     print(data_base.get_companies_and_vacancies_count())
    # elif choice == '2':
    #     print(data_base.get_all_vacancies())
    # elif choice == '3':
    #     print(data_base.get_avg_salary())
    # elif choice == '4':
    #     print(data_base.get_vacancies_with_higher_salary())
    # elif choice == '5':
    #     keyword = str(input('Введите слово для поиска в названии вакансии:\n'))
    #     print(data_base.get_vacancies_with_keyword(keyword))


if __name__ == '__main__':
    main()
