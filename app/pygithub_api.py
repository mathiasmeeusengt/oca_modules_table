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

