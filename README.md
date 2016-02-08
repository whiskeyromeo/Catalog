
# Catalog

>Catalog is a simple RESTful app built with Flask

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

In order to drop the database

```sh
$ python manage.py dropDB
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


### Credits

- [Udacity Discussions] - Adarsh's response here helped me establish the xml endpoint. 
- [Pluralsight] - The file structure is based on the 'Introduction to the Flask Microframework' course on Pluralsight by Reindert-Jan Ekker. I highly recommend the course as in introduces the use of blueprints and database migrations very effectively.
 - [StackExchange] -  Json serialization idea came from Plaes answer.



[Udacity Discussions]: <https://discussions.udacity.com/t/create-an-additional-api-end-points-in-project-3/27060/2>
[Pluralsight]: <https://www.pluralsight.com>
[StackExchange]:<http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask>
