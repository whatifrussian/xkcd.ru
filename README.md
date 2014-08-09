## Prepare

```
git clone https://github.com/whatifrussian/xkcd.ru.git
cd xkcd.ru
cp settings_local.py.template settings_local.py
./bin/random_key.py     # generate SECRET_KEY
edit settings_local.py  # change ADMINS and SECRET_KEY
cp urls_local.py.template urls_local.py
./manage.py syncdb
```

## Update from old versions

Database scheme changed, so if you have not clean installation, you need to
perform (for sqlite3):

```
sqlite3 xkcd.db < 'ALTER TABLE main.comics_comics ADD comment_title text NOT NULL DEFAULT "";'
```

Maybe Django can update database scheme itself, but I don’t try.

## Run

For debug and testing purposes:

```
./manage.py runserver
```

Look at:
- [http://localhost:8000]
- [http://localhost:8000/login]
- [http://localhost:8000/admin]
- [http://localhost:8000/add]

## Deploy

We consider nginx + uwsgi + django couple. Install they first.

Note: I don’t like package manager avoiding, so install these three packages
into system using emerge (Gentoo package manager). If you prefer `virtualenv`
or `pip` or something like, try it. But I will describe configuration as well
as all needed packages installed info system.

### xkcd.ru settings

Move repo root to `/var/www/xkcd.ru`. Recursively change directory owner to
your webserver user:group ('nginx:nginx' in my case).

Keep im mind set `DEBUG` in `settings_local.py` to `False` after testing your
deployment.

Run `./manage.py collectstatic` in repo directory for collecting Django static
files into `static` directory (virtually now only `static/admin` directory
will be added). Nginx will be directly serve it.

### Nginx settings

Let’s see `deploy/nginx.conf` file in this repo. This is slighly edited
standart Gentoo nginx configuration file, changed only in `server` section. It
assume that `xkcd.ru` directory (repo root) placed into `/var/www/`. You can
copy file entirely or adopt `server` section for your preferences.

Nginx just serve static (and media) data and appeal to uwsgi (via Unix socket)
for processing other queries.

### uwsgi settings

Let’s see `deploy/uwsgi.xkcd.ru`. In Gentoo you can simply do:

```
cp deploy/uwsgi.xkcd.ru /etc/conf.d/
cd /etc/init.d/
ln -s uwsgi uwsgi.xkcd.ru
cd -
/etc/init.d/uwsgi.xkcd.ru start
```

Otherwise you can export all these variables and simply run

```
uwsgi --master --daemonize ${UWSGI_LOG_FILE} ${UWSGI_EXTRA_OPTIONS} --socket ${UWSGI_SOCKET} --processes ${UWSGI_PROCESSES} --pidfile /var/run/uwsgi_xkcd.ru/xkcd.ru.pid
```

Of course you can use start-stop-daemon or it’s wrapper as well as wrappers from uwsgi package from your distro.

Note: I use Python 3.4 as default, so use 'python34' plugin. And one more non-trivial detail: '--plugin python3X' option MUST placed before '--wsgi-file=wsgi.py' option.
