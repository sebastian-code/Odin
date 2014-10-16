## Deploy tools

This fabfile script will automate the provision, deployment and update.
It gets most of the settings from `fabfile_settings.ini`.


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
