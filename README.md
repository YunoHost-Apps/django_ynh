# django2ynh


Glue code to package django projects as yunohost apps.

This repository is:

* The Python package [django2ynh](https://pypi.org/project/django2ynh/) with helpers for integrate a Django project as YunoHost package
* A example [YunoHost Application](https://install-app.yunohost.org/?app=django2ynh) that can be installed


[![Integration level](https://dash.yunohost.org/integration/django2ynh.svg)](https://dash.yunohost.org/appci/app/django2ynh) ![](https://ci-apps.yunohost.org/ci/badges/django2ynh.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/django2ynh.maintain.svg)
[![Install django2ynh with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django2ynh)


Pull requests welcome ;)


## Features

* SSOwat integration (see below)
* Helper to create first super user for `scripts/install`
* Run Django development server with a local generated YunoHost package installation (called `local_test`)
* Run `pytest` against `local_test` "installation"


### SSO authentication

[SSOwat](https://github.com/YunoHost/SSOwat) is fully supported:

* First user (`$YNH_APP_ARG_ADMIN`) will be created as Django's super user
* All new users will be created as normal users
* Login via SSO is fully supported
* User Email, First / Last name will be updated from SSO data


### usage

To create/update the first user in `install`/`upgrade`, e.g.:

```bash
./manage.py create_superuser --username="$admin" --email="$admin_mail"
```
This Create/update Django superuser and set a unusable password.
A password is not needed, because auth done via SSOwat ;)

Main parts in `settings.py`:
```python
from django2ynh.secret_key import get_or_create_secret as __get_or_create_secret

# Function that will be called to finalize a user profile:
YNH_SETUP_USER = 'setup_user.setup_project_user'

SECRET_KEY = __get_or_create_secret(FINAL_HOME_PATH / 'secret.txt')  # /opt/yunohost/$app/secret.txt

INSTALLED_APPS = [
    #...
    'django2ynh',
    #...
]

MIDDLEWARE = [
    #... after AuthenticationMiddleware ...
    #
    # login a user via HTTP_REMOTE_USER header from SSOwat:
    'django2ynh.sso_auth.auth_middleware.SSOwatRemoteUserMiddleware',
    #...
]

# Keep ModelBackend around for per-user permissions and superuser
AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',  # AxesBackend should be the first backend!
    #
    # Authenticate via SSO and nginx 'HTTP_REMOTE_USER' header:
    'django2ynh.sso_auth.auth_backend.SSOwatUserBackend',
    #
    # Fallback to normal Django model backend:
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = None
LOGIN_URL = '/yunohost/sso/'
LOGOUT_REDIRECT_URL = '/yunohost/sso/'
```


## local test

For quicker developing of django2ynh in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/YunoHost-Apps/django2ynh.git
~$ cd django2ynh/
~/django2ynh$ make
install-poetry         install or update poetry
install                install project via poetry
update                 update the sources and installation and generate "conf/requirements.txt"
lint                   Run code formatters and linter
fix-code-style         Fix code formatting
tox-listenvs           List all tox test environments
tox                    Run pytest via tox with all environments
pytest                 Run pytest
publish                Release new version to PyPi
local-test             Run local_test.py to run the project locally
local-diff-settings    Run "manage.py diffsettings" with local test

~/django2ynh$ make install-poetry
~/django2ynh$ make install
~/django2ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`


## Backwards-incompatible changes

### v0.2.0

The project was renamed!

* PyPi package name is now: `django2ynh`
* YunoHost app name is now: `django2ynh_ynh`

See also: [pull #13](https://github.com/YunoHost-Apps/django_ynh/pull/13)


## history

* [compare v0.2.0...master](https://github.com/YunoHost-Apps/django2ynh/compare/v0.2.0...master) **dev**
  * rename `django_ynh` to `django2ynh`
  * tbc
* [v0.1.5 - 19.01.2021](https://github.com/YunoHost-Apps/django2ynh/compare/v0.1.4...v0.1.5)
  * Make some deps `gunicorn`, `psycopg2-binary`, `django-redis`, `django-axes` optional
* [v0.1.4 - 08.01.2021](https://github.com/YunoHost-Apps/django2ynh/compare/v0.1.3...v0.1.4)
  * Bugfix [CSRF verification failed on POST requests #7](https://github.com/YunoHost-Apps/django2ynh/issues/7)
* [v0.1.3 - 08.01.2021](https://github.com/YunoHost-Apps/django2ynh/compare/v0.1.2...v0.1.3)
  * set "DEBUG = True" in local_test (so static files are served and auth works)
  * Bugfixes and cleanups
* [v0.1.2 - 29.12.2020](https://github.com/YunoHost-Apps/django2ynh/compare/v0.1.1...v0.1.2)
  * Bugfixes
* [v0.1.1 - 29.12.2020](https://github.com/YunoHost-Apps/django2ynh/compare/v0.1.0...v0.1.1)
  * Refactor "create_superuser" to a manage command, useable via "django2ynh" in `INSTALLED_APPS`
  * Generate "conf/requirements.txt" and use this file for install
  * rename own settings and urls (in `/conf/`)
* [v0.1.0 - 28.12.2020](https://github.com/YunoHost-Apps/django2ynh/compare/f578f14...v0.1.0)
  * first working state
* [23.12.2020](https://github.com/YunoHost-Apps/django2ynh/commit/f578f144a3a6d11d7044597c37d550d29c247773)
  * init the project


## Links

* Report a bug about this package: https://github.com/YunoHost-Apps/django2ynh
* YunoHost website: https://yunohost.org/
* PyPi package: https://pypi.org/project/django2ynh/

These projects used `django2ynh`:

* https://github.com/YunoHost-Apps/pyinventory_ynh
* https://github.com/YunoHost-Apps/django-for-runners_ynh

---

# Developer info

## package installation / debugging

Please send your pull request to https://github.com/YunoHost-Apps/django2ynh

Try 'main' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/django2ynh/tree/master --debug
or
sudo yunohost app upgrade django2ynh -u https://github.com/YunoHost-Apps/django2ynh/tree/master --debug
```

Try 'testing' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/django2ynh/tree/testing --debug
or
sudo yunohost app upgrade django2ynh -u https://github.com/YunoHost-Apps/django2ynh/tree/testing --debug
```

To remove call e.g.:
```bash
sudo yunohost app remove django2ynh
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps django2ynh
yunohost backup list
archives:
  - django2ynh-pre-upgrade1
  - 20201223-163434
yunohost app remove django2ynh
yunohost backup restore 20201223-163434 --apps django2ynh
```

Debug installation, e.g.:
```bash
root@yunohost:~# ls -la /var/www/django2ynh/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/django2ynh/
total 58
drwxr-xr-x 5 django2ynh django2ynh   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 django2ynh django2ynh  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 django2ynh django2ynh    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 django2ynh django2ynh  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 django2ynh django2ynh  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 django2ynh django2ynh    6 Dec  8 08:37 venv
-rw-r--r-- 1 django2ynh django2ynh  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 django2ynh django2ynh 4737 Dec  8 08:39 django2ynh_demo_settings.py

root@yunohost:~# cd /opt/yunohost/django2ynh/
root@yunohost:/opt/yunohost/django2ynh# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/django2ynh# ./manage.py check
django2ynh v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='django2ynh_demo_settings'
PROJECT_PATH:/opt/yunohost/django2ynh/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/django2ynh
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/django2ynh/django2ynh.log
root@yunohost:~# cat /etc/systemd/system/django2ynh.service

root@yunohost:~# systemctl reload-or-restart django2ynh
root@yunohost:~# journalctl --unit=django2ynh --follow
```


