from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)

# Custom validator to check image context type and file size
def validate_image(image_obj):
    file = image_obj.file

    # Maximum permitted file size in bytes (3MB)
    maximum_file_size = 20 * 1024 * 1024

    # InMemoryUploadedFile - Used for small files
    # TemporaryUploadedFile - Used for larger files
    if isinstance(file, InMemoryUploadedFile) or isinstance(
        file, TemporaryUploadedFile
    ):
        # Check image file content type is permitted
        if file.content_type not in [
            "image/jpeg",
            "image/png",
        ]:
            raise ValidationError(
                "Invalid file type (only valid 'jpg' and 'png' files permitted)."
            )

        # Check image file doesn't exceed maximum file size
        if file.size > maximum_file_size:
            raise ValidationError("Maximum file size exceeded (3MB maximum).")
