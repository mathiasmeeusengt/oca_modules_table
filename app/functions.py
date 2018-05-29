from app import db
from github import GithubException, UnknownObjectException
from sqlalchemy import and_
from app.models import Repository, Module
from urllib.request import urlopen
from app.pygithub_api import get_oca_repositories, get_one_repository
import urllib.request
import urllib.error
import requests


# Order of update functions:
# - update_repositories()
# - update_modules(...)
# - url_test_module(...)
# - count_modules(...)
# - write_installable(...)
# - get_readme


# Main update function. Updates everything of one repository at a time.
# checks if repository is new or not, if true: adds it to the db
def update_repositories():
    counter = 0
    repositories = get_oca_repositories()
    for repository in repositories:
        # start: update repository
        if Repository.query.filter(Repository.repository == repository.name).first():
            repo = Repository.query.filter(Repository.repository == repository.name).first()
            repo.description = repository.description
            db.session.commit()
        else:
            repo = Repository(repository=repository.name, description=repository.description,
                              in_scope='False')

            db.session.add(repo)
            db.session.commit()
        # end: update repository
        # start: update-functions
        # update modules for repository
        update_modules(repository)
        # count modules per version in repository (not in shown in any table)
        count_modules(repository)

        get_installable_and_get_readme(repository)
        get_readme_repository(repository)
        # end: update-functions

        if counter % 5 == 0:
            print('loop {}'.format(counter))
        counter += 1
    pass


# does the same as update_repositories, but for only one repository. function called from any table with repositories
def update_single_repository(repository1):
    repository = get_one_repository(repository1)
    repository1 = Repository.query.filter(Repository.repository == repository.name).first()
    repository1.description = repository.description
    db.session.commit()
    update_modules(repository)
    count_modules(repository)
    get_installable_and_get_readme(repository)
    get_readme_repository(repository)
    pass


# check if a module is new, and check in which versions it exists
def update_modules(repository):
    repository_hashes = get_tree_hashes_per_repo(repository)

    for repository_hash in repository_hashes:
        try:
            gittree_element = repository.get_git_tree(repository_hash)
        except GithubException:
            pass
        try:
            for type_tree in gittree_element.tree:
                if type_tree.type == "tree":
                    if Module.query.filter(Module.addon == type_tree.path).first():
                        # existing module
                        pass
                    else:
                        # new module
                        module = Module(addon=type_tree.path, repo_name=repository.name)
                        db.session.add(module)
                        db.session.commit()
                        pass
                    # update module
                    url_test_module(type_tree.path)

        except UnboundLocalError:
            pass
    pass


# Pull Tree(=branch) hashes(:sha) from a repository using the refs
# Dictionary could be replaced by a string with operators that searches "??.?"
def get_tree_hashes_per_repo(repo):
    references = repo.get_git_refs()
    ref_sha = {'8.0': '', '9.0': '', '10.0': '', '11.0': ''}
    try:
        for reference in references:
            if reference.ref == 'refs/heads/8.0':
                ref_sha['8.0'] += reference.object.sha
            elif reference.ref == 'refs/heads/9.0':
                ref_sha['9.0'] += reference.object.sha
            elif reference.ref == 'refs/heads/10.0':
                ref_sha['10.0'] += reference.object.sha
            elif reference.ref == 'refs/heads/11.0':
                ref_sha['11.0'] += reference.object.sha
            else:
                pass
    except GithubException:
        pass
    return ref_sha


# ping url to see if module exists based on the returned statuscode
def url_test_module(module):
    module = Module.query.filter(Module.addon == module).first()
    module.version_8 = check_if_url_valid("https://github.com/OCA/" + module.repo_name + "/tree/8.0/" + module.addon)
    module.version_9 = check_if_url_valid("https://github.com/OCA/" + module.repo_name + "/tree/9.0/" + module.addon)
    module.version_10 = check_if_url_valid("https://github.com/OCA/" + module.repo_name + "/tree/10.0/" + module.addon)
    module.version_11 = check_if_url_valid("https://github.com/OCA/" + module.repo_name + "/tree/11.0/" + module.addon)
    db.session.commit()
    pass


# return an 'X' if ping status code <= 400 (successful)
def check_if_url_valid(url):
    request = requests.get(url)
    if request.status_code < 400:
        return 'X'
    else:
        return '-'


# assign symbol to get_readme_<object>
def check_if_readme_exists(url):
    request = requests.get(url)
    if request.status_code < 400:
        return 'readme'
    else:
        return '-'


