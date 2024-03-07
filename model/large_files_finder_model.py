import os
import heapq
from concurrent.futures import ThreadPoolExecutor
import datetime
from typing import Tuple, List


class LargeFilesFinderModel:
    def __init__(self):
        self.folder_path = None

    def get_folders_files(self, path: str):
        folders = []
        files = []
        for root, dirs, filenames in os.walk(path):
            for directory in dirs:
                folders.append(os.path.join(root, directory))
            for filename in filenames:
                files.append(os.path.join(root, filename))
            break
        return folders, files

    def get_sorted_file_list(self, folder_path: str, n=100) -> List[Tuple[str, str, str]]:
        file_heap = []

        def process_file(entry):
            file_size = entry.stat().st_size
            file_mtime = entry.stat().st_mtime

            if len(file_heap) < n:
                heapq.heappush(
                    file_heap, (file_size, entry.path, file_mtime))
            else:
                heapq.heappushpop(
                    file_heap, (file_size, entry.path, file_mtime))

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for root, dirs, files in os.walk(folder_path, topdown=True, followlinks=False):
                with os.scandir(root) as it:
                    for entry in it:
                        if entry.is_file():
                            executor.submit(process_file, entry)

        return [(path, self.format_size(size), self.format_timestamp(mtime)) for size, path, mtime in [heapq.heappop(file_heap) for _ in range(len(file_heap))]][::-1]

    def format_timestamp(self, timestamp: float) -> str:
        date = datetime.datetime.fromtimestamp(timestamp)
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def format_size(self, size: float) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
