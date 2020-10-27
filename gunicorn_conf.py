# /path-to-your-project/gunicorn_conf.py
bind = '0.0.0.0:8080'
pidfile = 'pid.py'
worker_class = 'sync'
loglevel = 'debug'
accesslog = 'access.log'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  'error.log'
