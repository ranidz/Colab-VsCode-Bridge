# Usage Guide

## Installation

```bash
pip install colab-vscode-bridge
```

## Import

```python
from colab_vscode_bridge import (
    upload_to_colab,
    ColabFileDownloader,
    authenticate_kaggle,
    upload_to_kaggle
)
```

---

## 1. Upload Files to Colab

Upload files from your local machine to the Colab kernel.

```python
# Upload to default location (/content/uploads)
upload_to_colab()

# Upload to custom location
upload_to_colab(destination_folder='/content/data')
```

**Parameters:**
- `destination_folder` (str, optional): Target directory in Colab. Default: `/content/uploads`

**Returns:** Interactive file upload widget

---

## 2. Download Files from Colab

Download files from Colab kernel to your local machine.

```python
# Download a single file
ColabFileDownloader("data/my_plot.png")

# Download with custom button text
ColabFileDownloader("results.csv", description="Download Results")
```

**Parameters:**
- `file_path` (str): Path to file in Colab kernel
- `description` (str, optional): Custom button text

**Note:** Best for small files only. Large files may fail due to browser limitations.

---

## 3. Authenticate Kaggle

Set up Kaggle API credentials in the Colab environment.

```python
authenticate_kaggle()
```

**Interactive prompts:**
1. Enter your Kaggle username
2. Enter your Kaggle API token

**Where to get credentials:**
1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New Token"
4. Use the username and key from downloaded `kaggle.json`

---

## 4. Upload to Kaggle

Upload files from Colab to Kaggle as a dataset.

```python
# Basic upload (private dataset)
upload_to_kaggle(
    file_path="/content/data.csv",
    dataset_slug="my-dataset",
    dataset_title="My Dataset"
)

# Public dataset with subtitle
upload_to_kaggle(
    file_path="/content/model.h5",
    dataset_slug="my-model",
    dataset_title="My Trained Model",
    subtitle="A neural network model",
    public=True
)

# Custom license and options
upload_to_kaggle(
    file_path="/content/results.csv",
    dataset_slug="experiment-results",
    dataset_title="Experiment Results",
    license_name="MIT",
    quiet=True,
    keep_tabular=True
)
```

**Parameters:**
- `file_path` (str): Path to file in Colab
- `dataset_slug` (str): Dataset URL slug (no spaces/underscores)
- `dataset_title` (str): Display title
- `upload_folder` (str, optional): Temp folder. Default: `/content/data/upload_folder`
- `subtitle` (str, optional): Dataset subtitle
- `license_name` (str, optional): License type. Default: `CC0-1.0`
- `public` (bool, optional): Make public. Default: `False`
- `quiet` (bool, optional): Suppress output. Default: `False`
- `keep_tabular` (bool, optional): Don't convert to CSV. Default: `False`
- `dir_mode` (str, optional): Directory handling: `skip`, `zip`, `tar`. Default: `skip`

**Returns:** `True` if successful, `False` otherwise

**Important:**
- Must call `authenticate_kaggle()` first
- Dataset slug cannot contain spaces or underscores
- Use hyphens instead: `my-dataset-name`

---

## Complete Workflow Example

```python
from colab_vscode_bridge import *

# 1. Upload training data from local to Colab
upload_to_colab(destination_folder='/content/data')

# 2. Train your model (your code here)
# ...

# 3. Download results to local machine
ColabFileDownloader("/content/results.csv")

# 4. Authenticate Kaggle
authenticate_kaggle()

# 5. Upload model to Kaggle
upload_to_kaggle(
    file_path="/content/model.h5",
    dataset_slug="my-trained-model",
    dataset_title="My Trained Model",
    public=False
)
```

---

## Common Issues

**Upload to Colab not working:**
- Ensure you're connected to Colab kernel via VS Code
- Check destination folder permissions

**Download fails:**
- File too large (use for small files only)
- File path doesn't exist

**Kaggle authentication fails:**
- Verify credentials from kaggle.com/settings
- Remove quotes when pasting token

**Kaggle upload fails:**
- Check authentication first
- Verify slug has no spaces/underscores
- Ensure file exists at specified path
