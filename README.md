
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d5d58c94c2154bde8c34608e4c9c5611)](https://app.codacy.com/app/jmichelsen/bisl__backend?utm_source=github.com&utm_medium=referral&utm_content=jmichelsen/bisl__backend&utm_campaign=Badge_Grade_Settings)

Deploying with heroku:

git push heroku master
heroku run sh
heroku run python manage.py collectstatic --noinput
heroku run python manage.py migrate
heroku run gunicorn config.wsgi

For heroku docker deploy, see x

