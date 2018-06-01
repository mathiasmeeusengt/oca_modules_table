Pages
#####

*This page will explain what information can be found on every page of the application.
The titles correspond with the pages in the menu of the application.*


Home
====

This is the homepage of the application. Here you can find a short explanation of every page.
There's not much else going on.


Search repository
=================

This page leads to a form which you can fill in to filter repositories based on inputted words and selections.
These filters are:

    * **Repository**: A word to search for the name of a repository
    * **In scope**: Select if the result is in the scope or not. A repository that is in scope, means that it's
      relevant for the company (eg.: l10n-brazil is probably not in the scope)
    * **BP**: Select a BP from the list
    * **Select version**: Select a version. This will not affect repository results, but enables clicking on a
      repository's name to show the modules of the correct version

The result will be a table similar to the one described in **Full Table** a bit below here.


Search module
=============

This page leads to a form which you can fill in to filter modules based on inputted words and selections.
These filters are:

    * **Module**: Input a word or even a couple of words (multiple words will only work if 'search readme' is checked)
    * **Select version**: Which version the module needs to exist in
    * **Installable**: If the module is installable (yes/no/both)
    * **Customer**: Input a customer to filter on
    * **Vertical**: Input a vertical to filter on
    * **Search Readme**: And a checkbox to indicate if the readme should be checked too, instead of only the name

The result will be a table similar to the one described in **Table per Version** below here.
With the exception of an added column:

    * **Repository**: links to the **Table per Version** table for the modules of that repository.


Full table
==========

This page leads to a table that focuses on providing an overview.
When you click on "Full Table" in the menu, you will see a table filled with all existing repositories.

The rows contain a number of columns:

    * **Repository**: The name of the repository
    * **Description**: A very short description of the repository, this does not exist for all repositories
    * **In Scope**: The repository is in the scope of the company (True/False)
    * **BP**: Which BP that is linked to this repository
    * **Employee**: An assignee who has experience with this repository
    * **Edit Repository**: You can click here to edit a couple of options for this repository:
        * BP
        * In Scope
        * Employee

If you click on a repository name, you will see a table filled with modules. These are
all the modules that exists in at least one version of the selected repository. In the columns you can see for which
version every module exists. If it exists, it is indicated as such by an 'X'.
Clicking the 'X' will take you to the corresponding OCA page.
If the module does not exist in a version, the cell will be empty.


Table per version
=================

This page leads to a table that focuses on detail.
First you will be required to select an Odoo version from the existing (and relevant, 6.1 and 7 are not included)
versions. After that you are redirected to a table consisting of repositories. Each of these repositories contain
modules for the selected version. If a repository does not contain existing modules for the selected version,
it is not shown.

You will see the same columns as with **Full Table**, but less rows.
This is because not every module exists in every version.

You can click on every Repository. Doing so will present you with a table of modules that are
part of the repository. You are then greeted by a number of rows and columns:

    * **Addon**: The name of the module
    * **Readme**: If a readme-file exists for this module, a clickable link is shown here
    * **Installable**: This field indicates if the module is installable or not
    * **OCA**: This is a clickable link to the module on OCA
    * **Customer**: Shows all the custmers that have been assigned to this module
    * **Vertical**: Shows all the verticals that have been assigned to this module
    * **Rating**: A user can input a rating using 'write review' which will be shown here
    * **Review**: A user can input a review using 'write review' which will be shown here
    * **Write Review**: A clickable link to write a review and assign a score


OCA
===

This is a link to the Odoo Community Association on GitHub.