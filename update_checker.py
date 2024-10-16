import requests
import os

class UpdateChecker:
    def __init__(self, repo_url, local_version_file="local_version.txt"):
        # Set the URL to the version.txt file on GitHub
        self.repo_url = repo_url.rstrip("/") + "/master/version.txt"
        self.local_version_file = local_version_file

    def get_latest_version(self):
        """Fetch the latest version number from the repository."""
        try:
            print(f"Fetching latest version from {self.repo_url}...")
            response = requests.get(self.repo_url)
            if response.status_code == 200:
                latest_version = response.text.strip()
                print(f"Latest version fetched: {latest_version}")
                return latest_version
            else:
                print(f"Failed to fetch the latest version. HTTP status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching the version: {e}")
            return None

    def get_local_version(self):
        """Retrieve the local version number from the file."""
        if not os.path.exists(self.local_version_file):
            print(f"Local version file '{self.local_version_file}' not found. Assuming version 0.0.0")
            return "0.0.0"  # If the file doesn't exist, assume it's version 0.0.0
        
        try:
            with open(self.local_version_file, "r") as file:
                local_version = file.read().strip()
                print(f"Local version: {local_version}")
                return local_version
        except Exception as e:
            print(f"Error reading local version file: {e}")
            return "0.0.0"  # Return default version if reading fails

    def check_for_updates(self):
        """Check if a new version is available and prompt the user to update."""
        local_version = self.get_local_version()
        latest_version = self.get_latest_version()

        if latest_version is None:
            print("Could not check for updates due to an error fetching the latest version.")
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
        print("1. Type '/update' in the bot's chat.")
        print("2. This will pull the latest changes from the repository and update your bot.")

    def update_local_version(self, new_version):
        """Update the local version file with the new version number."""
        if isinstance(new_version, str) and new_version:
            try:
                with open(self.local_version_file, "w") as file:
                    file.write(new_version)
                print(f"Local version updated to {new_version}")
            except Exception as e:
                print(f"Error writing to local version file: {e}")
        else:
            print("Invalid version format. The version must be a non-empty string.")
