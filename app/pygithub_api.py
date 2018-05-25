# File with functions that work with PyGitHub to use the GitHub API
from github import Github, GithubException, BadCredentialsException


# Change default github.MainClass.Github parameter from 30 to max 200
# per_page = number of items returned per API call
Github.per_page = 50


# Log in with user MathiasMeeusengt using personal access token to get OCA user details
def get_oca_user():
    try:
        g = Github('b5935d3156a0ec6ef53125952c7721ae3f31fa32')
        user_oca = g.get_user('OCA')
        return user_oca
    except BadCredentialsException:
        try:
            g = Github('4c0ec0d70636055953a0a1cce75c2b5173b71135')
            user_oca = g.get_user('OCA')
            return user_oca
        except BadCredentialsException:
            print('BadCredentialsException, 401, personal access token stopped working.'
                  'pygithub_api.py line 10-23')


# Get all repositories from OCA
def get_oca_repositories():
    user_oca_repos = get_oca_user().get_repos().get_page(0)
    # set to higher page for more returned values, pages start at 0
    # (30 values per page, about 170 in total on OCA)
    max_pages = 4
    i = 0
    while i < max_pages:
        i += 1
        user_oca_repos += get_oca_user().get_repos().get_page(i)
    return user_oca_repos


# Get a repository
def get_one_repository(repo):
    user = get_oca_user()
    one_repo = user.get_repo(repo)
    return one_repo


# Not used
# Get branches of a repository
def get_repo_branches(repo):
    branches = get_one_repository(repo).get_branches()
    return branches


# ==============================================================================================================
# All functions below are currently not used, but still kept just in case.
# "converted" means the function was taken to the new update_repositories() and edited/merged for better performance
# ===========================================================================================================


