import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from threading import Thread
import gc
class SecureFileDeleterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Deleter")
        self.root.geometry("400x300")

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_event)

        self.label = tk.Label(root, text="Drag files or folders here\nor select them using the buttons below", font=("Arial", 12), justify="center")
        self.label.pack(pady=5)

        self.select_file_button = tk.Button(root, text="Select File", command=self.select_file, font=("Arial", 12))
        self.select_file_button.pack(pady=2)

        self.select_folder_button = tk.Button(root, text="Select Folder", command=self.select_folder, font=("Arial", 12))
        self.select_folder_button.pack(pady=2)

        self.cancel_button = tk.Button(root, text="Cancel Selection", command=self.cancel_selection, font=("Arial", 12), state="disabled")
        self.cancel_button.pack(pady=2)

        self.delete_button = tk.Button(root, text="Delete Files/Folders", command=self.confirm_and_start_deletion, font=("Arial", 12), state="disabled")
        self.delete_button.pack(pady=5)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

        self.log_text = tk.Text(root, height=6, state="disabled", wrap="word", font=("Arial", 12))
        self.log_text.pack(pady=5)

        self.paths = []

    def log_message(self, message):

        self.log_text["state"] = "normal"
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text["state"] = "disabled"

    def select_file(self):

        paths = filedialog.askopenfilenames(title="Select Files for Deletion")
        if paths:
            self.paths.extend(paths)
            for path in paths:
                self.log_message(f"Added for deletion: {path}")
            self.update_selection_status()

    def select_folder(self):

        folder_path = filedialog.askdirectory(title="Select Folder for Deletion")
        if folder_path:
            self.paths.append(folder_path)
            self.log_message(f"Added for deletion: {folder_path}")
            self.update_selection_status()

    def drop_event(self, event):

        dropped_paths = self.root.tk.splitlist(event.data)
        self.paths.extend(dropped_paths)
        for path in dropped_paths:
            self.log_message(f"Added for deletion: {path}")
        self.update_selection_status()

    def update_selection_status(self):

        self.label.config(text=f"Selected items: {len(self.paths)}")
        self.delete_button["state"] = "normal"
        self.cancel_button["state"] = "normal"

    def cancel_selection(self):

        canceled_paths = self.paths[:]
        self.paths.clear()
        for path in canceled_paths:
            self.log_message(f"Selection canceled for: {path}")
        self.label.config(text="Drag files or folders here\nor select them using the buttons below")
        self.delete_button["state"] = "disabled"
        self.cancel_button["state"] = "disabled"

    def confirm_and_start_deletion(self):

        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected files/folders? This action is irreversible.")
        if confirm:
            self.start_deletion_thread()
        else:
            self.log_message("Deletion canceled by user.")

    def start_deletion_thread(self):

        self.delete_button["state"] = "disabled"
        self.log_message("Starting deletion...")
        Thread(target=self.delete_files_or_folders).start()

    def delete_files_or_folders(self):

        total_items = len(self.paths)
        completed = 0

        for path in self.paths:
            try:
                if os.path.isfile(path):
                    self.secure_delete(path)
                    self.log_message(f"Deleted: {path}")
                elif os.path.isdir(path):
                    self.delete_folder(path)
                    self.log_message(f"Deleted folder: {path}")
            except Exception as e:
                self.log_message(f"Error deleting {path}: {str(e)}")

            completed += 1
            self.progress_bar["value"] = (completed / total_items) * 100
            self.root.update_idletasks()
            gc.collect()

        self.log_message("Deletion complete.")
        self.label.config(text="Select files or folders for deletion")
        self.progress_bar["value"] = 0
        self.delete_button["state"] = "normal"
        self.cancel_button["state"] = "disabled"
        self.paths = []

    def secure_delete(self, file_path):

        with open(file_path, "ba+") as file:
            length = file.tell()
            passes = 7
            chunk_size = max(4096, length // 100)

            for _ in range(passes):
                file.seek(0)
                written = 0

                while written < length:
                    write_size = min(chunk_size, length - written)
                    file.write(os.urandom(write_size))
                    written += write_size


        random_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
        new_path = os.path.join(os.path.dirname(file_path), random_name)
        os.rename(file_path, new_path)

        os.remove(new_path)


        gc.collect()

    def delete_folder(self, folder_path):

        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                self.secure_delete(file_path)
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(folder_path)
        gc.collect()


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SecureFileDeleterApp(root)
    root.mainloop()