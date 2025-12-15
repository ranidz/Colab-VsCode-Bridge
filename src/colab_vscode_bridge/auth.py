from getpass import getpass
import json
import os
import shutil


def clean_kaggle_credentials():
    """
    Remove all existing kaggle.json files and clear environment variables.
    """
    # Remove kaggle.json files from common locations
    kaggle_paths = [
        "/root/.config/kaggle/kaggle.json",
        "/root/.kaggle/kaggle.json",
        "/content/.kaggle/kaggle.json",
        "/content/kaggle.json",
        "kaggle.json",
    ]

    for path in kaggle_paths:
        if os.path.exists(path):
            os.remove(path)

    # Remove directories if empty
    kaggle_dirs = [
        "/root/.config/kaggle",
        "/root/.kaggle",
        "/content/.kaggle",
    ]

    for dir_path in kaggle_dirs:
        if os.path.exists(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)

    # Clear environment variables
    env_vars = ["KAGGLE_USERNAME", "KAGGLE_KEY", "KAGGLE_API_TOKEN"]
    for var in env_vars:
        os.environ.pop(var, None)


def authenticate_kaggle():
    """
    Handles Kaggle authentication using newly generated credentials.
    Works with both Kaggle v1.7 and v1.8+.
    """

    # Clean up old credentials
    clean_kaggle_credentials()

    # Get new credentials
    kaggle_username = input("Kaggle Username: ")
    kaggle_username = kaggle_username.strip().replace('"', "").replace("'", "")

    raw_token = getpass("Kaggle Token: ")
    raw_token = raw_token.strip().replace('"', "").replace("'", "")

    # Create kaggle.json
    kaggle_dir = "/root/.config/kaggle"
    os.makedirs(kaggle_dir, exist_ok=True)

    kaggle_json = {"username": kaggle_username, "key": raw_token}

    kaggle_path = os.path.join(kaggle_dir, "kaggle.json")
    with open(kaggle_path, "w") as f:
        json.dump(kaggle_json, f)

    os.chmod(kaggle_path, 0o600)

    # Set environment variables
    os.environ["KAGGLE_USERNAME"] = kaggle_username
    os.environ["KAGGLE_KEY"] = raw_token
