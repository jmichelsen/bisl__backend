# Using Docker

Docker is the primary supported setup for development. This setup uses docker compose to build Docker containers for services, allowing the use of development, testing, and production configurations.

## SETUP

1. Install Docker, following the instructions for your system outlined in the Docker documentation.

	    https://docs.docker.com/install/#supported-platforms

2. Install Docker compose, following the instructions for your system outlined in the Docker documentation.

	    https://docs.docker.com/compose/install/#prerequisites

3. Navigate to the project directory. All docker-compose commands should be run from here.

        $ cd ~/projects/bisl/

4. Run Docker compose up from the docker directory. This will build the required images from the Dockerfile in this directory.

	    $ docker-compose up --no-start

5. You should now be able to run commands through the various services set up by docker-compose.

	    $ docker-compose run --rm <service_name> <command>

    If no command is specified, docker will run the default commands defined in the docker-compose file
    For example, running bisl will start the Django runserver on ip:port 0.0.0.0:8009
    
        $ docker-compose run bisl
        
    Navigate to 0.0.0.0:8009/common/health-check/ and verify the server is running properly.
    
    Try passing in a command, such as the manage.py help
    
        $ docker-compose run --rm bisl python manage.py --help
        
    Or try running the unit tests through Django directly
    
        $ docker-compose run --rm bisl python manage.py test --settings=config.settings.test --failfast --noinput
        
    You may need to run the migration scripts from time to time
    
        $ docker-compose run --rm bisl python manage.py migrate
    
6. An explanation of the command line parameters:
        
        --rm : (optional) removes the container when you are done using it
        --service-ports : (optional) exposes ports to your host machine, so that you can access the dev server from your browser, for example
        --use-aliases : (recommended) connects services together over the default docker network.

    Note: commands passed in by `run` override the command definitions that exist in the docker-compose.yml service definitions, including port definitions, whereas
    `docker-compose up` will use the definitions that exist in docker-compose.yml. PyCharm uses `docker-compose up` so services exist as defined.
