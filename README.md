Deploying with heroku:

git push heroku master
heroku run sh
heroku run /bisl/bin/python manage.py collectstatic --noinput
heroku run /bisl/bin/python manage.py migrate
heroku run /bisl/bin/gunicorn config.wsgi

For heroku docker deploy, see x

