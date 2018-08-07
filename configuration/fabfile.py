import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/patjouk/testing_goat.git"
SITE_FOLDER = f"/home/{env.user}/sites/{env.host}"

def deploy():
    run(f"mkdir -p {SITE_FOLDER}")
    with cd(SITE_FOLDER):
        _get_latest_source()
        _pipenv_install()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")

def _pipenv_install():
    run("pipenv install")

def _create_or_update_dotenv():
    with cd(SITE_FOLDER + "/superlists"):
        append(".env", "DEBUG=False")
        append(".env", "ALLOWED_HOSTS={env.host}")
        append(".env", "SITENAME={env.host")
        current_contents = run("cat .env")
        if "DJANGO_SECRET_KEY" not in current_contents:
            new_secret = "".join(random.SystemRandom().choices(
                'abcdefghijklmnopqrstuvwxyz0123456789', k=50
            ))
            append(".env", f"DJANGO_SECRET_KEY={new_secret}")

def _update_static_files():
    run("pipenv run python manage.py collectstatic --noinput")

def _update_database():
    run("pipenv run python manage.py migrate --noinput")
