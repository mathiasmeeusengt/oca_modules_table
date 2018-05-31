CLI
###

This page is intended for developers. Here is explained what you can / need to do in a CLI.


Start the application
=====================
To start the application follow the steps below:

#. Navigate to the directory where <app_name>.py is located
#. Enter ``venv\Scripts\Activate`` to start the virtual environment
#. Set the FLASK_APP environment variable:
    #. On Linux: ``export FLASK_APP=<app_name>.py``
    #. On Windows: ``set FLASK_APP=<app_name>.py``
#. Enter ``flask run``

The application should now be running.

To stop the application, press ``ctrl + c``. If this does not immediately stop the application, perform an action
(like refreshing) in a browser.


Start a python shell
====================
In a python shell you can test out snippets of code. Python files need to be imported in this shell before they can
be used.

To enter the python shell, instead of performing step 4 of **Start the application**, enter ``flask shell``.
Now it's possible to enter python code in your CLI.

To exit the shell, simply press ``ctrl + z``.

Create or update database schema
================================
When there is no database present, an extra command must be entered to create it.
Follow the first three steps from **Start the application** and then the steps below:

#. Enter ``flask db init`` to initialise the database (based on the models.py file)
#. Enter ``flask db migrate`` to create or overwrite the migration script
#. Enter ``flask db upgrade`` to apply the migration script to the database.

When there is an existing database that needs an update, because models.py is changedn simply input steps 2. and 3.
from above.