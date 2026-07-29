import pytest

from app.exceptions.custom_exceptions import (
    FileValidationException,
    ValidationException,
)
from app.validators.file_validator import FileValidator


class TestDocumentValidator:

    @pytest.fixture
    def validator(self):
        return FileValidator()

    def test_should_accept_valid_pdf(self, validator):
        validator.validate("employee_handbook.pdf", 1024)

    def test_should_accept_valid_docx(self, validator):
        validator.validate("leave_policy.docx", 1024)

    def test_should_accept_valid_txt(self, validator):
        validator.validate("notes.txt", 1024)

    @pytest.mark.parametrize(
        "filename",
        [
            "virus.exe",
            "image.png",
            "archive.zip",
            "music.mp3",
            "script.js",
        ],
    )
    def test_should_raise_exception_for_invalid_extension(
        self,
        validator,
        filename,
    ):
        with pytest.raises(FileValidationException):
            validator.validate(filename, 1024)

    def test_should_raise_exception_when_filename_is_empty(self, validator):

        with pytest.raises(ValidationException):
            validator.validate("", 1024)

    def test_should_raise_exception_when_filename_is_none(self, validator):

        with pytest.raises(ValidationException):
            validator.validate(None, 1024)

    def test_should_raise_exception_when_file_exceeds_max_size(self, validator):

        eleven_mb = 11 * 1024 * 1024

        with pytest.raises(ValidationException):
            validator.validate("policy.pdf", eleven_mb)

    def test_should_accept_file_exactly_at_max_size(self, validator):

        ten_mb = 10 * 1024 * 1024

        validator.validate("policy.pdf", ten_mb)