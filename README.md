# Learning-GitHub

# Azure Image Sorting Application

## 📜 Project Overview
This project uses **Azure Cognitive Services** and **Azure Blob Storage** to classify and organize images into categories like flowers, deserts, fruits, etc., based on their content. It employs the **Computer Vision API** for image analysis and Blob Storage for storing and managing images.

---

## 🚀 Features
- Automatically classifies images into predefined categories.
- Organizes classified images into separate Blob Storage containers.
- Uses a SAS token for secure access.
- Fully scalable and easy to integrate into other projects.

---

## 🛠️ Technologies Used
- **Azure Cognitive Services (Computer Vision API)** for image analysis.
- **Azure Blob Storage** for storing and organizing images.
- **Python** for scripting and automation.
- **Azure CLI** and **Azure Storage Explorer** for resource management.

---

## 📋 Steps to Implement

### 1. **Setup Azure Resources**
1. Created an **Azure for Students** subscription.
2. Created a **Resource Group**: `ImageSortProjectRG`.
3. Created a **Storage Account**: `imagesorter123`.
4. Created Blob Storage containers:
   - `raw-images` (for unprocessed images)
   - `flowers`, `deserts`, `fruits`, `others` (for categorized images)
5. Created an **Azure Cognitive Services Resource**: `ImageSortVision`.

### 2. **Prepare Local Environment**
1. Installed Python 3.x.
2. Installed required Python packages:
   ```bash
   pip install azure-cognitiveservices-vision-computervision azure-storage-blob msrest
