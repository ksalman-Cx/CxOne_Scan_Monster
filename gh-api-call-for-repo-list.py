import requests
import random

def get_popular_repositories(limit=50):
    """
    Retrieve a list of popular GitHub repositories based on specified criteria.

    Parameters:
    - limit (int): Maximum number of repositories to retrieve.

    Returns:
    - list: List of GitHub repositories.
    """
    url = "https://api.github.com/search/repositories"
    params = {
        'q': 'stars:>100000 size:<100000',  # Adjust the star count as needed
        'sort': 'stars',
        'order': 'desc',
        'per_page': 100  # Request a maximum of 100 repositories per page
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        repositories = response.json().get('items', [])
        
        # Shuffle the list of repositories and select the first 'limit' number
        random.shuffle(repositories)
        return repositories[:limit]
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
    print(f"Lines of Code: {repo['size']}")
    print(f"URL: http://github.com/{repo['full_name']}")
    print("-" * 50)

def main():
    # Set a maximum limit of 50 repositories
    limit = 50
    repositories = get_popular_repositories(limit)

    total_repos = len(repositories)
    total_loc = sum(repo['size'] for repo in repositories)
    total_stars = sum(repo['stargazers_count'] for repo in repositories)

    print(f"Collected {total_repos} random repositories with a total of {total_loc} lines of code and {total_stars} stars.")

    for repo in sorted(repositories, key=lambda x: x['size']):
        print_repository_details(repo)

if __name__ == "__main__":
    main()
