# File with functions that work with PyGitHub to use the GitHub API
from github import Github, GithubException, BadCredentialsException


# Change default github.MainClass.Github parameter from 30 to max 200
# per_page = number of items returned per API call
Github.per_page = 50


# Log in with user MathiasMeeusengt using personal access token to get OCA user details
def get_oca_user():
    g = Github('f92e0afc29454e34b9679c60e44c4502754065f7')
    user_oca = g.get_user('OCA')
    return user_oca




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

