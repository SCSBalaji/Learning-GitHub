# End-to-End Data Pipeline Sprint Backlog

This document contains the complete sprint backlog for the data preparation and preprocessing pipeline. It covers all tasks from dataset download, preprocessing, transformations, normalization, batching, splitting, augmentations, and visualization.

---

## 1. Dataset Download & Extraction

### Phase 1: Research & Setup
- [ ] Research and collect the direct, stable download URLs for all required datasets (Plant Village, CCMT, Sugarcane, Coconut).
- [ ] Create a configuration file (e.g., Python dictionary or JSON) to store dataset names, URLs, and expected compressed filenames.
- [ ] Add necessary libraries like `requests` and `tqdm` to the `requirements.txt` file.

### Phase 2: Implementation 💻
- [ ] Create a new Python script for this task (e.g., `download_data.py`).
- [ ] Implement a function that downloads a file from a URL, using `tqdm` for a live progress bar.
- [ ] Add logic to check if the dataset's destination folder or the compressed file already exists, and skip download if present.
- [ ] Implement a function to extract compressed files (.zip, .tar.gz).
- [ ] Write main script logic that reads the configuration, iterates through each dataset, and calls download/extraction functions.
- [ ] Automatically delete compressed files after extraction to save disk space.

### Phase 3: Testing & Validation ✅
- [ ] Run the script to download and extract a smaller dataset.
- [ ] Verify the progress bar displays correctly.
- [ ] Check that datasets are extracted into the correct folder structure.
- [ ] Confirm compressed files are removed after extraction.
- [ ] Run the script a second time to ensure existing data is correctly detected and skipped.

### Phase 4: Review & Finalization 📝
- [ ] Add comments and a docstring explaining how to run the script and add new datasets.
- [ ] Create a Pull Request (PR) with the new script and configuration file.
- [ ] Conduct a code review with a team member.
- [ ] Merge the approved PR into the main branch.

---

## 2. Loading Raw Dataset

### Phase 1: Setup & Preparation
- [ ] Define and document the official project-wide dataset folder structure (e.g., `data/raw/DatasetName/ClassName/image.jpg`).
- [ ] Download a small representative sample of a dataset (3–4 classes) for development/testing.
- [ ] Organize this sample dataset into the agreed-upon folder structure.

### Phase 2: Implementation 💻
- [ ] Create a new Python script for dataset handling (e.g., `dataset.py`).
- [ ] Implement a custom PyTorch Dataset class with core data loading logic.
- [ ] In `__init__`, scan the root directory for all image file paths.
- [ ] Automatically infer class names from sub-directory names.
- [ ] Create mappings: `class_name_to_index` and `index_to_class_name`.
- [ ] Implement `__len__` to return the total number of images.
- [ ] Implement `__getitem__` to return image path and its integer label for a given index.

### Phase 3: Testing & Validation ✅
- [ ] Create a test script (e.g., `test_dataset.py`) to verify the Dataset class.
- [ ] Unit test: initialize Dataset with sample data and assert total images count.
- [ ] Unit test: assert total number of unique classes.
- [ ] Unit test: fetch sample items and assert correct image path and label index.

### Phase 4: Review & Finalization 📝
- [ ] Add comments and docstrings explaining the Dataset class purpose and methods.
- [ ] Create a PR with `dataset.py` and `test_dataset.py`.
- [ ] Conduct a code review with a team member.
- [ ] Merge the approved PR into the main branch.

---

## 3. Image Transformations

### Phase 1: Implementation 💻
- [ ] Add `torchvision` and `Pillow` to `requirements.txt`.
- [ ] Import necessary modules in `dataset.py`.
- [ ] Create a transformation pipeline: `Resize((224,224))` → `ToTensor()`.
- [ ] Modify `__getitem__` to open images using `PIL.Image.open`.
- [ ] Apply the transformation pipeline to images.
- [ ] Return processed image tensor and label instead of file path.

### Phase 2: Testing & Validation ✅
- [ ] Update `test_dataset.py` to reflect new output.
- [ ] Fetch a sample item and assert it returns a `torch.Tensor`.
- [ ] Verify tensor shape is `(3, 224, 224)`.
- [ ] Assert pixel values scaled to [0,1].

### Phase 3: Review & Finalization 📝
- [ ] Update Dataset docstrings to specify it returns processed tensors.
- [ ] Create a PR and conduct code review.
- [ ] Merge approved PR.

---

## 4. Image Normalization

### Phase 1: Implementation 💻
- [ ] Add `transforms.Normalize` to the pipeline after `ToTensor`.
- [ ] Use ImageNet mean `(0.485,0.456,0.406)` and std `(0.229,0.224,0.225)`.

### Phase 2: Testing & Validation ✅
- [ ] Update `test_dataset.py` to verify normalization.
- [ ] Assert pixel values are no longer strictly in [0,1].
- [ ] Optional: assert normalized tensor mean ~0.

### Phase 3: Review & Finalization 📝
- [ ] Update docstrings to reflect normalized tensors.
- [ ] Create PR, conduct review, and merge.

---

## 5. DataLoader & Batching

### Phase 1: Implementation 💻
- [ ] Import `torch.utils.data.DataLoader`.
- [ ] Create a function that takes a Dataset and returns a DataLoader.
- [ ] Set configurable `batch_size` and `shuffle` parameters.
- [ ] Set `num_workers` for parallel loading.
- [ ] Ensure DataLoader returns batches `(image_tensor, label)`.