# # converted
# # Pull Tree hashes(:sha) from a repository using the refs
# # Dictionary could be replaced by a string with operators that searches "??.?"
# def get_tree_hashes_per_repo(repo):
#     references = repo.get_git_refs()
#     ref_sha = {'8.0': '', '9.0': '', '10.0': '', '11.0': ''}
#     try:
#         for reference in references:
#             if reference.ref == 'refs/heads/8.0':
#                 ref_sha['8.0'] += reference.object.sha
#             elif reference.ref == 'refs/heads/9.0':
#                 ref_sha['9.0'] += reference.object.sha
#             elif reference.ref == 'refs/heads/10.0':
#                 ref_sha['10.0'] += reference.object.sha
#             elif reference.ref == 'refs/heads/11.0':
#                 ref_sha['11.0'] += reference.object.sha
#             else:
#                 pass
#     except GithubException:
#         pass
#     return ref_sha
#
#
# # converted
# # Get a tree by branch (version) hash
# def get_modules_per_branch_and_repository(repository):
#     from app.models import Module
#     # Get a repo
#     repo = get_one_repository(repository)
#     # Get hashes from above repo
#     repo_hashes = get_tree_hashes_per_repo(repo)
#     # Look through Branches>Trees(hashes) for modules
#     for repo_hash in repo_hashes:
#         try:
#             gittree_element = repo.get_git_tree(repo_hash)
#         except GithubException:
#             pass
#         try:
#             # Filter out .gitignore, README,...
#             for type_tree in gittree_element.tree:
#                 if type_tree.type == "tree":
#                     module = Module(addon=type_tree.path, repo_name=repo.name)
#                     if Module.query.filter_by(addon=module.addon).first() is None:
#                         db.session.add(module)
#                         db.session.commit()
#         except UnboundLocalError:
#             pass
#     return
#
#
# # converted
# # Update tables from scratch
# def update_table_repositories():
#     from app.models import Repository
#     counter = 0
#     db.drop_all()
#     db.create_all()
#     repos = get_oca_repositories()
#
#     for repo in repos:
#         get_modules_per_branch_and_repository(repo.name)
#         repo = Repository(repository=repo.name, description=repo.description)
#         db.session.add(repo)
#         db.session.commit()
#         if counter % 5 == 0:
#             print("loop {}".format(counter))
#         counter += 1
#     print("Repository import complete")
#     return
#
#
# # get content from modules: ReadMe and installable
# # https://api.github.com/repos/OCA/website/contents/website_analytics_piwik?ref=9.0
# #                       /repos/:user/:repo/contents/:path  (/:ref)
# # :ref is optional, without it goes to default branch (Master, usually 11.0)
# # http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_contents
#
#
# # converted
# def query_all_existing_modules_for_installable():
#     from app.models import Repository, Module
#     from sqlalchemy import and_
#     repositories = Repository.query.all()
#     for repo in repositories:
#
#         modules = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_8 == "X")).all()
#         for module in modules:
#             module.installable_8 = get_install_boolean(repo.repository, module, "8.0")
#             db.session.commit()
#
#         modules = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_9 == "X")).all()
#         for module in modules:
#             module.installable_9 = get_install_boolean(repo.repository, module, "9.0")
#             db.session.commit()
#
#         modules = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_10 == "X")).all()
#         for module in modules:
#             module.installable_10 = get_install_boolean(repo.repository, module, "10.0")
#             db.session.commit()
#
#         modules = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_11 == "X")).all()
#         for module in modules:
#             module.installable_11 = get_install_boolean(repo.repository, module, "11.0")
#             db.session.commit()
#     pass
#
#
# # converted
# def get_install_boolean(repository, module, version_0):
#     install_bool = "False"
#     install_file = ''
#     repo = get_one_repository(repository)
#     files = repo.get_file_contents(module.addon, version_0)
#
#     for file in files:
#         if "openerp" in file.name:
#             install_file = str(file.decoded_content)
#         elif "manifest" in file.name:
#             install_file = str(file.decoded_content)
#     try:
#         install_index = install_file.index('installable')
#         ii_end = int(install_index) + 26
#         install_true = install_file.find("True", install_index, ii_end)
#
#         if install_true == -1:
#             install_bool = "False"
#         elif install_true > 0:
#             install_bool = "True"
#     except ValueError:
#         pass
#     return install_bool
#
#
# # converted
# def get_readme_and_save_to_table(module, version_x):
#     from app.functions import check_if_readme_exists
#     version = version_x[8:]
#     asterisk = '*'
#     url = 'https://raw.githubusercontent.com/OCA/{}/{}/{}/README.rst'.format(
#         module.repo_name, version_x[8:] + ".0", module.addon)
#     # check_if_readme_exists(url)
#     try:
#         text = (urlopen(url).read()).decode('utf-8')
#         for char in asterisk:
#             text = text.replace(char, '')
#         if version == "8":
#             module.readme_text_8 = text
#             module.readme_8 = check_if_readme_exists(url)
#         elif version == "9":
#             module.readme_text_9 = text
#             module.readme_9 = check_if_readme_exists(url)
#         elif version == "10":
#             module.readme_text_10 = text
#             module.readme_10 = check_if_readme_exists(url)
#         elif version == "11":
#             module.readme_text_11 = text
#             module.readme_11 = check_if_readme_exists(url)
#
#         db.session.commit()
#     except urllib.error.HTTPError:
#         pass
#     pass
#
#
# # converted, merged with other function into "get_readme"
# # variables need to be removed from call, or filled somehow: (version_x, repo)
# def search_version_modules_to_get_readme():
#     from app.models import Module, Repository
#     from sqlalchemy import and_
#     repository = Repository.query.all()
#     for repo in repository:
#
#         m = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_8 == "X")).all()
#         version_x = "version_8"
#         for module in m:
#             get_readme_and_save_to_table(module, version_x)
#
#         m = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_9 == "X")).all()
#         version_x = "version_9"
#         for module in m:
#             get_readme_and_save_to_table(module, version_x)
#
#         m = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_10 == "X")).all()
#         version_x = "version_10"
#         for module in m:
#             get_readme_and_save_to_table(module, version_x)
#
#         m = Module.query.filter(and_(Module.repo_name == repo.repository, Module.version_11 == "X")).all()
#         version_x = "version_11"
#         for module in m:
#             get_readme_and_save_to_table(module, version_x)
#     pass
#
#
# # converted, see update_repositories()
# # collection of update functions
# def mass_update():
#     from app.functions import get_all_repo_modules_and_url_test, count_modules_per_version
#
#     update_table_repositories()  # update_repositories
#     get_all_repo_modules_and_url_test()
#     count_modules_per_version()
#     query_all_existing_modules_for_installable()
#     search_version_modules_to_get_readme()
#     pass
#
#
# # not used
# def restructuredtext_test(raw_rst):
#     parts = core.publish_parts(
#         source=raw_rst,
#         writer_name='html')
#     return parts['body_pre_docinfo']+parts['fragment']
#
#
# # not used
# def get_readme_and_save_locally(module, version_x):
#     # download the file from 'url' and save it locally under 'file_name':
#     url = 'https://raw.githubusercontent.com/OCA/{}/{}/{}/README.rst'.format(
#         module.repo_name, version_x[8:] + ".0", module.addon)
#     from app.functions import check_if_readme_exists
#     check_if_readme_exists(url)
#     file_name = "{}__{}__v{}.txt".format(module.repo_name, module.addon, version_x[8:])
#     # change directory to save to
#     os.chdir('D:\\flask\\stageopdracht\\READMEs')
#     try:
#         with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
#             shutil.copyfileobj(response, out_file)
#     except urllib.error.HTTPError:
#         pass
#     pass
