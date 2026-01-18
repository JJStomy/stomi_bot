import os
from .paths import Paths

class FileManager:

    @staticmethod
    def read_file(path: Paths, file_name: str) -> str:
        if file_name.count('.') == 0:
            file_name += ".txt"

        file_path = os.path.join(path.value, file_name)

        with open(file_path, "r", encoding="UTF-8") as file:
            return file.read()