from invoke import task

# Workaround for homebrew installation of Python
# (https://bugs.python.org/issue22490)
import os
os.environ.pop('__PYVENV_LAUNCHER__', None)


@task
def test(ctx):
    ctx.run('pipenv run flake8')
    ctx.run('pipenv run coverage run manage.py test')
    ctx.run('pipenv run python functional_tests.py')
