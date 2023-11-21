import requests

def get_owasp_top_repositories(limit=25):
    url = "https://api.github.com/orgs/OWASP/repos"
    params = {
        'per_page': 100,  # You can adjust this based on the organization's repository count
        'type': 'public'  # Only include public repositories
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        repositories = response.json()

        # Filter out private repositories
        public_repositories = [repo for repo in repositories if not repo.get('private')]

        # Sort public repositories by stars in descending order
        sorted_repositories = sorted(public_repositories, key=lambda x: x['stargazers_count'], reverse=True)

        # Select the top 'limit' repositories
        top_repositories = sorted_repositories[:limit]

        return top_repositories
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def write_to_file(repositories):
    with open("OWASP-repos.txt", "w") as file:
        for repo in repositories:
            file.write(f"{repo['html_url']}\n")

def main():
    top_repositories = get_owasp_top_repositories()

    if top_repositories:
        print(f"Collected {len(top_repositories)} top public repositories from OWASP by stars.")

        # Write repository URLs to file
        write_to_file(top_repositories)

        print("Repository URLs written to 'OWASP-repos.txt'.")
    else:
        print("No public repositories found for OWASP.")

if __name__ == "__main__":
    main()
