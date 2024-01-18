# backend AlfaIPD
<details>
  <summary>Оглавление</summary>
  <ol>
    <li>
      <a href="#описание">О проекте</a>
      <ul>
        <li><a href="#зависимости">Установка зависимостей</a></li>
      </ul>
    </li>
    <li>
      <a href="#настройка">Настройка</a>
      <ul>
        <li><a href="#запуск">Запуск</a></li>
      </ul>
    </li>
  </ol>
</details>

## О проекте [](#описание)
MVP индивидуального плана развития для сотрудников в Альфа-Банке
## Установка зависимостей [](#зависимости)

1. Склонируйте репозиторий на локальную машину:
  ```
    git clone https://github.com/hackathon-individual-development-plan/backend.git
  ```

2. Создайте и активируйте виртуальное окружение
  ```
    python3 -m venv env
    source env/scripts/activate ( Для Windows)
    source env/bin/activate ( Для Linux)
  ```


3. Установите зависимости
  ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
```

4. Настроить pre-commit
  ```
    pre-commit install
  ```
> **Примечание**:
  > Перед каждым коммитом будет запущен линтер и форматтер,
  > который автоматически отформатирует код
  > согласно принятому в команде codestyle.
  > можно запустить pre-commit без коммита, чтоб посмотреть как работает:
  > команодй:
    ```
    pre-commit run --all-files
    ```


5. Создайте в папке infra .env файл
  ```
    touch .env
  ```
7. Заполните по примеру со своими значениями
  [Скопируйте этот файл](./infra/.env.example)

## Запуск [](#запуск)
1. Запустите БД командой:
  ```
    docker-compose -f infra/docker-compose.yml up -d
  ```
2. Запустить проект:

  ```
    python3 manage.py runserver
  ```
## Запуск [](#запуск)
