How-to
######

*This page will explain how to perform certain actions (eg.: update a repository) in the
application.*


Look up a repository
====================
You can look up a repository on a couple of pages: **Full table**, **Search repository** and
**Table per version**.

In **Full table**, you see an overview of every repository in the database. You can use the
search-function of your browser to look for a repository, or use the application's search-page to
filter based on some properties.

On the page **Search repository**, you can enter a keyword to look in a more specific way. There's
also the option to set a few properties, in scope, BP and Select version. Along with the keyword, this will affect
which repositories you will see in the search results. Select version does not alter which repositories will be shown,
and is only used to display the right modules if you click on the name of the repository in the results table.
Every field/option is optional to fill in, and leaving everything at the default value will result in a table
that is the same as **Full table**.

And lastly you can use the page **Table per version**. After you've selected a version, the table will
only show repositories that have modules in that specific version. So if the repository has modules,
but none exist in the selected version, it is not shown.


Look up a module
================
A module can be looked up in two ways: via the **Search Module** page or from any repository page.

The **Search Module** page works mostly the same as the repository one. Visually there will be a
few differences. The options are different and there's a checkbox too.

.. note::

    The search function works as long as at least one option or filter is selected/filled in.
    Except: "Select Version" and "Installable: All Results". Installable: True / False do work on their own.

Now all the different filters and options will be explained.

**Module** is a text field where you can input a keyword. When the search-button is pressed, this keyword will
be compared to the names of modules. Modules that match the keyword, and other options that are selected,
will be shown in the results table.

The **Select Version** field selects in which version you want to look for modules. This field has a default value
selected and can be changed to a different selection, but it cannot be unselected.

The **Installable** filter will select what the installable property of the modules is. It's possible to choose from
True, False or both (All results). Again, if you select True or False, this is enough to perform a search on,
this is not the case if "All results" is still selected. (If another filter or option is filled in, All results
will work.)

**Customer** and **Vertical** are two separate fields, but work the same. Here you can fill in the name of a
Customer and Vertical, in their respective textboxes. Any modules matching the entered text will show up in the results.
They always work, either if one field is filled in, or both.

**Search in Readme**, last but not least. If this checkbox is checked, the search will look in readme files
of modules **instead** of the names for the entered text in "Module".

It is possible to look up multiple words at once, if "Search in Readme" is checked. The words will be searched for in
the order that they were inputted. If no results are returned, try searching with less words to make it easier to find
an exact match.

.. note::

    If "Search in Readme" is checked, the keyword(s) inputted in "Module" will no longer look for the name of
    the modules, but only in the readme.

Another way to look up a module is via any table that also shows repositories. When you are looking
at such a table, simply click on a repository's name. This will take you to one of two tables.
Either the **Full table** variant, or the **Table per version** one. The difference is that the
Full table shows an overview for all versions. Whereas the Table per version only shows modules
for a preselected version with additional columns providing more information.


Go back to the previous screen
==============================
In order to go back to the previous screen, simply press the "Back" button of your browser. This
should take you out of your current page, back to the previous one.

.. warning::

    It is possible that by pressing Back after filling in and submitting a form ,
    the submitted data will not be written to the database. (Except with search-forms)

When pressing "Back" after performing a search, you will be taken to the form, with all the filters and options
filled in like they were.

Try to avoid using the "Back" button when you've written a review or edited a repository.


Update
======

This section explains how to update either the whole database or just a single repository.
As you shouldn't need these buttons/links very often, all the update actions are confined
to the page **Full table** to keep clutter in other tables, which display more information, to a minimum.


Update everything
-----------------

To update the whole database, visit the **Full table** page. Scroll all the way to the bottom and
click the button ``Update Database``. The application will now run through every record and update
it if necessary. If new repositories are found, they will be added to the database.

..  note::

    This will take a very long time.

You can interrupt it, but it cannot continue from
where it left off. If you want to update again, you'll have to start over.


Update one repository
---------------------

If you do not wish to update the entire table, or you're pressed for time for a couple of
repositories: You can update a single repository. To do this, you need to go to **Full table**.
In the last column of any repository, there's a link ``Update``. When clicked,
the application will run a mini-version of the ``Update Database``-button.

.. note::

    Depending on the numbers of modules in the repository, the time this takes can vary.


Edit repository
===============

*Affects Repository: In scope, BP, employee*

If you edit a repository, you can specify if it's ``in scope`` of the company, which ``BP`` it's
linked to, and an ``employee`` who has experience with this repository. To do this, you can go
to any repository table: **Full Table**, **Search Repository**'s search results
or **Table per version**. Usually in the last column, there's clickable
text ``Edit Repository``. Clicking on this will take you to a form. Here you can input or
select the above mentioned items.


Edit module
===========

*Affects Module: customer, vertical*

To edit a module you can click on ``Edit Module`` in **Search Module**'s results table or from
the module table in **Table per Version**. On this page you can fill in the **Customers** and **Verticals**
this module is used in. You can enter multiple names at once, given that they are separated by a space.
If the name contains a space, replace the space in the name by an underscore '_'.  There's also the option
of deleting previously added customers and/or verticals. Simply check the desired checkboxes. If you've
filled in the textfields and checked the checkboxes, it will first clear out the old customers and
verticals, then add the new ones. Once you filled in what you wanted to fill in, press the Save Changes
button to write the changes to the database.


Edit rating and review
======================

*Affects Module: rating, review*

When you have a version specific module table (so not from Full Table) on your screen, you can click
"Write review". This clickable link is in the last column of a module record. Clicking on
it will take you to a form, here you can assign a number and write a review. Optionally, you can
check a checkbox to delete previous reviews. If this is left unchecked, new reviews will be pasted
behind existing ones, separated by '||'. When de module is graded and a review is written, click on
'Place review'. This will save the review. New scores are not added to old scores,
and only the last score will be shown.
