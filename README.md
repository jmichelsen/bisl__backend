![bisl logo](static/common/img/bisl_logo.png)

## Bisl
Bisl is an app for exploring the recipes created by Andrew Rea, aka Oliver Babish, through his Youtube channel, Binging with Babish

## Motivation
Often when cooking, it is difficult to look up recipes on the web or YouTube. This project was created to help fans of Binging with Babish have quick and native access to all of the Binging recipes right on their phone while cooking.

Furthermore, social features for saving and sharing recipes with friends would be nice to have.

Thus Bisl was born.

Oh, and the name Bisl comes from the Yiddish word that mean, "a little bit of something, a tiny piece"

## Build status

![CircleCI](https://img.shields.io/circleci/build/github/jmichelsen/bisl__backend?logo=circleci&style=for-the-badge&token=a03eab67c6f91209061f4e2d7f720e1fd6347ba2)
![Codacy grade](https://img.shields.io/codacy/grade/ec793dad8579484a8917626e98989507?logo=codacy&style=for-the-badge)
![Codacy coverage](https://img.shields.io/codacy/coverage/ec793dad8579484a8917626e98989507?logo=codacy&style=for-the-badge)

## Code style
This project strictly follows Python PEP8 and Django coding standards. In addition, industry best practices are followed closely. Read more about best practices and processes in the [project docs](https://github.com/jmichelsen/bisl__backend/tree/master/docs) 
 
## Screenshots
To be added

## Tech/framework used

<b>Built with</b>
 -  [Django](https://www.djangoproject.com/) for recipe management
 -  [Django REST Framework](https://www.django-rest-framework.org/) for the API
 -  [CircleCI](https://circleci.com/) for continuous integration and deployment
 -  [Heroku](https://heroku.com/) for hosting

## Continuous Integration ad Deployment
Info about how this is set up

## General Design (work in progress)
The general design of this app consists of several components; 
the Django app (standard models, views, forms, and templates), then the API using Django REST Framework,
and finally the Flutter app which consumes the API

Each component has different requirements so each one will be addressed on its own here and will include related user stories.

#### The Django App
The general design of the Django app is primarily as a web interface for admins to add content.
The app is strictly a read-only consumer of data that Admins create, as it applies to core data.

Outside of core data (recipes from Binging with Babish), users can favorite (star), comment, share,
and upload photos of their attempts of recipes to the app. This will all happen in the Flutter app, 
so will rely on the API having the capabilities to provide these actions to users.

##### Django web app user stories
 -  As an admin, I can create/update/delete recipes in the app/API
 -  As an admin, I can moderate comments
 -  As an admin, I can moderate images
 -  As an admin, I can PM users
 -  As an admin, I can make announcements

From the user stories, you can see that the majority of interactions with the Django webapp are
performed by admins, not standard users.

#### The API
The API needs to allow for the desired user actions, as well as handle authentication for the Flutter
app, and API requests. To handle authentication, the Django app needs to act as an Oauth2 provider.

##### API based user stories
 -  As a user, I can create an account and log in
 -  As a user, I can comment on recipes
 -  As a user, I can share recipes
 -  As a user, I can upload photos of recipes
 -  As a user, I can mark recipes as favorites
 -  As a user, I can see what recipes I have starred
 -  As a user I can create and modify my account

The user stories for the API must be heard in the context of API requests. These are not UIs that users
will see in the API themselves, but the API needs to provide the functionality for a UI to satisfy the stories

#### The Flutter app
The Flutter app will be where users interact with Bisl. Flutter is cross-platform, so this applies
to both iPhone and Android users. The Django web interface, for non-admins, will direct users to
download the native app for their desired platform.

##### Flutter based user stories
 -  As a user, I can create an account and log in
 -  As a user, I can comment on recipes
 -  As a user, I can share recipes
 -  As a user, I can upload photos of recipes
 -  As a user, I can mark recipes as favorites
 -  As a user, I can see what recipes I have starred
 -  As a user I can create and modify my account

The user stories here are the same as the API stories, but they apply here in the context of
the native app, UI, and actions. Users will consume data from, and produce data for the APIs.

## Installation
To run Bisl locally, pull the project and use the following `docker-compose` commands:
```bash
$ docker-compose up bisl
```

That will build the project from the Dockerfile, run migrations, and start the local web server. You can then access the project on host `http://0.0.0.0` and port `8009`:
```bash
http://0.0.0.0:8009/
```
## API Reference
To be added

## Tests
Tests can be run through docker-compose, like the project itself:
```bash
$ docker-compose run --rm bisl pytest
```

## Contribute
Contributions are always welcome! Please read the [contributing guideline](CONTRIBUTING.md) first.

![GitHub contributors](https://img.shields.io/github/contributors/jmichelsen/bisl__backend?logo=github&style=for-the-badge)

## Credits
Built by [Jesse Michelsen](https://github.com/jmichelsen), [Jmast](https://github.com/jmast02), [Clem](https://github.com/ClemSau)

## License
GNU General Public License v3.0

GNU GPLv3 © [Jesse Michelsen](https://github.com/jmichelsen)
