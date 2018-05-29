Source Code
###########

This page is intended for developers. Here is explained what all the functions are and where code needs to be changed
in certain events (eg.: adding a new odoo version).

Database model
==============

The image below shows how the database looks like, it has two objects, Repository and Module.
One repository can have multiple modules, but one module cannot have multi repositories

.. image :: diagram.png


Python files
============

This section explains what each function in each .py file does. The names of the titles are not identical to the files,
but strongly resemble them.

Routes
------

This file contains all the 'routes' of the application. Routes are functions that specify what logic must be executed
when the client requests a URL. The routes in this application are usually built in the same way:


#. ``@app.route('/name_page/<variable>, methods=['GET', 'POST'])``
#. ``def name_page(variable):``
#. ``# body``
#. ``return render_template('name_page.html', 'title', var1=var1, var2=var2, ...)``

1. Specify the URL of the page along with optional variables and which methods this page is allowed to use
2. Actual definition of the function, with or without variable(s)
3. The code that runs when this page is accessed
4. A return statement that either returns a template or redirects to another route

First is a URL that will also be shown in the url-bar of your browser. If a variable needs to be passed along to this
page, it's possible to add this to the URL ``/name_page_to_visit/<variable>``. The greater than and lesser than
need to stay, this way the program knows it's a variable and not a solid part of the url.
If there is no variable in the URL, the actual function is created with empty parentheses. When one or more variables
are placed in the URL, they need to be placed in the parentheses. These variables can then be used in the body.
At the end of the body is a return statement with
a ``render_template('name_page.html', 'title', var1=var1, var2=var,...)``. This renders a html page with jinja2.
The variables passed along after the title can be used in the template.

The body can also contain an if-statement with a ``validate_on_submit()``. This is a function from flask-wtforms.
This if-statement is true when a button from a form on the page is pressed and no errors are raised.
There's either some code to be run or a function call behind this if-statement. If the program has run through the
entire body, it comes upon a separate return-statement on the same level as the if-statement. This return either has a
return_template or a ``return redirect(url_for('name_page', var1=var1,...))``. This redirects the browser to the page
that matches the name inside the parentheses.


Regular Functions
-----------------
This section will give a bit of explanation for the functions in 'functions.py'.

.. note::

    The Repository object from the local database has it's name under '.repository', so Repository.repository will get
    the name. The Repository object obtained from the GitHub API has it's name under ".name", making it Repository.name
    to get the name.


update_repositories()
*********************

*Parameters: None*

This function updates the entire database. It uses PyGitHub, a python library used to access the GitHub API v3.
First it gets all the repositories from the user OCA, then it loops for every repository that is returned. It starts
by checking if the Repository exists, if it does, it will update the description and move on. If the repository does
not exist in the database, a new record will be made. The name (repository) and description will be saved and
in_scope will be set to 'False'.
Now that the repository is updated/created, the function moves on to other functions that will update the repositories'
modules, and nearly every field of each module.
The functions are:

* ``update_modules(repository)``
* ``count_modules(repository)``
* ``get_installable_and_get_readme(repository)``
* ``get_readme_repository(repository)``

Every 5 repositories, a counter will print the number of repositories already updated. Just to have a little feedback.


update_single_repository(repository)
************************************

*Parameter: string(repository name)*

This function works exactly the same as ``update_repositories()``, with one difference. It only updates one repository,
instead of all of them. This can be useful when a user wants to be sure that the latest version is present on the
database. Naturally, the counter is left out.


update_modules(repository)
**************************

*Parameter: github.Repository.Repository(repository)*

This function is used to get the modules of a repository.  First it calls on another function,
``get_tree_hashes_per_repo(repo)`` to get the hashes from the trees (= Github branches). Then, every item in the
returned list is sent as a parameter for another PyGitHub function, ``get_git_tree(repository_hash)``. This returns
a lot of items from the API, not all of which are needed. Every item is filtered on the type of tree,
``list_item.type == 'tree'`` means it is a subdirectory and most likely a module that we want to get. Then it is checked
if the module is already in the database. If this is not the case, a new record is make and it's name and the repository
it is part of are saved in the database.

Before exiting this function, one last other function is called,
``url_test_module(list_item.path)``. The ``.path`` value is the name of the module.


get_tree_hashes_per_repo(repository)
************************************

*Parameter: github.Repository.Repository(repository)*

This function pulls the Tree (=branch) hashes from a repository using the Git references. This is done with a function,
``get_git_refs()``, from the PyGitHub library. The returned PaginatedList is then filtered based on the Odoo versions,
*refs/heads/x.0*, where x is the version. The hashes of the filtered list items are saved in a list which is then
returned for use in another function.


url_test_module(module)
***********************

*Parameter: string(module name)*

For every (relevant(= 8, 9, 10 ,11))Odoo version, a URL is prepared and filled in by the module name and linked
repository. This URL should lead to the GitHub page of the module, if it exists. To check this, a function is called,
``check_if_url_valid(url)``.


check_if_url_valid(url)
***********************

*Parameter: string(url)*

The url is checked on what statuscode is returned when accessed. If this code is lower than 400, it means the page,
and thus the module, exist. For each version where the page exists, an 'X' is saved to the database. If the module
does not exist, it is saved as '-'.


check_if_readme_exists(url)
***************************

*Parameter: string(url)*

The url is checked on what statuscode is returned when accessed. If this code is lower than 400, it means the
readme-file of this particular module exists. For each version where the readme exists, 'readme' is saved to the
database. If the readme does not exist, a '-' will be saved.


count_modules(repository)
*************************

*Parameter: github.Repository.Repository(repository)*

This function counts how many modules there are in a repository, per version. This is done by a join-query between
between all modules with the same Repository FK ``Module.repo_name`` and every module that exists (= has a 'X' in the
database).


get_installable_and_get_readme(repository)
******************************************

*Parameter: github.Repository.Repository(repository)*

This function checks if the module is installable and in the same breath gets the text of the readme.
This is done by using two other functions: ``get_installable(...)`` and ``get_readme_module(...)``. The reason these
functions aren't used separately is because now the database needs to be queried only once.

get_installable(repository, module, version)
********************************************

*Parameters: github.Repository.Repository(repository), app.Models.Module(module), string('x.0')*

This function checks if the module is installable. This is done by getting the files of a module from GitHub. When the
files are returned by the API, the function checks if either 'openerp' or 'manifest' exist and gets the content from
that file. Then it searches for the words "installable: True". Because the text is converted from .rst to .txt, some
bits of the syntax cause for some weird conversions. This is the reason that there's some space between the expected
place of 'installable:' and 'True'. The function returns a string 'True' or 'False' depending on if it finds
'Installable: True', even with some weird characters in between.


get_readme_module(module, version_x)
************************************

*Parameters: app.Models.Module(module), string('x.0')*

This function uses a URL to get the raw content of the readme file, which is saved for the correct version of the
module.

uses ``check_if_readme_exists(url)``


get_readme_repository(repository)
*********************************

*Parameter: github.Repository.Repository*




search_module_f(...)
********************
*Variables between parentheses: form_module_data, form_select_version_data, form_search_readme_data,
form_installable_bool_data.*

*Parameters: string(search keyword), string(selected version), bool(search_readme), string(selected option)*





search_repository_f(...)
************************
*Variables between parentheses: form_repository_data, form_bp_data, form_in_scope_data*

*Parameters: string(search keyword), string(selected option), string(selected option)*




PyGitHub API
------------




Version (specific) functions
----------------------------





Forms
-----





Maintenance
===========



