# Programming Style Guide

The focus of this style guide is to keep consistency within the developer team. Most of the style guide will be inherited from Python's style guide, [PEP-8](https://www.python.org/dev/peps/pep-0008/), and [Django's Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

## PEP-8
This is a highlight of the important pieces of the PEP-8 document. You should still read the whole document to familiarize yourself with all rules. [PEP-8](https://www.python.org/dev/peps/pep-0008/)

- Two good reasons to break a particular rule:
    - When applying the rule would make the code less readable, even for
      someone who is used to reading code that follows the rules.
- Use 4 spaces per indentation level. Not a tab character.
- Limit all lines to a maximum of 100 characters.
- Imports should be grouped as:
    
        import python_library1
        from python_library2 import foo
        
        import third_party_library1
        from third_party_library2 import bar
        
        import local_package1
        from local_package2 import baz

- Imports should use the parenthesis style import versus newline character when imports span multiple lines

        from local_package3 import (
            Foo, Bar, Baz,
        )

- Avoid extraneous whitespace in the following situations:
    - Immediately inside parentheses, brackets or braces.
    - Immediately before a comma, semicolon, or colon.
    - Immediately before the open parenthesis that starts the argument list
      of a function call.
    - Immediately before the open parenthesis that starts an indexing or
      slicing.
- Use spaces around arithmetic, comparison and binary operators.
- Do not use spaces when around the assignment operator '=' when used to
  indicate a keyword argument or a default parameter value.
- Compound statements (multiple statements on the same line) are generally
  discouraged.

# Django's Coding Style
This is a highlight of the important pieces of the Django Coding Style. You should still read the whole document to familiarize yourself with all rules. [Django's Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/).

- In Django template code, put one (and only one) space between the curly brackets and the tag contents.
- In Django views, the first parameter in a view function should be called request.
- Field names should be all lowercase, using underscores instead of camelCase.

# Docstrings Coding Style
Document all defined classes and methods using the standard ReStructuredText Style. [RST in Python](http://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html)

Example:

```python
def my_method(foo, bar, baz):
    """
    This method will take the voodoo and cause the magic, while removing the mystery.
    
    :param foo: The object for voodoo with magic
    :param bar: The order in which the mystery will be resolved
    :param baz: How the remaining voodoo will be converted to magic
    :return: All the magic
    """
    # Stuff happens here
```


# URL Routing
Name every URL route in Django. You should always be able to run reverse routing on the name of the URL.

Use hyphens to separate words for the URL routes (including namespace routes). Use underscores to represent the same separation in route and namespace names. For example, the URL r"^my-clients/$" should have the name "my_clients". Match the routes and their names as close as possible like the example. This will make it so if that my clients example was in an "accounts" app, someone
would expect to be able to use the reverse name of "accounts:my_clients" to get to "/accounts/my-clients".

If you have an ID or slug in the URL route, just skip that section in the naming of the route. For example, r'^(?P<slug>[\w\-]+)/edit/$' should map to "edit". However, in cases where there is nothing after the ID or slug, r'^(?P<slug>[\w\-]+)/$' needs to map to something. In this case, it is usually labeled a "view" page, this one would make sense to call it "view".

Each application should use Django URL namespaces to scope their urls.

If managing models, create namespaces for each model. For example, in the jobs app, the Job model should have it's own namespace for managing Job in the jobs namespace (i.e. jobs:job:index).

Within model routing, the following is the standard structure for working with those URL routes. It is close to RESTful routing, with a few differences.

<table>
    <tr>
        <td>Type</td><td>URL</td><td>Method</td><td>Description</td>
    </tr>
    <tr>
        <td>index</td><td>/</td><td>GET</td><td>List model records</td>
    </tr>
    <tr>
        <td>create</td><td>/</td><td>POST</td><td>Creates model record</td>
    </tr>
    <tr>
        <td>view</td><td>/(id|slug)/</td><td>GET</td><td>Views model record</td>
    </tr>
</table>
If you are adding extra pages/view to model routes, just create them for "/(id|slug)/(new route)/". For example, if you are within the jobs namespace and want to show all the jobs, use this full route "/jobs/{ job-id }/".

# Git usage
Master branch is always considered live. Never push to master (it's protected), if it is not ready for live at that moment.

Create your own remote branch on your github repo for all commits. Then create a Merge Request on Github.

If the branch is related to a ticket, the branch name should just be the referenced ticket name (e.g. UP-123_update_recall_process).

# Testing
Each class being tested should include tests for each condition in each method.

Try to keep methods and functions as specific (within reason) to it's purpose. If the functionality starts getting north of 10 lines of code, then some refactoring may need to be in store. This will keep the tests simple to write and maintain.

Never create a pull request if any of the tests are failing.

If a bug is found, you should first build a test to replicate the cause of the bug. Then, write the code to pass that test, therefore fixing the bug.

# Database
Use the Django ORM whenever possible.  In the event that a raw SQL query is required, stick to SQL standards when building queries. Do not introduce queries that will not work in PostgreSQL.

When drafting/implementing data models, we will follow the Django's imposed conventions of tables, columns, indexes, etc. Here are some highlights of those imposed conventions:

- Database table name: { app name }_{ model name }
- Primary key: id
- Foreign key: { foreign model name }_id
- Character Set: utf8
- Collation: utf8_general_ci
- Timestamps: Use for every model, unless specific reason not to.
    - Create: created_at
    - Update: updated_at

# Models
Always include a docstring with a model, describing the intentions of the model and how the model relates to others.

If a field is required, define the default value as well.

Every model should have a `__str__()` method.

Furthermore, follow [Django model style guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style)

# Settings
Some examples of where settings should go in the settings directory:

- base.py
    - Project directory paths.
    - I18n and L10n settings.
    - Middleware settings.
    - Generic database config.

- dev.py
    - Some setting overrides from base.py that generically apply to dev environments.

- test.py
    - Some setting overrides from base.py that generically apply to test environments.

- prod.py
    - Some setting overrides from base.py that generically apply to production environments.
