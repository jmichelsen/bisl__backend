Deploying with heroku:

git push heroku master
heroku run sh
heroku run python manage.py collectstatic --noinput
heroku run python manage.py migrate
heroku run gunicorn config.wsgi

For heroku docker deploy, see x

