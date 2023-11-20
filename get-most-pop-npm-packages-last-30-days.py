import requests
from datetime import datetime, timedelta

def get_most_popular_npm_packages(last_days=30, limit=10):
    # Calculate the date from which packages should be considered
    since_date = (datetime.now() - timedelta(days=last_days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    url = "https://api.npmjs.org/downloads/range"
    params = {
        'start': since_date,
        'end': 'latest',
        'period': 'daily',
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json().get('downloads', [])

        # Sort packages by download count in descending order
        sorted_packages = sorted(data, key=lambda x: x['downloads'], reverse=True)

        # Take the top 'limit' packages
        top_packages = sorted_packages[:limit]
        return top_packages
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

# The rest of the script remains the same...

if __name__ == "__main__":
    # Set the number of days and the limit of packages
    last_days = 30
    limit = 10

    # Get the most popular NPM packages in the last 30 days
    packages = get_most_popular_npm_packages(last_days=last_days, limit=limit)

    total_packages = len(packages)

    if total_packages > 0:
        print(f"Collected details for the {total_packages} most popular NPM packages in the last {last_days} days.")

        for package in packages:
            print(f"\nPackage: {package['package']}")
            print(f"Downloads: {package['downloads']}")
            print(f"Start Date: {package['start']}")
            print(f"End Date: {package['end']}")
            print("-" * 50)

        # Write NPM package details to 'npm_packages.txt'
        write_to_file(packages)
        print("NPM package details written to 'npm_packages.txt'.")
    else:
        print(f"No packages found in the last {last_days} days.")