# count number of modules in a repository
def count_modules(repository):
    m8 = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_8 == 'X')).count()
    repository.m_8 = m8
    m9 = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_9 == 'X')).count()
    repository.m_9 = m9
    m10 = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_10 == 'X')).count()
    repository.m_10 = m10
    m11 = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_11 == 'X')).count()
    repository.m_11 = m11
    db.session.commit()
    pass


# checks if the module is installable per version and get the readme right after
def get_installable_and_get_readme(repository):
    modules = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_8 == 'X')).all()
    for module in modules:
        module.installable_8 = get_installable(repository, module, '8.0')
        get_readme_module(module, 'version_8')
    db.session.commit()

    modules = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_9 == 'X')).all()
    for module in modules:
        module.installable_9 = get_installable(repository, module, '9.0')
        get_readme_module(module, 'version_9')
    db.session.commit()

    modules = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_10 == 'X')).all()
    for module in modules:
        module.installable_10 = get_installable(repository, module, '10.0')
        get_readme_module(module, 'version_10')
    db.session.commit()

    modules = Module.query.filter(and_(Module.repo_name == repository.name, Module.version_11 == 'X')).all()
    for module in modules:
        module.installable_11 = get_installable(repository, module, '11.0')
        get_readme_module(module, 'version_11')
    db.session.commit()
    pass


# gets boolean value of installable and returns a string to write in the db
def get_installable(repository, module, version):
    install_bool = 'False'
    install_file = ''
    try:
        files = repository.get_file_contents(module.addon, version)
        for file in files:
            if 'openerp' in file.name:
                install_file = str(file.decoded_content)
            elif 'manifest' in file.name:
                install_file = str(file.decoded_content)
        try:
            install_index = install_file.index('installable')
            ii_end = int(install_index) + 26
            bool_installable = install_file.find('True', install_index, ii_end)
            if bool_installable == -1:
                install_bool = 'False'
            elif bool_installable > 0:
                install_bool = 'True'
        except ValueError:
            pass
    except UnknownObjectException:
        pass
    return install_bool


# get readme text into database, used by search_module_f(...)
def get_readme_module(module, version_x):
    asterisk = '*'
    url = 'https://raw.githubusercontent.com/OCA/{}/{}/{}/README.rst'.format(
        module.repo_name, version_x[8:] + '.0', module.addon)
    try:
        text = (urlopen(url).read()).decode('utf-8')  # get and decode readme text
        for char in asterisk:  # replace bold-syntax '*' with empty string, to make multi-word searches possible
            text = text.replace(char, '')
        if version_x == 'version_8':
            module.readme_text_8 = text
            module.readme_8 = check_if_readme_exists(url)
        elif version_x == 'version_9':
            module.readme_text_9 = text
            module.readme_9 = check_if_readme_exists(url)
        elif version_x == 'version_10':
            module.readme_text_10 = text
            module.readme_10 = check_if_readme_exists(url)
        elif version_x == 'version_11':
            module.readme_text_11 = text
            module.readme_11 = check_if_readme_exists(url)
        db.session.commit()
    except urllib.error.HTTPError:
        pass
    pass


# get the readme of a repository
def get_readme_repository(repository):
    asterisk = '*'
    url = 'https://raw.githubusercontent.com/OCA/{}/11.0/README.md'.format(
        repository.name)
    try:
        text = (urlopen(url).read()).decode('utf-8')
        for char in asterisk:
            text = text.replace(char, '')
        repository = Repository.query.filter(Repository.repository == repository.name).first()
        if text:
            try:
                repository.readme = text
                db.session.commit()
            except AttributeError:
                pass
    except urllib.error.HTTPError or AttributeError:
        pass
    pass


