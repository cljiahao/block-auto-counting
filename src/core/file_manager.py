import json
from pathlib import Path
from shutil import copyfile, move

from core.directory_manager import directory_manager as dm


class FileManager:
    """A utility class for file management operations"""

    @staticmethod
    def read_txt(file_path: Path) -> str:
        """Reads content from a text file and returns it as a string.

        Args:
            file_path: The path to the text file.

        Returns:
            The content of the file as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If an error occurs while reading the file.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    @staticmethod
    def readlines_txt(file_path: Path) -> str:
        """Reads content from a text file and returns it as a string.

        Args:
            file_path: The path to the text file.

        Returns:
            The content of the file as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If an error occurs while reading the file.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.readlines()
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    @staticmethod
    def write_txt(file_path: Path, content: str) -> None:
        """Writes content to a text file, creating the file if it doesn't exist.

        Args:
            file_path: The path to the text file.
            content: The string content to write to the file.

        Raises:
            IOError: If an error occurs while writing to the file.
        """
        if file_path.suffix != ".txt":
            file_path = file_path.parent / f"{file_path.stem}.txt"
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            raise IOError(f"Failed to write to file {file_path}: {e}")

    @staticmethod
    def read_json(file_path: Path) -> dict[str, any]:
        """Reads a JSON file and returns its content as a dictionary.

        Args:
            file_path: The path to the JSON file.

        Returns:
            The content of the file as a dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the JSON is invalid.
            IOError: If an error occurs while reading the file.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from file {file_path}: {e}")
        except Exception as e:
            raise IOError(f"Failed to read JSON file {file_path}: {e}")

    @staticmethod
    def write_json(file_path: Path, content: dict) -> None:
        """Writes a dictionary to a JSON file, creating the file if it doesn't exist.

        Args:
            file_path: The path to the JSON file.
            content: The dictionary content to write to the file.

        Raises:
            IOError: If an error occurs while writing to the file.
        """
        if file_path.suffix != ".json":
            file_path = file_path.parent / f"{file_path.stem}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(content, file, indent=4)
        except Exception as e:
            raise IOError(f"Failed to write JSON to file {file_path}: {e}")

    @staticmethod
    def copy_files_to_dir(
        dst_path: Path, src_file_paths: list[Path], remove: bool = False
    ) -> None:
        """Copies files to the destination directory, with optional removal of the existing destination.

        Args:
            dst_path: The destination directory path.
            src_file_paths: A list of source file paths.
            remove: If True, remove the destination directory before copying.
        """
        dm.create_directory(dst_path, remove)
        for file_path in src_file_paths:
            copyfile(file_path, dst_path / file_path.name)

    @staticmethod
    def move_files_to_dir(
        dst_path: Path, src_file_paths: list[Path], remove: bool = False
    ) -> None:
        """Moves files to the destination directory, with optional removal of the existing destination.

        Args:
            dst_path: The destination directory path.
            src_file_paths: A list of source file paths.
            remove: If True, remove the destination directory before moving.
        """
        dm.create_directory(dst_path, remove)
        for file_path in src_file_paths:
            move(file_path, dst_path / file_path.name)
