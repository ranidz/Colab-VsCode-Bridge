import os
import json
import shutil
import subprocess


def upload_to_kaggle(
    file_path: str,
    dataset_slug: str,
    dataset_title: str,
    upload_folder: str = "/content/data/upload_folder",
    subtitle: str = None,
    license_name: str = "CC0-1.0",
    public: bool = False,
    quiet: bool = False,
    keep_tabular: bool = False,
    dir_mode: str = "skip",
):
    """
    Upload a file to Kaggle as a dataset.

    Args:
        file_path: Path to the file to upload
        dataset_slug: Kaggle dataset slug (no spaces or underscores)
        dataset_title: Display title for the dataset
        upload_folder: Temporary folder for upload preparation
        subtitle: Optional subtitle for the dataset
        license_name: License type (default: CC0-1.0)
        public: Make the dataset public (default: False, private)
        quiet: Suppress verbose output (default: False)
        keep_tabular: Do not convert tabular files to CSV (default: False)
        dir_mode: How to handle directories: 'skip', 'zip', or 'tar' (default: 'skip')

    Returns:
        bool: True if upload successful, False otherwise
    """

    # Validate dir_mode
    valid_dir_modes = ["skip", "zip", "tar"]
    if dir_mode not in valid_dir_modes:
        raise ValueError(
            f"Invalid dir_mode: '{dir_mode}'. Must be one of {valid_dir_modes}"
        )

    # Check for Kaggle authentication
    kaggle_json_path = "/root/.config/kaggle/kaggle.json"
    has_kaggle_json = os.path.exists(kaggle_json_path)
    has_env_vars = "KAGGLE_USERNAME" in os.environ and "KAGGLE_KEY" in os.environ

    if not has_kaggle_json and not has_env_vars:
        print("ERROR: Kaggle authentication not found.")
        print("Please set up authentication using one of these methods:")
        print("1. Create kaggle.json at /root/.config/kaggle/kaggle.json")
        print("2. Set KAGGLE_USERNAME and KAGGLE_KEY environment variables")
        return False

    # Validate dataset slug
    if " " in dataset_slug:
        raise ValueError(f"Dataset slug cannot contain spaces: '{dataset_slug}'")
    if "_" in dataset_slug:
        raise ValueError(f"Dataset slug cannot contain underscores: '{dataset_slug}'")

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_name = os.path.basename(file_path)

    # Create upload folder
    if os.path.exists(upload_folder):
        shutil.rmtree(upload_folder)

    os.makedirs(upload_folder, exist_ok=True)

    # Copy file to upload folder
    dest_path = os.path.join(upload_folder, file_name)
    shutil.copy(file_path, dest_path)

    # Read Kaggle username
    if has_kaggle_json:
        with open(kaggle_json_path, "r") as f:
            kaggle_data = json.load(f)
            kaggle_username = kaggle_data.get("username")
    else:
        kaggle_username = os.environ.get("KAGGLE_USERNAME")

    if not kaggle_username:
        print("ERROR: Could not determine Kaggle username")
        return False

    # Create metadata
    metadata = {
        "title": dataset_title,
        "id": f"{kaggle_username}/{dataset_slug}",
        "licenses": [{"name": license_name}],
    }

    if subtitle:
        metadata["subtitle"] = subtitle

    metadata_path = os.path.join(upload_folder, "dataset-metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    # Prepare environment
    upload_env = os.environ.copy()
    upload_env["KAGGLE_CONFIG_DIR"] = "/root/.config/kaggle"

    # Ensure credentials are in environment
    if has_kaggle_json:
        try:
            with open(kaggle_json_path, "r") as f:
                kaggle_data = json.load(f)
                upload_env["KAGGLE_USERNAME"] = kaggle_data.get("username", "")
                upload_env["KAGGLE_KEY"] = kaggle_data.get("key", "")
        except:
            pass

    # Upload to Kaggle
    try:
        # Build command with optional flags
        command = ["kaggle", "datasets", "create", "-p", upload_folder]

        if public:
            command.append("-u")

        if quiet:
            command.append("-q")

        if keep_tabular:
            command.append("-t")

        command.extend(["-r", dir_mode])

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=upload_env,
        )

        if result.returncode == 0:
            if not quiet:
                print("Upload successful!")
                if result.stdout.strip():
                    print(result.stdout)
            return True
        else:
            if not quiet:
                print("Upload failed.")
                if result.stderr.strip():
                    print(f"Error: {result.stderr}")
                if result.stdout.strip():
                    print(result.stdout)
            return False

    except Exception as e:
        if not quiet:
            print(f"Exception during upload: {e}")
        return False
