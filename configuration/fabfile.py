import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
from fabric.operations import reboot

REPO_URL = "https://github.com/patjouk/testing_goat.git"


env.roledefs = {
    "staging": ["testing-goat-staging.justhiding.org"],
    "prod": ["testing-goat.justhiding.org"],
}


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _pipenv_install()
        with cd("./superlists"):
            _create_or_update_dotenv()
        _update_static_files()
        _update_database()
    print("Rebooting now!")
    _reboot_instance()


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
    append(".env", "DEBUG=False")
    append(".env", f"ALLOWED_HOSTS={env.host}")
    append(".env", f"SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(
            random.SystemRandom().choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50)
        )
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")


def _update_static_files():
    run("pipenv run python manage.py collectstatic --noinput")


def _update_database():
    run("pipenv run python manage.py migrate --noinput")


def _reboot_instance():
    reboot(command="shutdown -r +0")
