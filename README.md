## Курсовая работа №5: Проект по БД

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)

#### Технологии:

- python 3.12
- pip 24.0
- psycopg2

#### Инструкция для развертывания проекта:

Клонирование проекта:
```
git clone https://github.com/Efim-K/Course-4.git
```

Для запуска проекта необходимо создать виртуальное окружение venv:

1.Запустить и активировать виртуальное окружение

*для Windows:*
```
python -m venv venv
venv\Scripts\activate
```

*для Linux, macOS:*
```
python3 -m venv venv
source ./venv/bin/activate
```

2.Установить библиотеки
```
pip install -r requirements.txt
```

### Условие задания
В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

####  Основные шаги проекта
```
Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку 
requests

Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используйте библиотеку psycopg2

Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
Создать класс *DBManager* для работы с данными в БД спользуя библиотеку psycopg2, который будет подключаться к БД PostgreSQL и иметь следующие методы:
get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
get_avg_salary() — получает среднюю зарплату по вакансиям.
get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
```

Автор проекта Ефим Кашапов