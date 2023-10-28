<h2 align="center">Finance FastAPI</h2>


### Описание проекта:
Веб-приложение финансов написанный на FastAPI.
- JWT авторизация
- CRUD пользователей
- CRUD категорий
- CRUD транзакций
- CRUD баланса
- Отправка Email

## To Do:
- Расширить функционал приложение
- Доработать веб-интерфейс для пользователя

### Инструменты разработки

**Стек:**
- Python >= 3.11
- FastAPI == 0.96.0
- PostgreSQL
- Docker
- Redis
- Alembic
- SQLAlchemy
- Nginx
- Grafana
- Prometheus
- Starlette_exporter

## Разработка

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) Создать виртуальное окружение

    python -m venv venv

##### 4) Активировать виртуальное окружение


##### 5) Устанавливать зависимости:

    pip install -r req.txt

##### 6) Переименовать файл .env.example на .env и изменить на свои данные

##### 7) Установить docker на свою ОС

##### 8) Запустить контейнеры с базами данными через docker

    make up

##### 9) Перейти по адресу

    http://127.0.0.1:8000/docs


##### 10) Для взаимодействия с веб-интерфейсом перейти по адресу

    http://127.0.0.1:8000/base



