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
                            SELECT employer_name AS "Компания", COUNT(*) AS "Кол-во вакансий" FROM employers
                            JOIN vacancies USING(employer_id)
                            GROUP BY employer_name
                            """)
                rows = cur.fetchall()
                # в первом элементе хранится имя колонки
                column_names = [d[0] for d in cur.description]
                for row in rows:
                    row_dict = {column_names[index]: value for (index, value) in enumerate(row)}
                    print(row_dict)
        conn.close()

    def get_all_vacancies(self):
        """
        Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT vacancy_name AS "Вакансия", employer_name AS "Компания",
                            salary_from AS "Зарплата от", salary_to AS "Зарплата до", currency AS "Валюта",
                            vacancy_url AS "Ссылка" 
                            FROM vacancies
                            JOIN employers USING(employer_id)
                            """)
                rows = cur.fetchall()
                # в первом элементе хранится имя колонки
                column_names = [d[0] for d in cur.description]
                for row in rows:
                    row_dict = {column_names[index]: value for (index, value) in enumerate(row)}
                    print(row_dict)
        conn.close()

    def get_avg_salary(self):
        """
        Получение средней зарплаты по вакансиям
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT ROUND(AVG((salary_from + salary_to) / 2)) AS "Средняя зарплата"
                    FROM vacancies
                """)

                rows = cur.fetchall()
                # в первом элементе хранится имя колонки
                column_names = [d[0] for d in cur.description]
                for row in rows:
                    row_dict = {column_names[index]: value for (index, value) in enumerate(row)}
                    print(row_dict)
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM vacancies AS "Вакансия"
                    WHERE (salary_to + salary_from) > 
                    (SELECT AVG(salary_from + salary_to) FROM vacancies);
                """)
                rows = cur.fetchall()
                # в первом элементе хранится имя колонки
                column_names = [d[0] for d in cur.description]
                for row in rows:
                    row_dict = {column_names[index]: value for (index, value) in enumerate(row)}
                    print(row_dict)
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                        SELECT * FROM vacancies  AS "Вакансия"
                        WHERE vacancy_name LIKE '%{keyword}%'
                        """)
                rows = cur.fetchall()
                # в первом элементе хранится имя колонки
                column_names = [d[0] for d in cur.description]
                for row in rows:
                    row_dict = {column_names[index]: value for (index, value) in enumerate(row)}
                    print(row_dict)
        conn.close()
