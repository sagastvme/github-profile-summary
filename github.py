import datetime
from collections import OrderedDict
import requests
from graphs import bar_chart, pie_chart
from dates import fromIsoStrToDate, getRelativeDate,parseIsoDateToDateObject


def prepare_user_info(username, user_info_request_content):
    user_info = profile_info(username, user_info_request_content)
    repo_specific_data_and_graphs = prepare_repo_section(user_info.get('repos_url'), username)
    return {**user_info, **repo_specific_data_and_graphs}

def prepare_repo_section(repo_info_endpoint, username):
    try:
        response = requests.get(repo_info_endpoint)
        response.raise_for_status()
        repo_info = response.json()
    except (requests.RequestException, ValueError):
        return None

    repos_per_lang = {}
    stars_data = {}
    stars_lang_data = {}
    commits_data = {}
    commits_per_lang = {}
    commits_per_year={}
    websites_deployed = []

    for repo in repo_info:
        lang = repo.get('language') or 'Unknown'
        repos_per_lang[lang] = repos_per_lang.get(lang, 0) + 1
        
        repo_name = repo.get('name')
        stargazers_count = repo.get('stargazers_count', 0)
        if stargazers_count > 0:
            stars_data[repo_name] = stargazers_count
            stars_lang_data[lang] = stars_lang_data.get(lang, 0) + stargazers_count

        if repo.get('homepage'):
            websites_deployed.append({'name': repo_name, 'url': repo.get('homepage')})
        
        commits_url_template = repo.get('commits_url')
        if commits_url_template:
            commits_url = commits_url_template.replace('{/sha}', '')
            try:
                commits_response = requests.get(commits_url)
                
                commits_response.raise_for_status()
                commit_list = commits_response.json()
            except (requests.RequestException, ValueError):
                continue

            commit_count = filter(lambda commit: only_user_commits(commit, username), commit_list)
            commit_count = len(list(commit_count))
            commits_data[repo_name] = commit_count
            commits_per_lang[lang] = commits_per_lang.get(lang, 0) + commit_count
            one_year_ago = getRelativeDate(years=1, months=1)
       
            for commit in commit_list:
                if commit and commit.get('author') and commit.get('author').get('login'):
                    if commit and  commit.get('author').get('login').lower() == username.lower():
                        date = commit.get('commit').get('author').get('date') or None 
                        if date : 
                            date = parseIsoDateToDateObject(date)
                            if date >= one_year_ago:
                                year = date.year
                                month = date.month
                                key = f"{year}:{month}"
                                commits_per_year[key] = commits_per_year.get(key, 0 ) + 1
                              
            commits_per_year = OrderedDict(sorted(
                commits_per_year.items(), 
                key=lambda keyAndValue: tuple(map(int, keyAndValue[0].split(":")))
            ))
          
            
            # loop through commit count and get count where author.login == username and author.date more or equal to date from today to last year 
    return {
        'stars_per_repo': pie_chart(stars_data, 'Stars per repo', graph_type='stars_per_repo'),
        'stars_per_lang': pie_chart(stars_lang_data, 'Stars per language', graph_type='stars_per_lang'),
        'commits_per_repo': pie_chart(commits_data, 'Public commits per repo', graph_type='commits_per_repo'),
        'commits_per_lang': pie_chart(commits_per_lang, 'Public commits per lang', graph_type='commits_per_lang'),
        'repos_per_language': pie_chart(repos_per_lang, 'Repos per language', graph_type='repos_per_language'),
        'commits_in_last_year': bar_chart(commits_per_year, 'Public commits in the last year', 'Public commits per month', graph_type='commits_in_last_year'),
        'websites_deployed': websites_deployed
    }
def profile_info(username, user_info_request_content):
    keys = [
        'avatar_url',
        'bio',
        'public_repos',
        'public_gists',
        'html_url',
        'company',
        'email',
        'hireable',
        'twitter_username',
        'name',
        'location',
        'blog',
        'following',
        'followers',
        'url', 
        'following_url',
        'followers_url', 
        'repos_url', 
        'gists_url'
    ]
    template_data = {}

    for key in keys:
        template_data[key] = user_info_request_content.get(key)
    current_date = datetime.datetime.now(datetime.timezone.utc)
    created_at = user_info_request_content.get('created_at')
    updated_at = user_info_request_content.get('updated_at')
    template_data['years_since'] = (current_date - parseIsoDateToDateObject(created_at)).days // 365
    template_data['created_account'] = fromIsoStrToDate(created_at, '%b %d, %Y') if created_at else None
    template_data['updated_at'] = fromIsoStrToDate(updated_at, '%b %d, %Y') if updated_at else None
    return template_data


def only_user_commits(commit, username):
    return commit.get('author').get('login').lower() == username.lower() if commit and commit.get('author') and commit.get('author').get('login') else False