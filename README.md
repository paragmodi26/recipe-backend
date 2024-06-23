## Recipe Master APIs

--------------


[![Python](https://img.shields.io/badge/Python-3.9_%7C_3.10_%7C_3.11-goldenrod)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python_Framework-green)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-Application_Server-orange)](https://www.uvicorn.org/)
[![Postgres](https://img.shields.io/badge/PostgreSQL-Database-mediumblue)](https://www.postgres.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Database_Toolkit-dodgerblue)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migration_tool-darkorange)](https://alembic.sqlalchemy.org/en/latest/)
[![Aioredis](https://img.shields.io/badge/Aioredis-Redis_Library-dodgerblue)](https://aioredis.readthedocs.io/en/latest/)



## 📝 Table of Contents
- 💡 [About](#about)
- 🏁 [Getting Started](#getting-started)
- 🛠️ [Prerequisites](#prerequisites)
- 🚀 [Setup Process](#setup-process)
- ⚙️ [Built Using](#built-using)

## 🧐 About <a name="about"></a>
This application serves APIs/Tasks for a Master Recipe application.

## 🏁 Getting Started <a name="getting-started"></a>

### Prerequisites
1. 💻 [Python](https://www.python.org/downloads/release/python-390/)
2. 📦 [Pipenv](https://pypi.org/project/pipenv/)

 --------------
 ## Setup Process
 
 - Clone the repository

     ```bash
     git clone https://github.com/
     ```
 
 - Create and set up the virtual env for [python](https://docs.python.org/3/library/venv.html) using pipenv.
 - Activate virtual environment
 
      ```bash
      pipenv shell
      ```
 - Install all the dependencies in venv : this command will use the already present Pipfile to install dependencies.
     ```bash
     pipenv install
     ```
 

  - create database with any name inside this database create schema with name recipe_db.
  - After creating schema run the below cmd

     ```bash
       alembic -c ./src/alembic.ini upgrade head
     ```
    
 
 - Optional : if alembic version is not present, generate one.
     ```bash
     alembic -c ./src/alembic.ini revision --autogenerate -m "1st version"
     ```
   
 - Optional Reflect schema changes to database table using alembic
     ```bash
     alembic -c ./src/alembic.ini upgrade head
     ```
     
 - If there are any error in this command check
     - database connection and credentials in config/env.py
     - already present schema
 
 - Run the fastapi server
     ```bash
     uvicorn --reload src.main:app
     ```
   
     ** mac users remove --reload form above command if it keeps reloading
 

    
- For swagger or openapi.json use url
- http://0.0.0.0:8000/docs

- Sample APIs Curl
 ```curl -X 'POST' \
      'http://127.0.0.1:8000/rich/api/v1/recipe/save' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -H 'fid: 3788197563718933477' \
      -d '{
      "name": "a",
      "description": "straaaaaing"
    }'
  ```

- Health Check APIs Curl
 ```curl -X 'POST' \
      'http://127.0.0.1:8000/frammer-internal/api/v1/ping/healthcheck'  \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json'
  ```

 ## ⛏️ Built Using <a name="built_using"></a>

- 🚀 [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- 🦄 [Uvicorn](https://www.uvicorn.org/) - Application Server
- 📦 [PostgreSQL](https://www.postgresql.com/) - Database
- 📚 [SQLAlchemy](https://www.sqlalchemy.org/) - The Database Toolkit for Python
- 🛠️ [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Migration tool
