import requests

def get_repositories():
    url = "https://api.github.com/search/repositories"
    params = {
        'q': 'stars:>1 size:<100000',
        'sort': 'stars',
        'order': 'desc'
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []

repositories = get_repositories()

for repo in repositories:
    print(f"Repository: {repo['full_name']}, Stars: {repo['stargazers_count']}, Size: {repo['size']} lines of code")
