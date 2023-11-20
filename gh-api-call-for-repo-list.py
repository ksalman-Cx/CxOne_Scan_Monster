import requests

def get_repositories():
    url = "https://api.github.com/search/repositories"
    params = {
        'q': 'stars:>100000 size:<100000',  # Adjust the star count as needed
        'sort': 'stars',
        'order': 'desc'
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        repositories = response.json().get('items', [])
        return sorted(repositories, key=lambda x: x['size'])
    else:
        print(f"Error: {response.status_code}")
        return []

repositories = get_repositories()

for repo in repositories:
    print(f"Repository: {repo['full_name']}, Stars: {repo['stargazers_count']}, Size: {repo['size']} lines of code")
    print(f"URI: {repo['html_url']}")
    print("-" * 50)

# Plain text list of GitHub URLs
print("\nPlain text list of GitHub URLs:")
for repo in repositories:
    print(f"http://github.com/{repo['full_name']}")
