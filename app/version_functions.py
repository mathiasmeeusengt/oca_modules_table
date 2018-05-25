# File that contains functions on querying the db based on the selected version
from app.models import Repository, Module
from sqlalchemy import and_


# get all repositories
# query modules
# if no modules exist in that version, dont show repository


# get a repositories' modules that exist in version_x
def search_version_modules(version_x, repo):
    if version_x == 'version_8':
        m = Module.query.filter(and_(Module.repo_name == repo, Module.version_8 == 'X')).all()
        return m
    elif version_x == 'version_9':
        m = Module.query.filter(and_(Module.repo_name == repo, Module.version_9 == 'X')).all()
        return m
    elif version_x == 'version_10':
        m = Module.query.filter(and_(Module.repo_name == repo, Module.version_10 == 'X')).all()
        return m
    elif version_x == 'version_11':
        m = Module.query.filter(and_(Module.repo_name == repo, Module.version_11 == 'X')).all()
        return m
    pass


# get modules for version_x
def get_version_repositories_and_modules(version_x):
    repositories = Repository.query.all()
    modules = []

    for repo in repositories:  # query all repos
        m = search_version_modules(version_x, repo.repository)
        modules.extend(m)
    return modules


# def get_version_repository_and_modules(version_x, repository):
#     modules = search_version_modules(version_x, repository)
#     return modules


# get repositories that have modules for version_x
def get_version_repositories(version_x):
    repos = []
    modules = get_version_repositories_and_modules(version_x)
    for repo_n in modules:
        repo = Repository.query.filter_by(repository=repo_n.repo_name).first()
        if repo not in repos:
            repos.append(repo)
    return repos
