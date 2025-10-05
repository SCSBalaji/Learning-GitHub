"""
Dataset Module for Loading Images from Folder Structure

This module provides a custom PyTorch Dataset class for loading images
from a folder structure where images are organized by class names.

Expected folder structure:
    root/
        class1/
            image1.jpg
            image2.jpg
        class2/
            image3.jpg
            image4.jpg
"""

import os
from torch.utils.data import Dataset


class ImageFolderDataset(Dataset):
    """
    Custom PyTorch Dataset for loading images from a folder structure.
    
    This dataset automatically scans a root directory to find all image files,
    infers class names from subdirectory names, and creates mappings between
    class names and indices.
    
    Args:
        root_dir (str): Root directory path containing class subdirectories
        
    Attributes:
        root_dir (str): Root directory path
        image_paths (list): List of all image file paths
        labels (list): List of integer labels corresponding to each image
        class_to_idx (dict): Mapping from class name to integer index
        idx_to_class (dict): Mapping from integer index to class name
        classes (list): List of class names
        
    Returns:
        tuple: (image_path, label) where image_path is the path to the image
               and label is the integer class index
    """
    
    # Supported image file extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    def __init__(self, root_dir):
        """
        Initialize the dataset by scanning the root directory.
        
        Args:
            root_dir (str): Path to root directory containing class subdirectories
        """
        self.root_dir = root_dir
        self.image_paths = []
        self.labels = []
        
        # Get all subdirectories (class names) and sort them for consistency
        self.classes = sorted([
            d for d in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, d)) and not d.startswith('.')
        ])
        
        # Create class name to index mapping
        self.class_to_idx = {class_name: idx for idx, class_name in enumerate(self.classes)}
        
        # Create index to class name mapping
        self.idx_to_class = {idx: class_name for class_name, idx in self.class_to_idx.items()}
        
        # Scan all subdirectories for image files
        self._scan_images()
    
    def _scan_images(self):
        """
        Scan the root directory to find all image files and their labels.
        
        This method populates the image_paths and labels lists by walking
        through all class subdirectories and finding valid image files.
        """
        for class_name in self.classes:
            class_dir = os.path.join(self.root_dir, class_name)
            class_idx = self.class_to_idx[class_name]
            
            # Get all files in the class directory
            for filename in os.listdir(class_dir):
                file_path = os.path.join(class_dir, filename)
                
                # Check if it's a file and has a valid image extension
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in self.IMAGE_EXTENSIONS:
                        self.image_paths.append(file_path)
                        self.labels.append(class_idx)
    
    def __len__(self):
        """
        Return the total number of images in the dataset.
        
        Returns:
            int: Total number of images
        """
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        """
        Get an image path and its label by index.
        
        Args:
            idx (int): Index of the item to retrieve
            
        Returns:
            tuple: (image_path, label) where image_path is the full path to the image
                   and label is the integer class index
        """
        if idx < 0 or idx >= len(self):
            raise IndexError(f"Index {idx} out of range for dataset of size {len(self)}")
        
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        return image_path, label
