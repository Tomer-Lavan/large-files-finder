from tkinter import filedialog
import tkinter as tk
import threading
import time
from view.large_files_finder_view import LargeFilesFinderView
from model.large_files_finder_model import LargeFilesFinderModel


class LargeFilesFinderPresenter:
    def __init__(self, view: LargeFilesFinderView, model: LargeFilesFinderModel):
        self.view = view
        self.model = model

    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.model.folder_path = folder_path
            self.view.set_folder_path(folder_path)

    def start_search(self):
        if self.model.folder_path:
            try:
                num_files = int(self.view.num_files_entry.get())
                if num_files > 1500:
                    self.view.show_message(
                        "Info", "Maximum number of files is 1500.")
                    num_files = 1500
                    self.view.num_files_entry.delete(0, tk.END)
                    self.view.num_files_entry.insert(0, "1500")
            except ValueError:
                self.view.show_message(
                    "Info", "Must choose number of files")
                num_files = None
                return
            threading.Thread(target=self.update_file_list, args=(
                self.model.folder_path, num_files)).start()
        else:
            self.view.show_message("Error", "Please choose a folder first.")

    def update_file_list(self, folder_path: str, n=100):
        self.view.show_loading(True)
        start_time = time.time()
        sorted_files = self.model.get_sorted_file_list(folder_path, n)
        duration = time.time() - start_time
        self.view.update_file_list(sorted_files, duration)
        self.view.show_loading(False)
