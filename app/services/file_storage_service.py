import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


class FileStorageService:

    def __init__(self):
        self.upload_directory = Path(settings.UPLOAD_DIRECTORY)
        self.upload_directory.mkdir(parents=True, exist_ok=True)

    def save(self, file: UploadFile):
        """
        Persist the uploaded file to disk.
        Returns the stored file path.
        """

        extension = Path(file.filename).suffix

        stored_filename = f"{uuid.uuid4()}{extension}"

        destination = self.upload_directory / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return destination

    def delete(
        self,
        filename: str,
    ):

        file_path = self.upload_directory / filename

        if file_path.exists():
            file_path.unlink()