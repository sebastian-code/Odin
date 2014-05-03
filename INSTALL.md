# Install python 2.7 and pip

If you are using Ubuntu just type:
```
sudo apt-get install python-pip
```
# Set up a virtual env and activate it

```
virtualenv <the path where you whant to place it> -p <path to python2.7>
source <the path where you paced it>bin/activate
```

# Get the project

You can get the leatest version of the project by cloning it from git:

```
git clone https://github.com/HackBulgaria/Odin
```

# Install all the requirements
You will need python-dev before installing the requirements.txt
```
sudo apt-get install python-dev
pip install -r requirements.txt
```

# Do some configs
Rename the `odin/example_local_settings.py` to `odin/local_settings.py`
Then the new file with your settings. For more information about the diferent databases read https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Make database
```
python manage.py syncdb --all
python manage.py migrate --fake
```
# Run the project
```
python manage.py runserver
```
