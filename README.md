# Стек технологий в проекте

* FastAPI
* SQLite
* Python

## Описание проекта

Проект QRKot — это проект благотворительного фонда поддержки котов. Фонд собирает пожертвования на различные целевые проекты.

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```bash
git@github.com:Devayter/cat_charity_fund.git
```

```bash
cd yacut
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### Для применения миграций

```bash
alembic upgrade head
```

Запустить программу

```bash
uvicorn app.main:app --reload
```

## Примеры запросов

* Создание проекта

### POST charity_project

```url
http://127.0.0.1:8000/charity_project/
```

```json
{
  "description": "project_description",
  "full_amount": 1000,
  "invested_amount": 0,
  "name": "project_name"
}
```

* Ответ

```json
{
  "id": 1,
  "full_amount": 1000,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2019-08-24T14:15:22Z",
  "name": "project_name",
  "description": "project_description"
}
```

* Создание пожертвования

### POST donation

```url
http://127.0.0.1:8000/donation/
```

```json
{
  "full_amount": 100,
  "comment": "some_comment"
}
```

* Ответ

```json
{
  "id": 1,
  "full_amount": 100,
  "create_date": "2019-08-24T14:15:22Z",
  "comment": "some_comment"
}
```

* Регистрация пользователя

### POST user

```url
http://127.0.0.1:8000/auth/register
```

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

* Ответ

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

## Ссылка на полную документацию ReDoc

[ReDoc](http://127.0.0.1:8000/redoc)

## Ссылка на полную документацию Swagger

[Swagger](http://127.0.0.1:8000/docs)

## Авторы

* [Павел Рябов](https://github.com/Devayter/)
