<h2 align="center">Library API on FastAPI with MongoDB</h2>


### Описание проекта:
API библиотеки на FastAPI с MongoDB.
- CRUD авторов, издательств, книг

**Стек:**
- Python == 3.10.2
- FastAPI == 0.75.2
- MongoDB == 5.0.7

## Инструкция

##### 1) Сделать форк репозитория и поставить звёздочку)

##### 2) Клонировать репозиторий

    git clone https://github.com/m019m1/test_case_FastAPI_mongoDB.git

##### 3) Создать виртуальное окружение

    python -m venv venv
    
##### 4) Активировать виртуальное окружение

##### 5) Установить зависимости:

    pip install -r requirements.txt

##### 6) Заполнить БД начальными данными

    python db_init.py
        
##### 7) Запустить сервер

    uvicorn main:app --reload
    
##### 8) Перейти по адресу

    http://127.0.0.1:8000/docs
    