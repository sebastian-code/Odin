## Deploy tools

This fabfile script will automate the provision, deployment and update.
It gets most of the settings from `fabfile_settings.ini`.

## How to deploy updates

The deployment workflow, when you have new updates, is the following:

1. Commit & push your changes to Odin's remote in the proper branch
2. Make Pull Request, and get your changes to master.
3. Go to the base folder of Odin and run the following command: `make deploy-update`
4. You will have to fill the two variables in the `Makefile` - `{{ USERNAME }}` and `{{ HOST }}`
5. This will fetch the latest master to the production server


## Requirements:

* Python 2.7
* Fabfile
* Jinja2


## How to use:

Assuming that you've already set your settings in `fabfile_settings.ini`,
run any of the available commands - `provision`, `deploy`, `update`.

```python
fab -f fabfile.py -H root@example.com command
```
* `-f` specifies the path to the fabfile to read. You can skip it and it may still work,
but it's if you use the flag anyway.
* `-H` specifies the SSH destination,
* `command` is any of the available commands.


## Utilize the Jinja templates

Fabric's `upload_to_template()` isn't so reliable in non-home folders.
Just in case check and/or manually replace the template tags and save the following files:


### Nginx config

* Replace `nginx.jinja` and save in `/etc/nginx/sites-available/{{ DOMAIN }}`,

* Create a symlink pointing to the newly created file. `ln -s /etc/nginx/sites-available/{{ DOMAIN }} /etc/nginx/sites-enabled/`,

* Delete the default config in sites-enabled. `rm /etc/nginx/sites-enabled/default`,

* Restart nginx. `sudo service nginx restart`.


### Gunicorn config

Replace `gunicorn-conf.jinja` and save in `{{ SOURCE_FOLDER }}/{{ APP_NAME }}/gunicorn-conf.py`


### Gunicorn upstart job

* Replace `upstart.jinja` and save in `/etc/init/gunicorn-{{ DOMAIN }}.conf`,

* Restart the gunicorn server - `sudo restart gunicorn-{{ DOMAIN }}`.
