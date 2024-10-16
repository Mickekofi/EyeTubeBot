import requests

class UpdateChecker:
    def __init__(self, repo_url, local_version_file="local_version.txt"):
        # Set the URL to the version.txt file on GitHub
        self.repo_url = repo_url.rstrip("/") + "/main/version.txt"
        self.local_version_file = local_version_file

    def get_latest_version(self):
        """Fetch the latest version number from the repository."""
        try:
            response = requests.get(self.repo_url)
            if response.status_code == 200:
                return response.text.strip()
            else:
                print("Failed to fetch the latest version.")
                return None
        except Exception as e:
            print(f"Error occurred while fetching the version: {e}")
            return None

    def get_local_version(self):
        """Retrieve the local version number from the file."""
        try:
            with open(self.local_version_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "0.0.0"  # If the file doesn't exist, assume it's version 0.0.0

    def check_for_updates(self):
        """Check if a new version is available and prompt the user to update."""
        local_version = self.get_local_version()
        latest_version = self.get_latest_version()

        if latest_version is None:
            print("Could not check for updates.")
        elif local_version != latest_version:
            print(f"A new version ({latest_version}) is available!")
            print("Please update your bot by downloading the latest version from GitHub.")
            print("Update link: https://github.com/Mickekofi/EyeTubeBot")  
            self.prompt_update()
        else:
            print("Your bot is up to date.")

    def prompt_update(self):
        """Provide instructions for updating the bot."""
        print("\nTo update the bot, follow these steps:\n")
        print("1. type '/update' in the bot's chat")
        print("This will pull the latest changes from the repository.")

    def update_local_version(self, new_version):
        """Update the local version file with the new version number."""
        with open(self.local_version_file, "w") as file:
            file.write(new_version)

