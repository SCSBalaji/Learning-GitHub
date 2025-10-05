"""
Test Suite for ImageFolderDataset

This module contains unit tests to verify the functionality of the
ImageFolderDataset class.
"""

import unittest
import os
from dataset import ImageFolderDataset


class TestImageFolderDataset(unittest.TestCase):
    """Test cases for ImageFolderDataset class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by all test methods."""
        cls.test_data_path = 'data/raw/PlantVillage'
        cls.expected_classes = 4
        cls.expected_total_images = 20
        cls.expected_images_per_class = 5
    
    def setUp(self):
        """Set up test dataset instance before each test."""
        self.dataset = ImageFolderDataset(self.test_data_path)
    
    def test_total_images_count(self):
        """Test that the dataset finds the correct total number of images."""
        self.assertEqual(
            len(self.dataset),
            self.expected_total_images,
            f"Expected {self.expected_total_images} images, but found {len(self.dataset)}"
        )
    
    def test_unique_classes_count(self):
        """Test that the dataset finds the correct number of unique classes."""
        self.assertEqual(
            len(self.dataset.classes),
            self.expected_classes,
            f"Expected {self.expected_classes} classes, but found {len(self.dataset.classes)}"
        )
        
        # Also verify that class_to_idx and idx_to_class have the same length
        self.assertEqual(
            len(self.dataset.class_to_idx),
            self.expected_classes,
            "class_to_idx mapping has incorrect length"
        )
        self.assertEqual(
            len(self.dataset.idx_to_class),
            self.expected_classes,
            "idx_to_class mapping has incorrect length"
        )
    
    def test_class_names(self):
        """Test that class names are correctly extracted from directory structure."""
        expected_class_names = ['PotatoHealthy', 'PotatoLateBlight', 
                               'TomatoEarlyBlight', 'TomatoHealthy']
        self.assertEqual(
            sorted(self.dataset.classes),
            sorted(expected_class_names),
            "Class names do not match expected values"
        )
    
    def test_class_mappings(self):
        """Test that class_to_idx and idx_to_class mappings are consistent."""
        # Verify that mappings are inverse of each other
        for class_name, idx in self.dataset.class_to_idx.items():
            self.assertEqual(
                self.dataset.idx_to_class[idx],
                class_name,
                f"Inconsistent mapping for class {class_name}"
            )
    
    def test_getitem_returns_correct_type(self):
        """Test that __getitem__ returns a tuple of (path, label)."""
        image_path, label = self.dataset[0]
        
        # Check types
        self.assertIsInstance(image_path, str, "Image path should be a string")
        self.assertIsInstance(label, int, "Label should be an integer")
    
    def test_getitem_path_exists(self):
        """Test that returned image paths exist."""
        for i in range(min(5, len(self.dataset))):
            image_path, label = self.dataset[i]
            self.assertTrue(
                os.path.exists(image_path),
                f"Image path {image_path} does not exist"
            )
    
    def test_getitem_label_in_range(self):
        """Test that labels are within valid range."""
        for i in range(len(self.dataset)):
            image_path, label = self.dataset[i]
            self.assertGreaterEqual(
                label, 0,
                f"Label {label} is less than 0"
            )
            self.assertLess(
                label, len(self.dataset.classes),
                f"Label {label} is >= number of classes {len(self.dataset.classes)}"
            )
    
    def test_specific_item_retrieval(self):
        """Test fetching specific items and verify path and label correctness."""
        # Get the first item
        image_path, label = self.dataset[0]
        
        # Verify the path contains one of the class directories
        class_name = self.dataset.idx_to_class[label]
        self.assertIn(
            class_name,
            image_path,
            f"Image path {image_path} should contain class name {class_name}"
        )
        
        # Verify the image file has a valid extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        _, ext = os.path.splitext(image_path)
        self.assertIn(
            ext.lower(),
            valid_extensions,
            f"Image extension {ext} is not valid"
        )
    
    def test_index_out_of_bounds(self):
        """Test that accessing invalid indices raises IndexError."""
        with self.assertRaises(IndexError):
            _ = self.dataset[len(self.dataset)]
        
        with self.assertRaises(IndexError):
            _ = self.dataset[-len(self.dataset) - 1]
    
    def test_all_images_have_labels(self):
        """Test that every image has a corresponding label."""
        self.assertEqual(
            len(self.dataset.image_paths),
            len(self.dataset.labels),
            "Number of image paths and labels should be equal"
        )


class TestImageFolderDatasetIntegration(unittest.TestCase):
    """Integration tests for ImageFolderDataset."""
    
    def test_iterate_through_dataset(self):
        """Test that we can iterate through the entire dataset."""
        dataset = ImageFolderDataset('data/raw/PlantVillage')
        
        image_count = 0
        for image_path, label in dataset:
            image_count += 1
            self.assertTrue(os.path.exists(image_path))
            self.assertIsInstance(label, int)
        
        self.assertEqual(
            image_count,
            len(dataset),
            "Number of iterations should equal dataset length"
        )
    
    def test_class_distribution(self):
        """Test that images are distributed across all classes."""
        dataset = ImageFolderDataset('data/raw/PlantVillage')
        
        # Count images per class
        class_counts = {idx: 0 for idx in range(len(dataset.classes))}
        for _, label in dataset:
            class_counts[label] += 1
        
        # Verify all classes have at least one image
        for class_idx, count in class_counts.items():
            self.assertGreater(
                count, 0,
                f"Class {dataset.idx_to_class[class_idx]} has no images"
            )


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
