# ХАКАТОН+. Задача Альфа-Банка. Команда 11. Backend

## Оглавление <a id="contents"></a>

1. [О проекте](#about)
2.  [Авторы проекта](#authors)
3. [Архив с кодом репозитория и скриншотами](#archive)
4. [Документация](#documentation)
5. [Стек технологий](#tools)
6. [Установка зависимостей](#installation)
7. [Настройка](#setting)
8. [Запуск локально](#startlocal)
8. [Запуск в контейнере](#start)
9. [Наполнение БД](#database)
10. [Тесты и покрытие](#tests)
11. [Frontend](#frontend)


## О проекте <a id="about"></a>

MVP индивидуального плана развития для сотрудников в Альфа-Банке.

[https://yahackathon.ddns.net/](https://yahackathon.ddns.net/)

Мы создали продукт, который должен работать внутри приложения Alfa People. Поэтому явная авторизация в системе не предусмотрена. Однако, чтобы проверить работу системы, можно авторизоваться через headers.

Для работы на сайте под разными ролями вам потребуются токены, которые следует прописать в инструментах разработчика->Application->Local Storage,
ввести ключ для токена в поле "Имя"/”Key” и значение токена в поле "Значение"/”Value”:

  Key:
  ```
  AlfaIprProjectToken
  ```

  для просмотра в режиме ***Руководитель***:

  Value:
  ```
  Token 08c8b74340e79ea26fbb73a9cc398c79fd36d77c
  ```
  для просмотра в режиме ***Сотрудник***:

  Value:
  ```
  Token ac83a1374ee39b726829e34d49ce15138704b737
  ```

* нажать Enter или кликнуть где-то вне поля, чтобы сохранить введенные данные
* обновить страницу

## Авторы проекта <a id="authors"></a>

Команда:

- Product manager
  - Никитин Валентин

- Project manager
  - Кутицкий Владислав

- Business analytics
  - Щетинина Наталья
  - Михненко Елена

- System analytics
  - Богатков Павел
  - Бибикова Вера

- Designers
  - Викулов Юрий
  - Конева Татьяна
  - Перадзе Мария

- Frontend
  - [Александрова Светлана](https://github.com/SvetAlexa)
  - [Тихонова Ксения](https://github.com/TikhonovaKs)
  - [Фрикина София](https://github.com/SofiaFrikina)

- Backend
  - [Ротбардт Ольга](https://github.com/esfiro4ka)
    * настройка CI/CD, деплой проекта на сервер
    * проверка миграций и тестирования на GitHub
    * создание приложения users
    * обработка эндпоинтов (пользователи)
    * тестирование
  - [Дунаева Клавдия](https://github.com/KlavaD)
    * настройка pre-commit
    * автогенерация документации
    * автоматическое наполнение БД тестовыми данными
    * создание приложения idps
    * обработка эндпоинтов (ИПР)
    * настройка админки
    * тестирование
  - [Ковалев Никита](https://github.com/NV-Kovalev)
    * авторизация
    * тестирование
  - [Лашков Павел](https://github.com/hutji)
    * тестирование


## Архив с кодом репозитория и скриншотами <a id="archive"></a>

  [ЯндексДиск](https://disk.yandex.ru/d/2zvYj-K8zfXQVw)

## Документация <a id="documentation"></a>

Документация сгенерирована автоматически при помощи drf-spectacular.

[Swagger](https://yahackathon.ddns.net/api/schema/docs/#/)

[Redoc](https://yahackathon.ddns.net/api/schema/redoc/)

## Стек технологий <a id="tools"></a>

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.1-green)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14.0-orange)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.10-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10.24-blue)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-alpine-brightgreen)](https://nginx.org/)
[![drf-spectacular](https://img.shields.io/badge/drf--spectacular-0.27.0-blue)](https://drf-spectacular.readthedocs.io/)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## Установка зависимостей для работы локально<a id="installation"></a>

1. Склонируйте репозитории фронтенда и бэкенда, положив их рядом друг с другом, на локальную машину и перейдите в бэкенд:

  ```
    git clone git@github.com:hackathon-individual-development-plan/backend.git
    git clone git@github.com:hackathon-individual-development-plan/frontend.git
    cd backend
  ```

2. Создайте и активируйте виртуальное окружение:

  ```
    python3 -m venv env
    source env/scripts/activate (Для Windows)
    source env/bin/activate (Для Linux)
  ```

3. Установите зависимости:
  ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
  ```

## Настройка <a id="setting"></a>

1. Настройте pre-commit:
  ```
    pre-commit install
  ```
> **Примечание**:
  > Перед каждым коммитом будет запущен линтер и форматтер,
  > который автоматически отформатирует код
  > согласно принятому в команде codestyle.
  > Можно запустить pre-commit без коммита командой:
    ```
      pre-commit run --all-files
    ```

2. Перейдите в infra и создайте .env файл:
  ```
    cd infra
    touch infra/.env
  ```

3. Заполните по примеру своими значениями:
  [скопируйте этот файл](./infra/.env.example)

## Запуск локально <a id="startlocal"></a>
 ```
    python3 manage.py runserver
    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver
  ```

## Запуск в контейнере <a id="start"></a>

Запустите контейнеры с проектом командой:
  ```
    docker-compose -f infra/docker-compose.yml up -d
  ```

## Наполнение БД <a id="database"></a>

Наполните БД тестовыми данными:
* локально
  ```
    python3 manage.py fill_db
  ```
* в контейнере
  ```
    docker-compose exec backend python manage.py fill_db
  ```
## Тесты и покрытие <a id="tests"></a>

Запустите тесты:

  ```
    python3 manage.py test
  ```
  или
  ```
    coverage run manage.py test
    coverage report
  ```

Покрытие составляет 97 процентов.

![Процент покрытия](./media/test_coverage.jpg)


##  Frontend <a id="frontend"></a>

[https://github.com/hackathon-individual-development-plan/frontend](https://github.com/hackathon-individual-development-plan/frontend)


[Оглавление](#contents)
