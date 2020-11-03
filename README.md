# Football Formation Generator

## System requirements

The following packages are mandatory to run the system:

- Python 3.8.5 or higher (Not tested in lower versions of Python, but it should work as long as it is Python 3.x)
- virtualenv
- python-dev
- default-libmysqlclient-dev
- python3-dev
- mysql-server

## Installation & Configuration

Clone or download this repository to any directory you want in your computer. After that, you have to run the following command in the root folder of the project: `python3 -m venv env`

After the folder has been created, you have to run `source env/bin/activate` to activate the virtual environment

Once you are running a terminal with the virtual environment activated, you have to run `pip install -r requirements.txt` to install all the requirements of the server.

Assuming you already have MySQL Installed, you'll have to create a database with the name "ffg" (without quotation marks) and an user called "ffg" with password "Ffg.1234" (without quotation marks). After that, give the user all the privileges over ffg.
```
CREATE DATABASE ffg;
CREATE USER 'ffg'@'localhost' IDENTIFIED BY 'Ffg.1234';
GRANT ALL PRIVILEGES ON ffg.* TO 'ffg'@'localhost';
```
If you wish to use another user, database and password, you can change the settings file in ```project_root/ffg_be/settings.py```

In addition, you'll have to make the migrations to the database. In order to do that, open the terminal with the env and run `python manage.py migrate` (You don't need to run `python manage.py makemigrations` since the migrations file is already up to date).

Finally, running `python manage.py runserver` should start the server.
