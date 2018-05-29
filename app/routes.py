# File that creates pages behind URLs
from app import app, db
from flask import render_template, redirect, url_for
from app.forms import SearchModuleForm, SearchRepositoryForm, VersionSelectionForm, RatingReviewForm, \
    EditRepositoryForm, SubmitForm, EditModuleForm
from sqlalchemy import and_
from app.models import Repository, Module
from app.functions import update_repositories, update_single_repository, search_repository_f, \
    search_module_f, rating_review_f, edit_module_f

from app.version_functions import get_version_repositories, search_version_modules


# Routes for single version pages
# ===============================================


@app.route('/version_repositories', methods=['GET', 'POST'])
def version_repositories():
    # dummy value to fill up string
    version_x = "0000 0000"
    form = VersionSelectionForm()
    if form.validate_on_submit():
        version_number = form.select_version.data
        version_x = "version_" + version_number
        return redirect(url_for('version_repositories_2', version_x=version_x))
    return render_template('version_repositories.html', title="repo table", form=form, version_x=version_x)


@app.route('/version_repositories_2/<version_x>', methods=['GET', 'POST'])
def version_repositories_2(version_x):
    repos = get_version_repositories(version_x)

    return render_template('version_repositories_2.html',
                           title=" repo table",
                           version_x=version_x,
                           repos=repos)


@app.route('/version_details/<repository>/<version_x>', methods=['GET', 'POST'])
def version_details(version_x, repository):
    modules = search_version_modules(version_x, repository)  # obsolete?: get_version_repository_and_modules()
    installable = "installable_" + (version_x[8:])
    readme = "readme_" + version_x[8:]
    rating = "rating_" + version_x[8:]
    review = 'review_' + version_x[8:]
    customer = 'customer_' + version_x[8:]
    vertical = 'vertical_' + version_x[8:]
    return render_template('version_details.html',
                           title="details",
                           version_x=version_x,
                           modules=modules,
                           installable=installable,
                           readme=readme,
                           rating=rating,
                           review=review,
                           vertical=vertical,
                           customer=customer)


@app.route('/rating_review/<module>/<version_x>', methods=['GET', 'POST'])
def rating_review(module, version_x):
    module = Module.query.filter(Module.addon == module).first()
    version = version_x[8:]
    form = RatingReviewForm()
    if form.validate_on_submit():
        rating = form.rating.data
        review = form.review.data
        rating_review_f(version, module, rating, review, form.delete_reviews.data)
        # version, module, rating, review, form_delete_reviews_data)
        return redirect(url_for('version_details', repository=module.repo_name, version_x=version_x))
    return render_template('rating_review.html', title='Rating_Review', form=form)


@app.route('/search_module', methods=['GET', 'POST'])
def search_module():
    form = SearchModuleForm()
    if form.is_submitted():
        modules = search_module_f(form.module.data, form.select_version.data,
                                  form.search_readme.data, form.installable_bool.data)
        version_x = 'version_' + form.select_version.data
        installable = 'installable_' + form.select_version.data
        # readme_text = 'readme_text_' + version_x[8:]
        rating = "rating_" + version_x[8:]
        review = 'review_' + version_x[8:]
        readme = 'readme_' + version_x[8:]
        customer = 'customer_' + version_x[8:]
        vertical = 'vertical_' + version_x[8:]
        search_readme = False
        return render_template('search_results_module.html', title='Module Search Results',
                               modules=modules, version_x=version_x,
                               installable=installable, search_readme=search_readme,
                               rating=rating, review=review, readme=readme, vertical=vertical,
                               customer=customer)
    return render_template('search_module.html', title='Search Module', form=form)


@app.route('/search_repository', methods=['GET', 'POST'])
def search_repository():
    form = SearchRepositoryForm()
    if form.validate_on_submit():
        version_x = form.select_version.data
        repositories = search_repository_f(form.repository.data, form.bp.data, form.in_scope.data)
        return render_template('search_results_repository.html',
                               title='Repository Search Results',
                               repositories=repositories,
                               version_x=version_x)
    return render_template('search_repository.html', title='Search Repository', form=form)


@app.route('/edit_repository/<repository>', methods=['GET', 'POST'])
def edit_repository(repository):
    repository = Repository.query.filter(Repository.repository == repository).first()
    form = EditRepositoryForm()
    if form.validate_on_submit():

        if form.bp.data == 'unchanged':
            pass
        else:
            repository.bp = form.bp.data

        if form.in_scope.data == 'unchanged':
            pass
        else:
            repository.in_scope = form.in_scope.data

        if form.employee.data == '':
            pass
        else:
            repository.employee = form.employee.data

        db.session.commit()
        return redirect(url_for('table'))
    return render_template('edit_repository.html', title='Edit Repository', form=form, repository=repository.repository)


@app.route('/edit_module/<module>/<version_x>', methods=['GET', 'POST'])
def edit_module(module, version_x):
    module = Module.query.filter(Module.addon == module).first()
    version = version_x[8:]

    form = EditModuleForm()
    if form.validate_on_submit():

        edit_module_f(version,
                      module,
                      form.customer_str.data,
                      form.vertical_str.data,
                      form.delete_customers.data,
                      form.delete_verticals.data)


        return redirect(url_for('version_details', repository=module.repo_name, version_x=version_x))
    return render_template('edit_module.html', title='Edit Module',
                           form=form, module=module.addon, version=version)


# Routes for all repositories
# ==============================================


# Homepage with multiple routes linked to it
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')


# Route to Table page
@app.route('/table', methods=['GET', 'POST'])
def table():
    # Update table with button, checks if it exists before creating new repository/module
    form = SubmitForm()
    if form.validate_on_submit():
        # Update everything
        update_repositories()
        return redirect(url_for('table'))
    # Show Table
    repository = Repository.query.all()
    return render_template('table.html', title="Table", repository=repository, form=form, )


# route to update a single repository, doesn't actually stay on the page, used more as a pseudo-button.
@app.route('/update_repository/<repository>', methods=['GET', 'POST'])
def update_repository(repository):
    update_single_repository(repository)
    return redirect(url_for('table'))


# Module table, linked to Repository by foreign key on the repository name (=repository)
@app.route('/detail/<repository>', methods=['GET', 'POST'])
def detail(repository):
    r = Repository.query.filter(Repository.repository == repository).first()
    module = Module.query.filter(and_(Module.repo_name == r.repository, Module.addon is not None))
    return render_template('detail.html', title="detail", module=module)

# testing pages used to test new pieces of code

# @app.route('/testing', methods=['GET', 'POST'])
# def testing():
#     # body
#     return render_template('testing.html', title="testing")
#
#
# @app.route('/testing_2', methods=['GET', 'POST'])
# def testing_2():
#     # body
#     return render_template('testing_2.html', title="testing_2")
