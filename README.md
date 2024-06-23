## Recipe Master APIs

--------------

A FastAPI application to manage recipes and user authentication.

## Overview

This project is a RESTful API built with FastAPI that allows users to perform CRUD operations on recipes and manage user authentication.


[![Python](https://img.shields.io/badge/Python-3.9_%7C_3.10_%7C_3.11-goldenrod)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python_Framework-green)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-Application_Server-orange)](https://www.uvicorn.org/)
[![Postgres](https://img.shields.io/badge/PostgreSQL-Database-mediumblue)](https://www.postgres.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Database_Toolkit-dodgerblue)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migration_tool-darkorange)](https://alembic.sqlalchemy.org/en/latest/)



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

     bash
     git clone https://github.com/paragmodi26/recipe-backend.git
     
- Install pipenv by using cmd

  - For mac
    bash 
    brew install pipenv
    
  - For other visit official website
  
 - Create and set up the virtual env for [python](https://docs.python.org/3/library/venv.html) using pipenv.
 - Activate virtual environment
 
      bash
      pipenv shell
      
 - Install all the dependencies in venv : this command will use the already present Pipfile to install dependencies.
     bash
     pipenv install
     
 

  - create database with any name inside this database create schema with name "recipe_db".
  - After creating schema run the below cmd

     bash
       alembic -c ./src/alembic.ini upgrade head
     
    
 
 - Optional : if alembic version is not present, generate one.
     bash
     alembic -c ./src/alembic.ini revision --autogenerate -m "1st version"
     
   
 - Optional Reflect schema changes to database table using alembic
     bash
     alembic -c ./src/alembic.ini upgrade head
     
     
 - If there are any error in this command check
     - database connection and credentials in config/env.py
     - already present schema
 
 - Run the fastapi server
     bash
     uvicorn --reload src.main:app
     
   
     ** mac users remove --reload form above command if it keeps reloading

    
- For swagger or openapi.json use url
    bash
    http://0.0.0.0:8000/docs
    

- For test-cases:
    run command in terminal 
    bash 
    pytest
    

##### First confirm the backend process completed and access above swagger url then continue
 ### Frontend setup process

- Clone the repository

    bash
    git clone https://github.com/paragmodi26/recipe-fronend.git
   

- Navigate to the templates directory:

    bash
    cd recipe-frontend/templates
    

- Open index.html in your browser (preferably Chrome):

    - On Windows: Right-click the index.html file and select "Open with" > "Chrome".
    - On macOS or Linux: Use your file manager to navigate to the file and double-click it, or use the terminal:
      bash
      open index.html  # macOS
      xdg-open index.html  # Linux
      



## Endpoints

### User Endpoints

- *Register User*: POST /rich/api/v1/user/save
  - Request Body:
    json
    {
        "name": "string",
        "email": "string",
        "mobile_no": "string",
        "password": "string"
    }
    
  - Response:
    json
    {
        "status": "success",
        "data": {
            "id": "int",
            "name": "string",
            "email": "string@gmail.com",
            "mobile_no": "string"
        }
    }
    

- *Login User*: POST /rich/api/v1/user/login
  - Request Body:
    json
    {
        "email": "string@gmail.com", 
        "password": "string"
    }
    
  - Response:
    json
    {
        "status": "success",
        "data": {
            "access_token": "string",
            "token_type": "string"
        }
    }
    

- *Logout User*: GET /rich/api/v1/user/logout (Requires Authentication : Bearer Token)
  - Response:
    json
    {
        "status": "success",
        "message": "Logged out successfully"
    }
    

### Recipe Endpoints

- *Create Recipe*: POST /rich/api/v1/recipe/save (Requires Authentication : Bearer Token)
  - Request Body:
    json
    {
        "name": "string",
        "title": "string",
        "description": "string",
        "ingredients": [
            {
                "name": "string",
                "quantity": "string"
            }
        ],
        "instructions": "string"
    }
    
  - Response:
    json
    {
        "status": "success",
        "message": "Recipe saved successfully"
    }
    

- *Get All Recipes*: GET /rich/api/v1/recipe/all (Requires Authentication : Bearer Token)
  - Query Parameters: 
    - page: int (default=1)
    - limit: int (default=10)
    - search_keyword: Optional string
    - is_all: bool (default=True)
  - Response:
    json
    {
        "status": "success",
        "data": [
            {
                "id": "int",
                "name": "string",
                "title": "string",
                "description": "string",
                "ingredients": [
                    {
                        "name": "string",
                        "quantity": "string"
                    }
                ],
                "instructions": "string",
                "created_by": "int"
            }
        ]
    }
    

- *Update Recipe*: PATCH /rich/api/v1/recipe/{id} (Requires Authentication : Bearer Token)
  - Request Body:
    json
    {
        "title": "string",
        "name": "string",
        "description": "string",
        "ingredients": [
            {
                "name": "string",
                "quantity": "string"
            }
        ],
        "instructions": "string"
    }
    
  - Response:
    json
    {
        "status": "success",
        "data": {
            "id": "int",
            "name": "string",
            "title": "string",
            "description": "string",
            "ingredients": [
                {
                    "name": "string",
                    "quantity": "string"
                }
            ],
            "instructions": "string",
            "created_by": "int"
        }
    }
    

- *Delete Recipe*: DELETE /rich/api/v1/recipe/{id} (Requires Authentication : Bearer Token)
  - Response:
    json
    {
        "status": "success",
        "message": "Recipe deleted successfully"
    }
    



 ## ⛏️ Built Using <a name="built_using"></a>

- 🚀 [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- 🦄 [Uvicorn](https://www.uvicorn.org/) - Application Server
- 📦 [PostgreSQL](https://www.postgresql.com/) - Database
- 📚 [SQLAlchemy](https://www.sqlalchemy.org/) - The Database Toolkit for Python
- 🛠️ [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Migration tool