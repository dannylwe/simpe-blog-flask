## create database
```
$ python
>> from api import db,create_app
>> db.create_all(app=create_app())
```

## start application
```
$ export FLASK_APP=api
$ export FLASK_DEBUG=1
$ export FLASK_ENV=development
$ flask create_admin
$ flask run
```