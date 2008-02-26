#!/usr/bin/env LD_LIBRARY_PATH="/pub/home/myths/local/lib/mysql" /pub/home/myths/local/bin/python2.4
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/pub/home/myths/dj")
sys.path.insert(0, "/pub/home/myths/misc")

# Switch to the directory of your project. (Optional.)
#os.chdir("/pub/home/myths/dj/mysite")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "misc.settings"
os.environ['LD_LIBRARY_PATH'] = "/pub/home/myths/local/lib/mysql"

from django.core.servers.fastcgi import runfastcgi
#help(runfastcgi)

runfastcgi(["method=threaded", "daemonize=false"])


