{% if False %}
# Introduction

The goal of this project is to create RESTful backend service for a medical application that allows users to manage and access their medical records. 


![Preview](screenshot.png?raw=true "Medical App")

### Main features

* User Managment

* Record Management


# Setup

### Requirement
- Docker (Docker Desktop v4.x.x)
- Docker Compose
- Python 3.11
- <a href="https://python-poetry.org/docs/">Poetry</a>
- <a href="https://black.readthedocs.io/en/stable/">Black</a>

### Docker Installation

1. The `.env-sample` should be modified appropriately and renamed to `.env`. However, the value of the variable `POSTGRES_HOST` has a default value which can be modified, if modified, the service name for the PostgreSQL conatiner must be modified accordingly.

2. Use the command `docker-compose up --build` should be run in the root of the project to build the Docker Images and spin up the containers. If the operation is successfull, two containers should be running, and the Django Superuser describe in the .env should be created.
![Preview](docker.png?raw=true "Docker Dashboard")

3. All python dependencies for the project are defined in `pyproject.toml`.

4. The containers can stopped at anytime running the command `docker-compose down`.

5. It's important to note also that the PostgreSQL container has a persistent volume attached to it, so that data store in table are not destroyed whenever the container restarts. If there be any need to discard the volume, the command `docker-compose up -v` could be useful.
      
### virtualenv
Deploying the App using virtual environment requires setting up the appropriate values for the database connection variables in the `.env` file.

{% endif %}

# Medical App

# Getting Started
Once the app is fully setup, the `postman_collection.json` file can be imported into Postman for access to samples of API requests and responses for all the endpoints. Where necessary, the authentication and types for the different api mention in the documentation tab.

# Testing
`pytest 7.4.2` and `pytest-django 4.5.2` are used for the tests. The tests has been setup to run even outside the container environment. The `db.sqlite` in the root of the project is the database used for the test.if for any reason the file is missing from the root, once the `python manage.py makemigration` the db file will be recreated.