# function to search for modules
def search_module_f(form_module_data,
                    form_select_version_data,
                    form_search_readme_data,
                    form_installable_bool_data):
    version_x = 'version_' + form_select_version_data
    installable = 'installable_' + form_select_version_data
    readme_text = 'readme_text_' + version_x[8:]
    '''
    === Overview for searching Modules ===
    ======================================
    check if module field is empty
        True: skip
        False: cont.
            -check readme?
                True:
                    -check filter
                        -if elif else       check for each option for installable (True/False/both)
                            -query
                False:
                    -check filter
                        -if elif else       check for each option for installable (True/False/both)
                            -query
    ======================================
    '''
    # Module search parameters
    if form_module_data == '':
        modules = []
    else:
        if form_search_readme_data is True:
            if form_installable_bool_data == 'True':
                modules1 = Module.query.filter(and_(Module.addon.like('%' + form_module_data + '%'),
                                                    getattr(Module, installable) == 'True',
                                                    getattr(Module, version_x) == 'X')).all()
                modules2 = Module.query.filter(
                    and_(Module.__getattribute__(Module, readme_text).like('%' + form_module_data + '%'),
                         getattr(Module, installable) == 'True', getattr(Module, version_x) == 'X')).all()
                modules = modules1
                for m in modules2:
                    modules.append(m)
            elif form_installable_bool_data == 'False':
                modules1 = Module.query.filter(
                    and_(Module.addon.like('%' + form_module_data + '%'), getattr(Module, installable) == 'False',
                         getattr(Module, version_x) == 'X')).all()
                modules2 = Module.query.filter(
                    and_(Module.__getattribute__(Module, readme_text).like('%' + form_module_data + '%'),
                         getattr(Module, installable) == 'False', getattr(Module, version_x) == 'X')).all()
                modules = modules1
                for m in modules2:
                    modules.append(m)
            else:
                modules1 = Module.query.filter(
                    and_(Module.addon.like('%' + form_module_data + '%'), getattr(Module, version_x) == 'X')).all()
                modules2 = Module.query.filter(
                    and_(Module.__getattribute__(Module, readme_text).like('%' + form_module_data + '%'),
                         getattr(Module, version_x) == 'X')).all()
                modules = modules1
                for m in modules2:
                    modules.append(m)
        else:
            if form_installable_bool_data == 'True':
                modules = Module.query.filter(and_(
                    (Module.addon.like('%' + form_module_data + '%')),
                    (getattr(Module, installable) == 'True'),
                    (getattr(Module, version_x) == 'X'))).all()
            elif form_installable_bool_data == 'False':
                modules = Module.query.filter(and_(
                    (Module.addon.like('%' + form_module_data + '%')),
                    (getattr(Module, installable) == 'False'),
                    (getattr(Module, version_x) == 'X'))).all()
            else:
                modules = Module.query.filter(and_
                                              (Module.addon.like('%' + form_module_data + '%')),
                                              (getattr(Module, version_x) == 'X')).all()
    return modules


# function to search for repositories
def search_repository_f(form_repository_data, form_bp_data, form_in_scope_data):
    var = ''  # random code to force '''text''' below to be seen as comment, not docstring
    '''
    === Overview for searching Repositories ===
    ===========================================
    check if repo in scope:
        -both
            check BP:
                - unspecified
                - value
        -True
            check BP:
                - unspecified
                - value
        -False
            check BP:
                - unspecified
                - value
    ============================================
    '''
    # Repository search parameters
    if form_in_scope_data == 'both':
        if form_bp_data == 'unspecified':
            repositories = Repository.query.filter(Repository.repository.like('%' + form_repository_data + '%')).all()
        else:
            repositories = Repository.query.filter(and_(Repository.bp == form_bp_data,
                                                        Repository.repository.like(
                                                            '%' + form_repository_data + '%'))).all()
    elif form_in_scope_data == 'True':
        if form_bp_data == 'unspecified':
            repositories = Repository.query.filter(and_(Repository.in_scope == 'True', Repository.repository.like(
                '%' + form_repository_data + '%'))).all()
        else:
            repositories = Repository.query.filter(and_(
                Repository.in_scope == 'True',
                Repository.bp == form_bp_data,
                Repository.repository.like('%' + form_repository_data + '%'))).all()

    elif form_in_scope_data == 'False':
        if form_bp_data == 'unspecified':
            repositories = Repository.query.filter(and_(
                Repository.in_scope == 'False',
                Repository.repository.like('%' + form_repository_data + '%'))).all()
        else:
            repositories = Repository.query.filter(and_(
                Repository.in_scope == 'False',
                Repository.bp == form_bp_data,
                Repository.repository.like('%' + form_repository_data + '%'))).all()
    else:
        repositories = []
    return repositories


# Write the rating and review to db
# Appends new reviews to existing ones
# Can delete all previous reviews
def rating_review_f(version, module, rating, review, form_delete_reviews_data):
    if version == '8':
        module.rating_8 = str(rating)
        if form_delete_reviews_data is True:
            module.review_8 = None
        if module.review_8 is None:
            module.review_8 = str(review)
        else:
            module.review_8 += ' || ' + str(review)
    elif version == '9':
        module.rating_9 = str(rating)
        if form_delete_reviews_data is True:
            module.review_9 = None
        if module.review_9 is None:
            module.review_9 = str(review)
        else:
            module.review_9 += ' || ' + str(review)
    elif version == '10':
        module.rating_10 = str(rating)
        if form_delete_reviews_data is True:
            module.review_10 = None
        if module.review_10 is None:
            module.review_10 = str(review)
        else:
            module.review_10 += ' || ' + str(review)
    elif version == '11':
        module.rating_11 = str(rating)
        if form_delete_reviews_data is True:
            module.review_11 = None
        if module.review_11 is None:
            module.review_11 = str(review)
        else:
            module.review_11 += ' || ' + str(review)
    db.session.commit()
    return


