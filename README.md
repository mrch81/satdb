# Overview

Satdb is a lightweight and type-safe [Django]((https://www.djangoproject.com/)) app for storing and querying Satellite informations such as its owner, payloads, TLE info and launcher.

The objective of the project is to exploit:

- GraphQL querying capabilities 
- WebSocket subscriptions for updates

The project includes:
- [x] **Backend**: a Django backend service with GraphQL API framework using graphene and graphene-django
- [x] **Fetch Service**: a service that periodically fetches TLE information from an Open API. Celery can be used but the objective is to exploit asyncio.
- [] **Frontend**: Working on it. I haven't yet decided whether to use Angular or React
- [x] **CI Gitlab**: CI pipelines for QA and testing on [Gitlab](https://gitlab.com/webfw1/satdb)
- [x] **CI Github**: Actions for QA and testing on Github
- [x] **Containerisation**: a dockerfile and a docker-compose.yml for containerisation.
- [x] **Fixtures**: fixtures to generate initial data for tests
- [x] **Testing**: Unit tests, of course!
- [x] **Package Management**: Package and dependencies installation using Poetry as well as pip.
- [x] **Database**: A default sqlite database. Postgresql is recommended.

---

## Database Schema

![image description](docs/schema.v1.0.png)

---


#  Installation

## Project Requirements

- [Python](https://www.python.org/) 3.10.*
- [Django](https://www.djangoproject.com/) 4.2.*
- [Docker](https://www.docker.com/).
- [Docker Compose](https://docs.docker.com/compose/install/).
- [Dependencies](pyproject.toml)

### Installation - Local

1. **Install dependencies:**
    
    ```console
    poetry install
    ```

3. **Run migrations:**

    ```console
    poetry run python manage.py migrate
    ```

4. **Run the backend:**

    ```console
    poetry run python manage.py runserver 0.0.0.0:8000
    ```

5. **Run the fetch service:**


    ```console
    poetry run python fetch_service\tle_updater.py 
    ```

6. **Query data in django admin page:**

    Go to your internet browser and consult: http:\\localhost:8000\graphql\


### Installation - Docker


### Installation Steps

1. **Build the Docker image:**

    ```console
    docker build -t satdb .
    ```
3. **Launch Docker Compose:** 

    ```console
    docker-compose up
    ```

##  Query examples

1. **Query: get available satellite list:**

TODO

2. **Mutation: update satellite:** 

TODO