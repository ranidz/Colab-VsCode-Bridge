#  Kaggle-Colab Bridge

A Python package to simplify file transfers between Google Colab, Kaggle datasets, and your local machine.

## Overview

This package streamlines common workflows when working in Google Colab:

* Upload datasets and results to Kaggle datasets
* Download files from Colab to your local machine
* Simplified authentication process

## Features

* Easy authentication with clickable links
* Upload files and folders to Kaggle datasets
* Download files from Colab directly to local storage
* Control dataset visibility (public/private)

## Installation

```bash
pip install kaggle-colab-bridge
```

## Quick Start

```python
from kaggle_colab_bridge import authenticate, upload_to_kaggle, download_file

# One-time authentication
authenticate()

# Upload to Kaggle
upload_to_kaggle('my_dataset.csv', 'username/my-dataset', private=False)

# Download to local PC
download_file('results/plot.png')
```

## Requirements

* Python >= 3.8
* Google Colab environment (for authentication and download features)
* Kaggle API credentials (for uploading to Kaggle)

## Usage

### Authentication

(Coming soon - detailed usage instructions)

### Uploading to Kaggle

(Coming soon - detailed usage instructions)

### Downloading Files

(Coming soon - detailed usage instructions)

## Roadmap

* [X] Kaggle dataset upload
* [X] File download to local machine
* [X] Clickable authentication
* [ ] Batch file operations
* [ ] HuggingFace support
* [ ] Google Drive integration

## Contributing

This is an early-stage project. Bug reports and feature requests are welcome via GitHub issues.

## License

MIT License

## Author

**ranidzkellou**

---

 **Note** : This is v0.1.0 - early release with Kaggle support. More platforms coming soon!
