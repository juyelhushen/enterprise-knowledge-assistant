from pathlib import Path

from app.core.config import settings
from app.exceptions.custom_exceptions import ValidationException


class FileValidator:

    def validate_filename(
            self,
            filename: str,
    ) -> None:
        """
        Validates the uploaded filename
        """

        if not filename:
            raise ValidationException("Filename is required")

        extension = Path(filename).suffix.lower().replace(".","")

        if extension not in settings.ALLOWED_EXTENSIONS:
            raise ValidationException(
                f"Unsupported file type: {extension}"
            )

    def validate_size(self, size:int) -> None:
        """
        Validates the uploaded size
        """
        
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if size > max_bytes:
            raise ValidationException(f"File exceeds {settings.MAX_UPLOAD_SIZE_MB} MB.")

    def validate(self, filename: str, size: int) -> None:
        """
        Performs complete validation.
        """

        self.validate_filename(filename)
        self.validate_size(size)