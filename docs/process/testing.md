# Bisl Testing

Testing is an important part of maintaining a project. We focus on building automated testing for models, forms and other classes with commonly-used and/or vital interfaces.

## Process

**Note:** Be sure you run the tests through docker to be as close to production as possible.

1. We use docker-compose to execute Django's test commands to execute tests.  The only adjustment is you will need to point the test runner at your test settings file.

        $ docker-compose up bisl_test

2. To prevent unnecessary reporting on multiple failed tests, you can call the test runner and add the `--failfast` param to it

        $ docker-compose run --rm bisl python manage.py test --settings=config.settings.test --failfast --noinput
        
3. You can force tests of a single app, file or test case by using Python's `package.module.class` syntax.

        $ docker-compose run --rm bisl python manage.py test --settings=config.settings.test --failfast --noinput some.package.tests.test_something.SomeTest

4. All tests must pass before creating a merge request. 

Using Coverage
--------------
1. Code coverage describes how much source code has been tested, and shows which lines of code are or are not covered by tests. To run tests with the coverage tool, use the coverage run command on manage.py. This is similar to the testing process above, and uses the same settings.

        $ docker-compose run --rm bisl coverage run manage.py test --settings=config.settings.test --noinput

2. View the coverage report from the terminal.

        $ docker-compose run --rm bisl coverage report

3. When examining the coverage report, pay attention to code that has low test coverage. Refer to the 'Should this be tested' section in the 'best_practices.md' documentation to help determine whether a block of code that is missing a test should have a test written for it.

4. If you determine code does *not* require test coverage, be sure it is appropriately skipped using either `.coveragerc` entries or a manual `# pragma: no cover` comment. 
