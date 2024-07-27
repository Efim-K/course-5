import psycopg2


class DB_Manager:
    """
    Класс для  для работы с БД
    """
    __slots__ = ('__db_name', '__params')

    def __init__(self, db_name, params: dict):
        self.__db_name = db_name
        self.__params = params

    def get_companies_and_vacancies_count(self):
        """
        Получение списка всех компаний и количество вакансий у каждой компании
        :return:
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT employer_name, COUNT(*) FROM employers
                            JOIN vacancies USING(employer_id)
                            GROUP BY employer_name
                            """)
                print(cur.fetchall())
        conn.close()

    def get_all_vacancies(self):
        """
        Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT vacancy_name, employer_name, salary_from, salary_to, currency, vacancy_url 
                            FROM vacancies
                            JOIN employers USING(employer_id)
                            """)
                print(cur.fetchall())
        conn.close()

    def get_avg_salary(self):
        """
        Получение средней зарплаты по вакансиям
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT ROUND(AVG((salary_from + salary_to) / 2)) AS avg_salary
                    FROM vacancies
                """)
                print(cur.fetchall()[0])
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM vacancies
                    WHERE (salary_to + salary_from) > 
                    (SELECT AVG(salary_from + salary_to) FROM vacancies);
                """)
                print(cur.fetchall())
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                        SELECT * FROM vacancies
                        WHERE vacancy_name LIKE '%{keyword}%'
                        """)
                print(cur.fetchall())
        conn.close()
