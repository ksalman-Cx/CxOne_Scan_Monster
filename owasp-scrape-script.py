import requests

def get_owasp_repositories():
    url = "https://api.github.com/orgs/OWASP/repos"
    params = {
        'per_page': 100,  # You can adjust this based on the organization's repository count
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        repositories = response.json()
        return repositories
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def write_to_file(repositories):
    with open("OWASP-repos.txt", "w") as file:
        for repo in repositories:
            file.write(f"{repo['html_url']}\n")

def main():
    repositories = get_owasp_repositories()

    if repositories:
        print(f"Collected {len(repositories)} repositories from OWASP.")

        # Write repository URLs to file
        write_to_file(repositories)

        print("Repository URLs written to 'OWASP-repos.txt'.")
    else:
        print("No repositories found for OWASP.")

if __name__ == "__main__":
    main()
