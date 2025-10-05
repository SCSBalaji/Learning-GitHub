# Dataset Folder Structure

This directory contains the project datasets organized in a standardized structure.

## Structure

```
data/
└── raw/
    └── DatasetName/
        └── ClassName/
            └── image.jpg
```

## Example

```
data/
└── raw/
    └── PlantVillage/
        ├── TomatoHealthy/
        │   ├── image_0.jpg
        │   ├── image_1.jpg
        │   └── ...
        ├── TomatoEarlyBlight/
        │   ├── image_0.jpg
        │   └── ...
        ├── PotatoHealthy/
        │   └── ...
        └── PotatoLateBlight/
            └── ...
```

## Usage

- Place all raw datasets in the `data/raw/` directory
- Each dataset should have its own folder (e.g., `PlantVillage`)
- Within each dataset folder, organize images by class name
- Each class should be a subfolder containing all images for that class
- Supported image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`

## Sample Dataset

A sample dataset with 4 classes (TomatoHealthy, TomatoEarlyBlight, PotatoHealthy, PotatoLateBlight) has been included for development and testing purposes. Each class contains 5 sample images.
