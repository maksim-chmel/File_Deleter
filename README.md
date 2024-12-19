# Secure File Deleter

Secure File Deleter is an application designed to securely delete files and folders from your computer. It uses data overwrite methods before deletion to prevent file recovery.

## Features

- Secure file deletion with data overwrite.
- Drag-and-drop support for easy file and folder selection.
- Simple interface for selecting files and folders to delete.
- Option to cancel selection.

## Security

Your data security is crucial, and regular file deletion methods (like moving to the recycle bin) don’t ensure that your data is gone for good. Secure File Deleter uses advanced techniques to guarantee **complete and irreversible deletion** of your files.

### 1. **Data Overwriting**

Instead of just deleting files, Secure File Deleter overwrites the data multiple times with random information, making recovery impossible. 

- **Overwrite cycles**: 7 overwrite passes ensure that files are effectively destroyed.
- **Block size**: Data is overwritten in small blocks to fully erase all traces of the file.

### 2. **File Renaming Before Deletion**

To further protect your data, files are renamed to a random string before deletion. This prevents file recovery tools from locating and restoring the deleted files by name.

- **Random filenames**: Each file is renamed to a 16-character random string, making recovery extremely difficult.

### 3. **Folder Deletion**

The app recursively deletes all files and subfolders within a folder, ensuring complete destruction of data before the folder is removed.

### 4. **Using Standard Security Practices**

Secure File Deleter relies on trusted, system-level tools to interact with files, ensuring reliable and error-free deletion. This minimizes risks and enhances the security of your data destruction process.

---

### Why It Matters

Deleted files can still be recovered, especially on SSDs, using basic recovery tools. Secure File Deleter ensures that once a file is deleted, it is **gone for good**. This is essential when dealing with sensitive or confidential data, giving you peace of mind knowing your files are securely erased.

This project is open-source and licensed under the Apache License Version 2.0.
