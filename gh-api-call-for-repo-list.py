import requests
from datetime import datetime, timedelta

def construct_api_url(stars_threshold, forks_threshold, limit):
    """
    Construct the GitHub API URL based on specified criteria.

    Parameters:
    - stars_threshold (int): Minimum number of stars.
    - forks_threshold (int): Minimum number of forks.
    - limit (int): Maximum number of repositories to retrieve.

    Returns:
    - str: GitHub API URL.
    """
    return f"https://api.github.com/search/repositories?q=stars%3A%3E{stars_threshold}+forks%3A%3E{forks_threshold}&sort=stars&order=desc&per_page={limit}"

def get_repositories(api_url):
    """
    Retrieve a list of GitHub repositories based on the provided API URL.

    Parameters:
    - api_url (str): GitHub API URL.

    Returns:
    - list: List of GitHub repositories.
    """
    headers = {'Accept': 'application/vnd.github.v3+json'}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        repositories = response.json().get('items', [])
        return repositories
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def print_repository_details(repo):
    """
    Print details of a GitHub repository.

    Parameters:
    - repo (dict): GitHub repository details.
    """
    print(f"\nRepository: {repo.get('full_name', 'N/A')}")
    print(f"Stars: {repo.get('stargazers_count', 'N/A')}")
    print(f"Forks: {repo.get('forks_count', 'N/A')}")
    print(f"Watchers: {repo.get('watchers_count', 'N/A')}")
    print(f"Issues: {repo.get('open_issues_count', 'N/A')}")
    print(f"Pull Requests: {repo.get('pulls_url', '').replace('{/number}', '')}")
    print(f"Contributors: {repo.get('contributors_url', 'N/A')}")
    print(f"License: {repo['license']['name'] if repo.get('license') else 'None'}")
    print(f"Last Commit: {datetime.strptime(repo.get('pushed_at', ''), '%Y-%m-%dT%H:%M:%SZ')}")
    print(f"URL: http://github.com/{repo.get('full_name', 'N/A')}")
    print("-" * 50)

def write_to_file(repositories):
    """
    Write GitHub URLs to a file.

    Parameters:
    - repositories (list): List of GitHub repositories.
    """
    with open("repos.txt", "w") as file:
        for repo in repositories:
            file.write(f"http://github.com/{repo.get('full_name', 'N/A')}\n")

def main():
    # Set the thresholds for stars and forks, and the limit of repositories
    stars_threshold = 1000
    forks_threshold = 500
    limit = 100

    # Construct the GitHub API URL
    api_url = construct_api_url(stars_threshold, forks_threshold, limit)

    # Get repositories based on the API URL
    repositories = get_repositories(api_url)

    total_repos = len(repositories)

    if total_repos > 0:
        print(f"Collected {total_repos} repositories with stars > {stars_threshold} and forks > {forks_threshold}.")

        for repo in repositories:
            print_repository_details(repo)

        # Write GitHub URLs to 'repos.txt'
        write_to_file(repositories)
        print("GitHub URLs written to 'repos.txt'.")
    else:
        print(f"No repositories found with stars > {stars_threshold} and forks > {forks_threshold}.")

if __name__ == "__main__":
    main()