def edit_module_f(version, module, customer_str, vertical_str, customer_delete, vertical_delete):
    customer_version = 'customer_' + version
    vertical_version = 'vertical_' + version

    # clear fields if delete is checked
    if customer_delete is True:
        setattr(module, customer_version, None)
    if vertical_delete is True:
        setattr(module, vertical_version, None)

    # set values if no values are set, or append new values to old ones and set those
    if getattr(module, customer_version) is None:
        setattr(module, customer_version, customer_str)
    else:
        customers = getattr(module, customer_version)
        customers += ' ' + customer_str
        setattr(module, customer_version, customers)

    # set values if no values are set, or append new values to old ones and set those
    if getattr(module, vertical_version) is None:
        setattr(module, vertical_version, vertical_str)
    else:
        verticals = getattr(module, vertical_version)
        verticals += ' ' + vertical_str
        setattr(module, vertical_version, verticals)

    db.session.commit()
    pass


# ==============================================================================================================
# All functions below are currently not used, but still kept just in case.
# "converted" means the function was taken to the new update_repositories() and edited/merged for better performance
# ===========================================================================================================


# import requests
# from app import db
#
#
# # converted
# def check_if_readme_exists(url_to_check):
#     request = requests.get(url_to_check)
#     if request.status_code < 400:
#         return "readme"
#     else:
#         return "-"
#     pass
#
#
# # converted
# # Check URL and return "X" or "-" depending on the returned code
# def check_if_url_is_valid(url_to_check):
#     # can maybe be optimised by only requesting/checking headers
#     # http://docs.python-requests.org/en/latest/user/advanced/?highlight=download#http-verbs
#     request = requests.get(url_to_check)
#     if request.status_code < 400:
#         return "X"
#     else:
#         return "-"
#
#
# # converted
# def module_url_tester(m):
#     from app.models import Module
#     module = Module.query.filter_by(addon=m.addon).first()
#     module.version_8 =
# check_if_url_is_valid("https://github.com/OCA/" + module.repo_name + "/tree/8.0/" + module.addon)
#     module.version_9 =
# check_if_url_is_valid("https://github.com/OCA/" + module.repo_name + "/tree/9.0/" + module.addon)
#     module.version_10 =
# check_if_url_is_valid("https://github.com/OCA/" + module.repo_name + "/tree/10.0/" + module.addon)
#     module.version_11 =
# check_if_url_is_valid("https://github.com/OCA/" + module.repo_name + "/tree/11.0/" + module.addon)
#     db.session.commit()
#     pass
#
#
# # converted
# def get_one_repo_module_and_url_test(repository):
#     from app.models import Module
#     module = Module.query.filter_by(repo_name=repository.repository)
#     for m in module:
#         module_url_tester(m)
#     pass
#
#
# # converted
# def get_all_repo_modules_and_url_test():
#     from app.models import Repository, Module
#     repos = Repository.query.all()
#     for repo in repos:
#         modules = Module.query.filter_by(repo_name=repo.repository)
#         for module in modules:
#             module_url_tester(module)
#         pass
#     pass
#
#
# # converted
# def module_counter(repo):
#     from app.models import Module, Repository
#     '''m61 = Module.query.filter_by(repo_name=repo.repository).filter_by(version_6="X").count()
#     repo.m_6_1 = m61
#     m7 = Module.query.filter_by(repo_name=repo.repository).filter_by(version_7="X").count()
#     repo.m_7 = m7'''
#     m8 = Module.query.filter_by(repo_name=repo.repository).filter_by(version_8="X").count()
#     repo.m_8 = m8
#     m9 = Module.query.filter_by(repo_name=repo.repository).filter_by(version_9="X").count()
#     repo.m_9 = m9
#     m10 = Module.query.filter_by(repo_name=repo.repository).filter_by(version_10="X").count()
#     repo.m_10 = m10
#     m11 = Module.query.filter_by(repo_name=repo.repository).filter_by(version_11="X").count()
#     repo.m_11 = m11
#     db.session.commit()
#     pass
#
#
# # converted
# def count_modules_per_version():
#     from app.models import Repository
#     repo_list = Repository.query.order_by(Repository.id).all()
#     for repo in repo_list:
#         module_counter(repo)
#     pass
