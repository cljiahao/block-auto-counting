from pathlib import Path
from shutil import rmtree


class DirectoryManager:
    """Handles directory structure and ensures required folders exist."""

    def __init__(self) -> None:
        """Initialize directory paths and ensure required folders exist."""
        self.base_dir = Path(__file__).resolve().parent.parent.parent

        # Log folder
        self.log_dir = self.base_dir / "log"

        # Config folder
        self.config_dir = self.base_dir / "config"
        self.json_dir = self.config_dir / "json"

        # Data folder
        self.data_dir = self.base_dir / "data"
        self.images_dir = self.data_dir / "images"
        self.accuracy_dir = self.images_dir / "accuracy"
        self.block_dir = self.images_dir / "block"
        self.trouble_dir = self.images_dir / "trouble"
        self.excel_dir = self.data_dir / "excel"
        self.prass_dir = self.data_dir / "prass"

        self._initialize_base_folders()

    def _initialize_base_folders(self) -> None:
        """Initialize base required directory paths."""
        folders = [
            self.log_dir,
            self.images_dir,
            self.accuracy_dir,
            self.block_dir,
            self.trouble_dir,
            self.excel_dir,
            self.prass_dir,
        ]
        for folder in folders:
            self.create_directory(folder)

    def create_directory(self, folder_path: Path, to_remove: bool = False) -> None:
        """
        Helper method to ensure the destination directory exists, and remove it if necessary.

        Args:
            folder_path: The path to the directory.
            to_remove: If True, remove the directory before creating it.
        """
        if to_remove and folder_path.exists():
            try:
                rmtree(folder_path)
            except Exception as e:
                raise OSError(
                    f"Failed to remove existing directory: {folder_path}"
                ) from e

        try:
            folder_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise OSError(f"Failed to create directory: {folder_path}") from e

    def list_png_paths(self, folder_path: Path) -> list[Path]:
        """
        Returns a list of all .png files in the given directory.

        Args:
            folder_path: The path to the directory.

        Returns:
            A list of Path objects for .png files.

        Raises:
            FileNotFoundError: If the directory does not exist.
            ValueError: If the path is not a directory.
        """
        if not folder_path.exists():
            raise FileNotFoundError(f"Directory not found: {folder_path}")

        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")

        return list(folder_path.glob("*.png"))


directory_manager = DirectoryManager()
