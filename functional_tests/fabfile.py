from fabric.api import env, run


def _get_base_folder(host):
    return '~/sites/' + host


def _get_manage_dot_py(host):
    formatted_path = _get_base_folder(host)
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(path=formatted_path)


def reset_database():
    manage_py = _get_manage_dot_py(env.host)
    run('{0} flush --noinput'.format(manage_py))


def create_session_on_server(email):
    manage_py = _get_manage_dot_py(env.host)
    session_key = run('{command} create_session {email}'.format(
        command=manage_py,
        email=email
    ))
    print(session_key)