### Phase 2: Testing & Validation ✅
- [ ] Create/Update test script to validate DataLoader.
- [ ] Fetch a batch and assert shapes: images `(batch_size,3,224,224)`, labels `(batch_size,)`.
- [ ] Verify multiple iterations produce different batches with `shuffle=True`.

### Phase 3: Review & Finalization 📝
- [ ] Add docstrings and comments.
- [ ] Create PR, conduct review, merge approved PR.

---

## 6. Train/Validation/Test Split

### Phase 1: Implementation 💻
- [ ] Use `prepare_dataset.py` to handle splitting.
- [ ] Create label list for stratification.
- [ ] Use `sklearn.model_selection.train_test_split` with `stratify=y`.
- [ ] Apply stratification for both train/temp and temp/val-test splits.

### Phase 2: Testing & Validation ✅
- [ ] Calculate class distribution in original dataset.
- [ ] After split, calculate distributions in train/val/test folders.
- [ ] Assert distributions are approximately preserved.

### Phase 3: Review & Finalization 📝
- [ ] Add comments explaining `stratify`.
- [ ] Create PR, review, merge.

---

## 7. Augmentations

### Phase 1: Implementation 💻
- [ ] Add `albumentations` to `requirements.txt`.
- [ ] Define separate pipelines: training and validation/test.
- [ ] Training pipeline includes: Horizontal Flip, Random 90° Rotation, Shift/Scale/Rotate, Random Gamma/Brightness/Contrast, RGB Shift, CLAHE, Resize, ToTensor, Normalize.
- [ ] Validation/test pipeline: Resize, ToTensor, Normalize.
- [ ] Apply augmentation-rich pipeline only to training Dataset.

### Phase 2: Testing & Visualization ✅
- [ ] Create `visualize_augmentations.py`.
- [ ] Apply training pipeline multiple times on the same image.
- [ ] Display a grid (e.g., 4x4) to confirm augmentations.

### Phase 3: Review & Finalization 📝
- [ ] Add comments to distinguish pipelines.
- [ ] Create PR, review, merge.

---

## 8. DataLoader Shuffle Verification

### Phase 1: Implementation 💻
- [ ] Set `shuffle=True` for training DataLoader.
- [ ] Set `shuffle=False` for validation/test DataLoader.

### Phase 2: Testing & Validation ✅
- [ ] Unit test: iterate training DataLoader twice, assert order changes.
- [ ] Unit test: iterate validation/test DataLoader twice, assert order is same.

### Phase 3: Review & Finalization 📝
- [ ] Add comment explaining shuffle importance.
- [ ] Create PR, review, merge.

---

## 9. Visualization of Data

### Phase 1: Implementation 💻
- [ ] Add `matplotlib` to `requirements.txt`.
- [ ] Create `visualize_data.py`.
- [ ] Function accepts a DataLoader, retrieves a batch.
- [ ] De-normalize images and arrange into a grid with `torchvision.utils.make_grid`.
- [ ] Display images with `matplotlib.pyplot` including class labels.

### Phase 2: Testing & Validation ✅
- [ ] Run script on training DataLoader with augmentations.
- [ ] Visually confirm augmentations are applied randomly.
- [ ] Optional: run on validation DataLoader, confirm no augmentations.

## 9. Visualization of Data (continued)

### Phase 3: Review & Finalization 📝
- [ ] Add a clear docstring and comments to the script explaining its purpose and usage.
- [ ] Create a Pull Request (PR) with the new visualization script.
- [ ] Conduct a code review with a team member to ensure the de-normalization logic is correct and the plot is clear and informative.
- [ ] Merge the approved Pull Request into the main development branch.

---

## 10. Streaming Download with Progress Bar

### Phase 1: Implementation 💻
- [ ] Locate the `download_data.py` script and the specific function responsible for downloading files.
- [ ] Modify the file download request (e.g., using `requests`) to enable streaming mode (`stream=True`).
- [ ] Get the total file size from the response headers to set the total for the progress bar.
- [ ] Initialize a `tqdm` progress bar instance before starting the download, passing the total file size to it.
- [ ] Write a loop to download the file in chunks and write each chunk to the local file.
- [ ] Inside the loop, update the `tqdm` progress bar with the size of the chunk just downloaded.

### Phase 2: Testing & Validation ✅
- [ ] Run the updated script to download a dataset file that is large enough to see the progress bar in action.
- [ ] Confirm that a progress bar is displayed in the terminal during the download process.
- [ ] Visually verify that the progress bar correctly updates and proceeds from 0% to 100%.
- [ ] After the download is complete, confirm that the resulting file is complete and not corrupted.

### Phase 3: Review & Finalization 📝
- [ ] Add a comment to the download function explaining the streaming logic and `tqdm` integration.
- [ ] Create a Pull Request (PR) with the updated script.
- [ ] Conduct a code review with a team member to ensure the streaming download is implemented correctly and efficiently.
- [ ] Merge the approved Pull Request into the main development branch.

---

# Notes

- Each user story is broken into **Implementation**, **Testing & Validation**, and **Review & Finalization** phases.
- All tasks are designed to be clear and actionable for any team member.
- PRs should always be reviewed by at least one other team member to ensure code quality and correctness.
- This backlog covers **all tasks from dataset download to preprocessing, augmentation, batching, splitting, normalization, and visualization**.
