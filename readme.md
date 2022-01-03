# Consulting Activity Report Application And API

## Introduction

The Consulting Activity Report (CAR) application has been developed to capture the work undertaken bu consultants while working for a client and produce a report that can be distributed on the completion of the engagement. Each CAR captures

1. The name and contact details of the client
2. The name of the consultant that has undertaken the work
3. The Statement of Work reference number under whcih the work is being undertaken
4. The date, or date range the report covers
5. The Client Manager 
6. The high level description of the work requested and the expected outcomes
7. The work actually undertaken
8. Any issues encountered and their resolution status
9. The details of any work to still to be completed or followed up 

The application will provide a searchable centralised repository of all work undertaken for a client, providing future consultants with background to work previously complete and provide client managers with a reference for client queries.


# Installation and Setup

## Dependancies

- Python 3.7 or later- Development Language
- Flask - The web application framework for the API
- Flask-Cors
- Flask-Migrate
- Flask-Script
- Flask-SQLAlchemy - 
- psycopg2-binary - PostgreSQL adapter

**NOTE:** This project assumes the use of a PostagreSQL database to query and persist data. While other relational database systems are supported by SQLAlchemy (eg SQLite3, MySQL, MS SQL Server, etc) changes will be required for the correct configuration of the database and the database adaptor/connector library.

## Environment Setup

To prevent the project libraries and modules conflicting with other applications, establish a new project directory and virtual environment in which to install the application.

```console
$ mkdir car-app
$ cd car-app
$ python3 -m venv venv
$ source venv/bin/activate
```

Clone this repository into your project directory using ```git clone``` or download the code as a zip archive and extract it into the directory.

Install all the project project dependancies with pip install

```console
$ pip install -r requirements.txt
```

### Development Setup

To test the application in a development mode, set the ```FLASK_APP``` and ```FLASK_ENV``` environment variables

```console
$ export FLASK_APP=run_app.py
$ export FLASK_ENV=development
```

When the application is set to "development" the database used by the application will be SQLite. Establish the database and database tables by performing and initial migration. 

```console
$ flask db init
$ flask db migrate
$ flask db upgrade
```

### Production Setup

```console
$ export FLASK_APP=run_app.py
$ export FLASK_ENV=production
$ export DBHOST=your-db-server
$ export DBNAME=your-db-name
$ export DBUSER=your-db-username
$ export DBPWD=your-db-password
```

As noted earlier, when the application is set to "production" the database used by the application will be PostgreSQL. Establish the database and database tables by performing and initial migration. 

```console
$ flask db init
$ flask db migrate
$ flask db upgrade
```


# API Documentation


### API Resources

[Contacts](./documentation/contacts.md)

[Clients and Client Contacts](./documentation/clients.md)

[Reports](./documentation/reports.md)

[Testing](./documentation/app_testing.md)

