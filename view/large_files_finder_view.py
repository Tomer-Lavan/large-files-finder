import tkinter as tk
from tkinter import filedialog, ttk
import os
from typing import Tuple, List


class LargeFilesFinderView(tk.Tk):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.title("File Size Viewer")
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(padx=10, pady=5)

        self.folder_frame = tk.Frame(self.top_frame)
        self.folder_frame.pack(side=tk.LEFT, padx=10)

        self.num_files_frame = tk.Frame(self.top_frame)
        self.num_files_frame.pack(side=tk.LEFT, padx=10)

        self.folder_path_label = tk.Label(
            self.folder_frame, text="Folder: Not selected")
        self.folder_path_label.pack()

        self.choose_button = tk.Button(
            self.folder_frame, text="Choose Folder", command=self.presenter.choose_folder)
        self.choose_button.pack()

        self.num_files_label = tk.Label(
            self.num_files_frame, text="Number of files:")
        self.num_files_label.pack(side=tk.LEFT)

        self.num_files_entry = tk.Entry(self.num_files_frame)
        self.num_files_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(
            self, text="Search", command=self.presenter.start_search)
        self.search_button.pack(pady=2)

        self.loading_label = tk.Label(self, text="")
        self.loading_label.pack()

        self.duration_frame = tk.Frame(self)
        self.duration_frame.pack(padx=2, pady=1, fill=tk.X)

        self.duration_label = tk.Label(
            self.duration_frame, text="Duration: 0 seconds")
        self.duration_label.pack(side=tk.RIGHT)

        self.file_list_frame = tk.Frame(self)
        self.file_list = ttk.Treeview(self.file_list_frame, columns=(
            "File Name", "Size", "Last Modified"), show="headings")
        for col in ("File Name", "Size", "Last Modified"):
            self.file_list.heading(col, text=col)
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_list.bind('<Double-1>', self.open_file_folder)

        self.scrollbar = ttk.Scrollbar(
            self.file_list_frame, orient=tk.VERTICAL, command=self.file_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list.configure(yscrollcommand=self.scrollbar.set)

        self.file_list_frame.pack(fill=tk.BOTH, expand=True)

    def format_duration(self, seconds: float):
        if seconds < 60:
            return f"{round(seconds)} seconds"
        elif seconds < 3600:
            return f"{round(seconds / 60)} minutes"
        else:
            return f"{round(seconds / 3600)} hours"

    def update_file_list(self, sorted_files: List[Tuple[str, str, str]], duration: float):
        self.file_list.delete(*self.file_list.get_children())
        for file, size, mtime in sorted_files:
            self.file_list.insert('', 'end', values=(file, size, mtime))
        self.duration_label.config(
            text=f"Duration: {self.format_duration(duration)}")

    def set_folder_path(self, folder_path: str):
        self.folder_path_label.config(text=f"Folder: {folder_path}")

    def set_process_duration(self, folder_path: str):
        self.folder_path_label.config(text=f"Folder: {folder_path}")

    def show_loading(self, loading: bool):
        self.loading_label.config(text="Loading..." if loading else "")

    def show_message(self, title: str, message: str):
        tk.messagebox.showinfo(title, message)

    def open_file_folder(self, event):
        selected_item = self.file_list.selection()[0]
        file_path = self.file_list.item(selected_item, 'values')[0]
        folder_path = os.path.dirname(file_path)
        os.startfile(folder_path)
