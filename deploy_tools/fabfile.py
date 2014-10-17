from ConfigParser import ConfigParser
import os
import random

from fabric.api import env, local, run, cd, sudo
from fabric.context_managers import settings
from fabric.contrib.files import append, exists, upload_template


def __generate_dict_from_ini_file_section(section):
    config_parser = ConfigParser()
    config_parser.read('fabfile_settings.ini')

    ## Alternative with different API calls. Not sure if I should delete it yet.
    # dictionary = {}
    # for option in config_parser.options(section):
    #     dictionary[option.upper()] = config_parser.get(section, option)
    return {option.upper(): value for option, value in config_parser.items(section)}


def provision():
    app_settings = __generate_dict_from_ini_file_section('APP')
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host or app_settings['HOST'])
    linux_packages = app_settings['LINUX_PACKAGES']
    python_packages = app_settings['PYTHON_PACKAGES']
    db_settings = __generate_dict_from_ini_file_section('DB')

    _create_directory_structure_if_neccessary(site_folder)
    _install_requirements_if_neccessary(linux_packages, python_packages)
    _create_db_cluster_database_and_user_with_privileges(db_settings)


def _create_directory_structure_if_neccessary(site_folder):
    subfolders_to_create = ('database', 'source', 'static', 'virtualenv')
    for subfolder in subfolders_to_create:
        run('mkdir -p {}/{}'.format(site_folder, subfolder))


def _install_requirements_if_neccessary(linux_packages, python_packages):
    sudo('apt-get update')
    sudo('apt-get install {}'.format(linux_packages))
    sudo('pip3 install {}'.format(python_packages))


def _create_db_cluster_database_and_user_with_privileges(db_settings):
    with settings(warn_only=True, sudo_user=db_settings['SUDO_USER']):
        sudo('pg_createcluster {} main --start'.format(db_settings['VERSION']))
        sudo('createdb {}'.format(db_settings['NAME']))
        sudo('createuser {} {}'.format(db_settings['PRIVILEGES'], db_settings['USERNAME']))
        sudo('psql -c \'GRANT ALL PRIVILEGES ON DATABASE {} TO {};\''.format(db_settings['NAME'],
                                                                             db_settings['USERNAME']))


def deploy():
    app_settings = __generate_dict_from_ini_file_section('APP')
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host or app_settings['HOST'])
    source_folder = site_folder + '/source'

    _create_directory_structure_if_neccessary(site_folder)
    _get_latest_source(source_folder, app_settings)
    _set_settings(source_folder)
    _create_or_update_virtualenv(source_folder, app_settings)
    with cd(source_folder):
        _initialize_database()
        _update_static_files()


def _get_latest_source(source_folder, app_settings):
    if exists(source_folder + '/.git'):
        with cd(source_folder):
            run('git fetch')
    else:
        run('git clone {} {}'.format(app_settings['REPO_URL'], source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    with cd(source_folder):
        run('git reset --hard {}'.format(current_commit))


def _initialize_database():
    run('../virtualenv/bin/python manage.py syncdb --all --noinput')
    run('../virtualenv/bin/python manage.py migrate --fake --noinput')


def update():
    app_settings = __generate_dict_from_ini_file_section('APP')
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host or app_settings['HOST'])
    source_folder = site_folder + '/source'

    _get_latest_source(source_folder, app_settings)
    _update_static_files()
    _update_database()


def _set_settings(source_folder):
    template_path = 'local_settings_template.jinja'
    local_settings_path = source_folder + '/odin/local_settings.py'
    settings_context = _create_settings_context()

    upload_template(filename=template_path, destination=local_settings_path,
                    use_jinja=True, context=settings_context)
    run('cat {}'.format(local_settings_path))
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_ROOT = os.path.join(BASE_DIR, '../static')

    settings_path = source_folder + '/odin/settings.py'
    append(settings_path, 'BASE_DIR = \'{}\''.format(BASE_DIR))
    append(settings_path, 'STATIC_ROOT = \'{}\''.format(STATIC_ROOT))


def _create_settings_context():
    context = __generate_dict_from_ini_file_section('DJANGO')

    if not context['ALLOWED_HOSTS']:
        container_ip = run('ifconfig eth0 | grep \'inet addr:\' | cut -d: -f2 | awk \'{ print $1}\'')
        context['ALLOWED_HOSTS'] = [container_ip, ]
    if not context['SECRET_KEY']:
        context['SECRET_KEY'] = _generate_secret_key()
    return context


def _generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(50))


def _create_or_update_virtualenv(source_folder, app_settings):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python={} {}'.format(app_settings['PYTHON_VERSION'], virtualenv_folder))
    run('{}/bin/pip install -r {}/requirements/stable.pip'.format(virtualenv_folder, source_folder))


def _update_static_files():
    run('../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('../virtualenv/bin/python manage.py migrate --noinput')
