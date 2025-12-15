```
Colab-VsCode-Bridge
```

A Python package to complete functionalities missing from the VS Code Colab extension.

## Overview

This package fills the gaps in VS Code's Colab extension by providing:

* Upload files from localhost to Colab kernel
* Download smaller files from Colab kernel to local PC
* Authenticate to Kaggle
* Upload from kernel to Kaggle datasets

## Features

* Upload local files to Colab kernel while connected via VS Code
* Download files from Colab kernel to local machine
* Kaggle authentication integration
* Upload datasets from Colab to Kaggle
* Control dataset visibility (public/private)

## Installation

```bash
pip install colab-vscode-bridge
```

## Quick Start

```python
from colab_vscode_bridge import upload_to_colab, download_from_colab, authenticate_kaggle, upload_to_kaggle

# Upload local file to Colab
upload_to_colab(destination_folder='/content/data.csv')

# Download from Colab to local
ColabFileDownloader("data/my_plot.png")

# Authenticate Kaggle
authenticate_kaggle()

# Upload to Kaggle
upload_to_kaggle(
    file_path=file_path,
    dataset_slug="kaggle-dataset-slug",
    dataset_title="kaggle-dataset-title",
    public=False,
)
```

## Requirements

* Python >= 3.8
* VS Code with Colab extension
* Active connection to Colab kernel in VS Code
* Kaggle API credentials (for Kaggle features)

## Usage

**Read**
https://github.com/ranidz/Colab-VsCode-Bridge/blob/main/docs/useDetails.md

## Roadmap

* [X] Upload files from localhost to Colab kernel
* [X] Download files from Colab kernel to local PC
* [X] Kaggle authentication
* [X] Upload from kernel to Kaggle
* [ ] Batch file operations
* [ ] HuggingFace integration
* [ ] Google Drive support
* [ ] Compression for large files

## Contributing

This is an early-stage project. Bug reports and feature requests are welcome via GitHub issues.

## License

MIT License

## Author

**ranidzkellou**

---

 **Note** : This is v0.1.0 - early release bridging VS Code Colab extension gaps.
