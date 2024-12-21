import requests
import sys

def check_support():
    # Repository details
    repo_owner = "Mickekofi"
    repo_name = "EyeTubeBot"

    print("Please enter your GitHub username:")
    github_user = input("> ").strip()

    print(f"Checking if {github_user} has starred or forked the repository...")

    # GitHub API endpoints
    star_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/stargazers"
    fork_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/forks"

    try:
        # Fetch stargazers
        star_response = requests.get(star_url)
        star_response.raise_for_status()
        stargazers = [user['login'] for user in star_response.json()]

        # Fetch forks
        fork_response = requests.get(fork_url)
        fork_response.raise_for_status()
        forkers = [fork['owner']['login'] for fork in fork_response.json()]

        if github_user not in stargazers and github_user not in forkers:
            print("\033[91mPlease, You must star 🌟 or fork 🍽  the repository to use EyeTubeBot. Please do so and try again...\033[0m")
            sys.exit(1)
        else:
            print("\033[92mThank you for supporting the project!\033[0m")

    except requests.exceptions.RequestException as e:
        print("\033[91m Error checking repository support. Please try again later.\033[0m")
        sys.exit(1)


