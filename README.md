# task_plastilin

Task_plastilin — это решение тестового задания на позицию `python-разработчик` в компанию `Plastilin`. </br>


# Дополнительная информация

- Для создания суперпользователя из директории `task_plastilin` выполните в консоли: </br>
```
python manage.py csu
```
- Для просмотра покрытия кода тестами введите в консоли:
```
coverage run --source='.' manage.py test
coverage report
```
- Для получения качественного анализа программного кода введите в консоли:
```
flake8 --config .flake8
```

# Клонирование репозитория

В проекте для управления зависимостями используется [poetry](https://python-poetry.org/). </br>
Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/task_plastilin.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/task_plastilin.git
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
```

# Работа с базой данной PostgreSQL

- Установите PostgreSQL, если он не установлен. Для этого, например для Ubuntu, выполните в консоли:
```
sudo apt install postgresql
```
- Выполните вход в интерактивную оболочку PostgreSQL от имени `postgresql`, выполнив в консоли:
```
sudo -i -u postgres psql
```
- Создайте базу данный для проекта, выполнив в консоли:
```
CREATE DATABASE task_plastilin;
```
- Закройте интерактивную оболочку PostgreSQL:
```
\q
```
# Работа с переменными окружения

В проекте для получения курса валют используется [apilayer](https://apilayer.com/). </br>
- В директории `task_plastilin` создайте файл `.env`. Пример содержимого файла:
- Пример содержимого файла `.env` для запуска сервиса через docker:
```
HOST=название текущего хоста — db (из docker-compose)
NAME=название базы данных — postgres
USER=имя текущего пользователя — postgres
PASSWORD=пароль текущего пользователя — ваш пароль

POSTGRES_USER=имя пользователя — postgres
POSTGRES_PASSWORD=пароль пользователя — ваш пароль 
POSTGRES_DB=название базы данных для подключения из docker — db (из docker-compose)

EMAIL_BACKEND=путь импорта Python для вашего класса бэкенда
EMAIL_HOST=хост SMTP
EMAIL_HOST_USER=адрес электронной почты для аутентификации на почтовом сервере
EMAIL_HOST_PASSWORD=пароль для аутентификации на почтовом сервере

LOCATION=местоположение используемого кеша (redis://redis:6379)

API_KEY=API ключ для получение курса валют
``` 
- Пример содержимого файла `.env` для запуска сервиса на локальной машине без docker:
```
HOST=название текущего хоста — localhost
NAME=название базы данных — task_plastilin
USER=имя текущего пользователя — postgres
PASSWORD=пароль текущего пользователя — ваш пароль

EMAIL_BACKEND=путь импорта Python для вашего класса бэкенда
EMAIL_HOST=хост SMTP
EMAIL_HOST_USER=адрес электронной почты для аутентификации на почтовом сервере
EMAIL_HOST_PASSWORD=пароль для аутентификации на почтовом сервере

LOCATION=местоположение используемого кеша (redis://127.0.0.1:6379)

API_KEY=API ключ для получение курса валют
``` 

# Работа с миграциями

Из директории `task_plastilin` выполните в консоли: </br>

```
python manage.py migrate
```

# Запуск сервера Django

- Активируйте виртуальное окружение согласно п. `Клонирование репозитория` </br>

- Из директории `task_plastilin` выполните в консоли: </br>
```
python3 manage.py runserver
```

# Запуск сервера Django c использованием docker-compose

- Установите `docker` согласно инструкции на сайте [docker](https://www.docker.com/get-started/). </br>
- Запустите образ для запуска нескольких контейнеров с использованием `docker-compose`. Для этого из директории `task_plastilin` выполните в консоли: </br>
```
docker-compose build
```
- Запустите собранный образ. Для этого из директории `task_plastilin` выполните в консоли: </br>
```
docker-compose up
```
- Или для запуска образа в фоновом режим из директории `task_plastilin` выполните в консоли: </br>
```
docker-compose up -d
```
- В новой открытой сессии создайте суперпользователя. Для этого из директории `task_plastilin` выполните в консоли: </br>
```
docker-compose exec web python manage.py csu
```
- Сервис будет доступен по URL `http://127.0.0.1:8000/` </br>
- Для остановки работы образа из директории `task_plastilin` в консоли нажмите `CTRL + C`: </br>
- Для удаления остановленного образа из директории `task_plastilin` в консоли выполните: </br>
```
docker-compose down
```