# Learning-GitHub

## Dataset Loading Implementation

This repository implements a custom PyTorch Dataset class for loading images from a folder structure where images are organized by class names.

### Folder Structure

The dataset follows this structure:
```
data/
└── raw/
    └── DatasetName/
        ├── ClassName1/
        │   ├── image1.jpg
        │   └── image2.jpg
        └── ClassName2/
            ├── image3.jpg
            └── image4.jpg
```

### Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Usage

```python
from dataset import ImageFolderDataset

# Initialize the dataset
dataset = ImageFolderDataset('data/raw/PlantVillage')

# Access dataset properties
print(f"Total images: {len(dataset)}")
print(f"Classes: {dataset.classes}")
print(f"Number of classes: {len(dataset.classes)}")

# Get an item (returns image path and label)
image_path, label = dataset[0]
print(f"Image: {image_path}")
print(f"Label: {label} ({dataset.idx_to_class[label]})")

# Iterate through the dataset
for image_path, label in dataset:
    # Process each image
    pass
```

### Features

- **Automatic class detection**: Automatically infers class names from subdirectory names
- **Class mappings**: Provides `class_to_idx` and `idx_to_class` mappings
- **Multiple image formats**: Supports `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`
- **PyTorch compatible**: Implements PyTorch Dataset interface
- **Well-documented**: Comprehensive docstrings and comments
- **Fully tested**: Includes 12 unit tests with 100% pass rate

### Testing

Run the test suite:
```bash
python test_dataset.py
```

All 12 tests should pass:
- Total images count validation
- Unique classes count validation
- Class name extraction
- Class mapping consistency
- Item retrieval and validation
- Path existence verification
- Label range validation
- Index bounds checking
- Dataset iteration
- Class distribution verification

### Sample Dataset

A sample dataset with 4 plant disease classes is available for testing. See `data/README.md` for details.

### Project Structure

```
.
├── dataset.py           # Custom PyTorch Dataset implementation
├── test_dataset.py      # Unit tests for the Dataset class
├── requirements.txt     # Python dependencies
├── data/
│   ├── README.md        # Dataset folder structure documentation
│   └── raw/
│       └── .gitkeep     # Maintains directory structure
└── README.md            # This file
```
