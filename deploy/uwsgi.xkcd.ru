UWSGI_SOCKET=/tmp/uwsgi.xkcd.ru.sock
UWSGI_THREADS=0
UWSGI_PROGRAM=
UWSGI_XML_CONFIG=
UWSGI_PROCESSES=1
UWSGI_LOG_FILE=/var/log/nginx/uwsgi.xkcd.ru.log
UWSGI_CHROOT=
UWSGI_DIR=/var/www/xkcd.ru
UWSGI_USER=nginx
UWSGI_GROUP=nginx
UWSGI_EXTRA_OPTIONS="--plugin python34 --wsgi-file=wsgi.py"
