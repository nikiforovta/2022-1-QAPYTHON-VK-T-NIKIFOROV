import os
import signal
import subprocess
import sys
import time
from copy import copy

from requests.exceptions import ConnectionError

from fixtures import *

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))
python_root = os.path.join(repo_root, '../venv/Scripts/python.exe') if sys.platform.startswith('win') else 'python3'


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 10:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 10s!')


def app_config():
    app_path = os.path.join(repo_root, 'application', 'app.py')

    env = copy(os.environ)
    env.update({
        'APP_HOST': settings.APP_HOST,
        'APP_PORT': settings.APP_PORT,
        'AGE_HOST': settings.STUB_HOST,
        'AGE_PORT': settings.STUB_PORT,
        'SURNAME_HOST': settings.MOCK_HOST,
        'SURNAME_PORT': settings.MOCK_PORT
    })

    app_stderr = open(os.path.join(repo_root, 'logs', 'app_stderr.log'), 'w+')
    app_stdout = open(os.path.join(repo_root, 'logs', 'app_stdout.log'), 'w+')

    app_proc = subprocess.Popen([python_root, app_path], stderr=app_stderr, stdout=app_stdout, env=env)
    wait_ready(settings.APP_HOST, settings.APP_PORT)

    return app_proc, app_stderr, app_stdout


def stub_config():
    stub_path = os.path.join(repo_root, 'stub', 'flask_stub.py')

    env = copy(os.environ)
    env.update({
        'STUB_HOST': settings.STUB_HOST,
        'STUB_PORT': settings.STUB_PORT,
    })

    stub_stderr = open(os.path.join(repo_root, 'logs', 'stub_stderr.log'), 'w+')
    stub_stdout = open(os.path.join(repo_root, 'logs', 'stub_stdout.log'), 'w+')

    stub_proc = subprocess.Popen([python_root, stub_path], stderr=stub_stderr, stdout=stub_stdout, env=env)
    wait_ready(settings.STUB_HOST, settings.STUB_PORT)

    return stub_proc, stub_stderr, stub_stdout


def mock_config():
    from mock import flask_mock
    flask_mock.run_mock()

    wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        config.app_proc, config.app_stderr, config.app_stdout = app_config()
        config.stub_proc, config.stub_stderr, config.stub_stdout = stub_config()
        mock_config()


def stop_process(proc):
    if sys.platform.startswith('win'):
        proc.send_signal(signal.CTRL_C_EVENT)
    else:
        proc.send_signal(signal.SIGINT)
    proc.wait()


def app_unconfig(config):
    stop_process(config.app_proc)

    config.app_stderr.close()
    config.app_stdout.close()


def stub_unconfig(config):
    stop_process(config.stub_proc)

    config.stub_stderr.close()
    config.stub_stdout.close()


def mock_unconfig():
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_unconfigure(config):
    app_unconfig(config)
    stub_unconfig(config)
    mock_unconfig()
