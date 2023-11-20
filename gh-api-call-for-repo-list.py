import requests
from datetime import datetime, timedelta

def get_repositories_by_criteria(stars_threshold=1000, forks_threshold=500, limit=100):
    """
    Retrieve a list of GitHub repositories based on specified star and fork criteria.

    Parameters:
    - stars_threshold (int): Minimum number of stars.
    - forks_threshold (int): Minimum number of forks.
    - limit (int): Maximum number of repositories to retrieve.

    Returns:
    - list: List of GitHub repositories.
    """
    url = "https://api.github.com/search/repositories"
    params = {
        'q': f'stars:>{stars_threshold} forks:>{forks_threshold}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': limit
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
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
    print(f"\nRepository: {repo['full_name']}")
    print(f"Stars: {repo['stargazers_count']}")
    print(f"Forks: {repo['forks_count']}")
    print(f"Watchers: {repo['watchers_count']}")
    print(f"Issues: {repo['open_issues_count']}")
    print(f"Pull Requests: {repo['pulls_url'].replace('{/number}', '')}")
    print(f"Contributors: {repo['contributors_url']}")
    print(f"License: {repo['license']['name'] if repo['license'] else 'None'}")
    print(f"Last Commit: {datetime.strptime(repo['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')}")
    print(f"URL: http://github.com/{repo['full_name']}")
    print("-" * 50)

def write_to_file(repositories):
    """
    Write GitHub URLs to a file.

    Parameters:
    - repositories (list): List of GitHub repositories.
    """
    with open("repos.txt", "w") as file:
        for repo in repositories:
            file.write(f"http://github.com/{repo['full_name']}\n")

def main():
    # Set the thresholds for stars and forks, and the limit of repositories
    stars_threshold = 1000
    forks_threshold = 500
    limit = 100

    # Get repositories based on criteria
    repositories = get_repositories_by_criteria(stars_threshold=stars_threshold, forks_threshold=forks_threshold, limit=limit)

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
