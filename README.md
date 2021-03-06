
# Catalog

>Catalog is a simple RESTful app built with Flask and postgres

## TODOS

- Add CSRF Support For Delete
- Refactor catalog

### Getting Started

Install the necessary packages

```sh
$ pip install -r requirements.txt
```

List out the possible commands from the manager
```sh
$ python manage.py
```

To initialize the database, use the db commands
To list the db commands

```sh
$ python manage.py db
```

Ensure that you have postgres set up and create a user by the name of 'catalog'
```
$ psql
> create user catalog;
```

To init the migration file structure

```sh
$ python manage.py db init
```

Create an initial migration with the message tag "initial"

```sh
$ python manage.py db migrate -m "initial"
```

Begin using the initial migration file

```sh
$ python manage.py db upgrade --tag initial
```

Use the manager to seed the database

```sh
$ python manage.py seedDB
```

To reset the database to the initial migration once it has been dropped

```sh
$ python manage.py db migrate
$ python manage.py db upgrade
```

Finally, to run the server

```sh
$ python manage.py runserver
```



### Tech

Currently the project relies on the following requirements

- Flask
- Flask-Migrate
- Flask-Sqlalchemy
- Flask-WTF
- WTForms
- oauth2client
- Requests 
- Flask-Script
