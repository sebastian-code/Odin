from ConfigParser import ConfigParser
import random
import os

from fabric.api import env, local, run, cd, sudo
from fabric.operations import prompt
from fabric.contrib.files import append, exists, upload_template


REPO_URL = 'https://github.com/HackBulgaria/Odin.git'
env.host = prompt('Your domain:')
site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
source_folder = site_folder + '/source'


def provision():
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
    _create_directory_structure_if_neccessary()
    _install_requirements_if_neccessary()
    _create_db_cluster_database_and_user_with_privileges()


def _install_requirements_if_neccessary():
    sudo('apt-get update')
    sudo('apt-get install -y git postgresql postgresql-contrib nginx python3-pip python-pip')
    sudo('pip3 install virtualenv gunicorn jinja2')


def _create_db_cluster_database_and_user_with_privileges():
    sudo('su - postgres')
    run('pg_createcluster 9.3 main --start')
    run('createdb odin_db')
    run('createuser -s -l -P odin_role')
    run('psql -c \'GRANT ALL PRIVELEGES ON DATABASE odin_db TO odin_role;\'')


def deploy():
    _create_directory_structure_if_neccessary()
    _get_latest_source()
    _set_settings()
    _create_or_update_virtualenv()
    _update_static_files()
    _initialize_database()


def _initialize_database():
    with cd(source_folder):
        run('..virtualenv/bin/python manage.py syncdb --all --noinput')
        run('..virtualenv/bin/python manage.py migrate --fake --noinput')


def update():
    _get_latest_source()
    _update_static_files()
    _update_database()


def _create_directory_structure_if_neccessary():
    subfolders_to_create = ('database', 'source', 'static', 'virtualenv')
    for subfolder in subfolders_to_create:
        run('mkdir -p {}/{}'.format(site_folder, subfolder))


def _get_latest_source():
    if exists(source_folder + '/.git'):
        with cd(source_folder):
            run('git fetch')
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    with cd(source_folder):
        run('git reset --hard {}'.format(current_commit))


def _set_settings():
    template_path = source_folder + '/deploy_tools/local_settings_template.jinja'
    local_settings_path = source_folder + '/odin/local_settings.py'
    settings_path = source_folder + '/odin/settings.py'
    settings_context = _create_settings_context()

    upload_template(filename=template_path, destination=local_settings_path,
                    use_jinja=True, context=settings_context)
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_ROOT = os.path.join(BASE_DIR, '../static')
    append(settings_path, 'BASE_DIR = {}'.format(BASE_DIR))
    append(settings_path, 'STATIC_ROOT {}'.format(STATIC_ROOT))


def _create_settings_context():
    config_parser = ConfigParser()
    config_parser.read('fabfile_settings.ini')

    container_ip = 'ifconfig eth0 | grep \'inet addr:\' | cut -d: -f2 | awk \'{ print $1}\''

    SECRET_KEY = config_parser.get('Odin', 'SECRET_KEY') or _generate_secret_key
    ENGINE = config_parser.get('Odin', 'ENGINE')
    NAME = config_parser.get('Odin', 'NAME')
    USER = config_parser.get('Odin', 'USER')
    PASSWORD = config_parser.get('Odin', 'PASSWORD')
    HOST = config_parser.get('Odin', 'HOST')
    PORT = config_parser.get('Odin', 'PORT')
    ALLOWED_HOSTS = config_parser.get('Odin', 'ALLOWED_HOSTS') or [container_ip, env.host]
    DEBUG = config_parser.get('Odin', 'DEBUG')
    GITHUB_OATH_TOKEN = config_parser.get('Odin', 'GITHUB_OATH_TOKEN')
    return locals()


def _generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(50))


def _create_or_update_virtualenv():
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder, '/bin/pip'):
        run('virtualenv --python=python2.7 {}'.format(virtualenv_folder))
    run('{}/bin/pip install -r {}/requirements/stable.pip'.format(virtualenv_folder, source_folder))


def _update_static_files():
    with cd(source_folder):
        run('../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    with cd(source_folder):
        run('../virtualenv/bin/python manage.py migrate --noinput')
