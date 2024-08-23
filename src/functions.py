import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц: employers, vacancies
    :param database_name: название создаваемой базы
    :param params: Настройки базы данных
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')
    conn.commit()
    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(''' 
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                employer_url text
                );
            ''')
    conn.commit()
    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR(255) NOT NULL,
                requirement VARCHAR(255),
                salary_from INT,
                salary_to INT,
                currency VARCHAR(50),
                vacancy_url text
                );
            ''')

    conn.commit()
    conn.close()


def save_data_in_database(database_name: str, employers: list[dict], vacancies: list[dict], params: dict) -> None:
    """
    Добавление информации в базу данных
    :param database_name: название базы
    :param employers: данные о компаниях
    :param vacancies: данные о вакансиях
    :param params: словарь с параметрами базы данных

    """
    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            for employer in employers:
                employer_id = employer['employer_id']
                employer_name = employer['employer_name']
                employer_url = employer.get('alternate_url', 'Нет информации')
                cur.execute("""
                    INSERT INTO employers (employer_id, employer_name, employer_url)
                    VALUES (%s, %s, %s)
                """, (employer_id, employer_name, employer_url))

            for vacancy in vacancies:
                currency = 'Нет информации'
                salary_from = 0
                salary_to = 0
                if vacancy.get('salary'):
                    if vacancy.get('salary').get('currency'):
                        currency = vacancy.get('salary').get('currency')
                    if vacancy.get('salary').get('from'):
                        salary_from = vacancy.get('salary').get('from')
                    if vacancy.get('salary').get('to'):
                        salary_to = vacancy.get('salary').get('to')

                vacancy_id = vacancy['id']
                employer_id = vacancy['employer']['id']
                vacancy_name = vacancy['name']
                requirement = vacancy['snippet'].get('requirement', 'Нет информации')
                vacancy_url = vacancy.get('alternate_url')
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, requirement,
                    salary_from, salary_to, currency, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (vacancy_id, employer_id, vacancy_name, requirement, salary_from,
                      salary_to, currency, vacancy_url))
    conn.commit()
    conn.close()
