# Dependencies:
* python 3.4
* virtualenv (python virtual environment)
* pip 1.5.4 (python package manager)
* python-dev (header files and a static library for python)
* libmysqlclient-dev (MySQL database client library)

## Important!
The package install snippets below are for Ubuntu distros and Ubuntu flavours.
For your distro the package manager and packages may differ.

```
sudo apt-get install python3-pip
```
might be, as in openSUSE
```
sudo zypper install python3-pip
```

# Install python 3.4, virtualenv and pip 1.5.4
```
sudo apt-get install python3
sudo apt-get install python3-virtualenv
sudo apt-get install python3-pip
```

# Set up a virtual env and activate it
```
virtualenv <the path where you want to place it> -p <path to python2.7>
source <the path where you placed it>bin/activate
```

# Get the project
You can get the latest version of the project by cloning it from git:

```
git clone https://github.com/HackBulgaria/Odin.git
```

# Install all the requirements
```
sudo apt-get install python3-dev
sudo apt-get install libmysqlclient-dev
pip install -r requirements/stable.pip
```

# Setup a database
If you want to use a MySQL DB. Install the server, create a root password, create a database.
```
sudo apt-get install mysql-server
# server should be started automatically, but just in case restart it
sudo service mysql restart
mysql -u root -p
# now you should be prompted to enter your password
# and if you authed correctly
CREATE DATABASE <dbname> CHARACTER SET utf8;
```

If you want to use a PostgreSQL DB. Install the server, install psycopg2 (django PostgreSQL connector), create a database.
```
sudo apt-get install postgresql
# server should be started automatically, but just in case restart it
sudo service postgresql restart
pip install psycopg2
sudo -u postgres createdb <dbname>
```

If you want to use MongoDB. Follow [this great presentation](http://staltz.github.io/djangoconfi-mongoengine/).
It's important to note that many of the models need to be refactored to work.


# Do some configs
Rename the `odin/example_local_settings.py` to `odin/local_settings.py`. This will be your settings file.
Adjust your database settings in `local_settings.py`.
For more information about the diferent databases read https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Now try populating the database
If you want to import data from a previous Django set up database:
```
python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > <dump_name>.json
python manage.py loaddata <dump_name>.json
```

If you want to start with a clean database:
```
python manage.py syncdb --all
python manage.py migrate --fake
```


# Run the project
```
python manage.py runserver
```
