from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from PIL import Image

# Custom validator to check image context type and file size
def validate_image(image_obj):

    allowed_MIME_types = ["image/jpeg", "image/png"]

    # Maximum permitted file size in MB
    maximum_file_size = 3

    # Use Pillow to check if the image format is one of the one of the
    # allowed_MIME_types and is valid
    #
    # CREDIT: Adapted from Brian - Stack Overflow
    # URL: https://stackoverflow.com/a/266731
    def is_valid_image(obj):
        try:
            image = Image.open(obj)
            for allowed_image_format in allowed_MIME_types:
                if image.format == allowed_image_format[6:].upper():
                    return True
        except OSError:
            return False

    # InMemoryUploadedFile - Used for small files
    # TemporaryUploadedFile - Used for larger files
    if isinstance(image_obj, InMemoryUploadedFile) or isinstance(
        image_obj, TemporaryUploadedFile
    ):

        # Check image file content type is permitted
        if image_obj.content_type not in allowed_MIME_types:
            raise ValidationError(
                "Invalid file type (only valid 'jpg' and 'png' files "
                "permitted)."
            )

        # Check image file doesn't exceed maximum file size
        if image_obj.size > (maximum_file_size * 1024 * 1024):
            raise ValidationError("Maximum file size exceeded (3MB maximum).")

        # Check if image is valid
        if not is_valid_image(image_obj.file):
            raise ValidationError(
                "Upload a valid image. The file you uploaded was either not "
                "an image or a corrupted image."
            )
