# backend AlfaIPD

## Оглавление <a id="contents"></a>

1. [О проекте](#about)
2. [Установка зависимостей](#installation)
3. [Настройка](#setting)
4. [Запуск](#start)
5. [Авторы проекта](#authors)


## О проекте <a id="about"></a>

MVP индивидуального плана развития для сотрудников в Альфа-Банке.

## Установка зависимостей<a id="installation"></a>

1. Склонируйте репозиторий на локальную машину и перейдите в него:
  ```
    git clone https://github.com/hackathon-individual-development-plan/backend.git
    cd backend
  ```

2. Создайте и активируйте виртуальное окружение
  ```
    python3 -m venv env
    source env/scripts/activate (Для Windows)
    source env/bin/activate (Для Linux)
  ```

3. Установите зависимости
  ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
  ```

## Настройка <a id="setting"></a>

4. Настроить pre-commit
  ```
    pre-commit install
  ```
> **Примечание**:
  > Перед каждым коммитом будет запущен линтер и форматтер,
  > который автоматически отформатирует код
  > согласно принятому в команде codestyle.
  > Можно запустить pre-commit без коммита, чтобы посмотреть как работает,
  > командой:
  ```
    pre-commit run --all-files
  ```

5. Создайте .env файл
  ```
    touch infra/.env
  ```
6. Заполните по примеру со своими значениями
  [Скопируйте этот файл](./infra/.env.example)

## Запуск <a id="start"></a>

1. Запустите БД командой:
  ```
    docker-compose -f infra/docker-compose.yml up -d
  ```
2. Запустить проект:

  ```
    python3 manage.py migrate
    python3 manage.py fill_db
    python3 manage.py createsuperuser
    python3 manage.py runserver
  ```

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

Backend
  - [Ротбардт Ольга](https://github.com/esfiro4ka)
  - [Дунаева Клавдия](https://github.com/KlavaD)
  - [Ковалев Никита](https://github.com/NV-Kovalev)
  - [Лашков Павел](https://github.com/hutji)

[Оглавление](#contents)
