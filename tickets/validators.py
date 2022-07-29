"""Custom validators for tickets application"""


from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from django.utils.html import strip_tags
from PIL import Image


def validate_image(image_obj):
    """Validator to check image context type and file size"""

    # Allowed image file types (based on image MIME types)
    allowed_MIME_types = ["jpeg", "png"]

    # Maximum permitted file size in MB
    maximum_file_size = 3

    # CREDIT: Adapted from Brian - Stack Overflow
    # URL: https://stackoverflow.com/a/266731
    def is_valid_image(obj):
        """Return bool value or raise ValidationErrors based on result of using
        the Pillow package to check if the image format is one of the one of
        the allowed_MIME_types and is a valid image file.
        """
        try:
            # Check each image to see if its format is one of the allowed
            # types.
            image = Image.open(obj)
            for allowed_image_format in allowed_MIME_types:
                if image.format == allowed_image_format.upper():
                    return True
            else:
                # If the file is not an allowed type, a ValidationError is
                # raised to feed this back to the user.
                raise ValidationError(
                    "Invalid file type (only valid 'jpg' and 'png' files "
                    "permitted)."
                )
        # If the file cannot be read an OSError exception with is thrown,
        # caught and a ValidationError raised in its place to notify the user.
        except OSError:
            raise ValidationError(
                "Upload a valid image. The file you uploaded was either not "
                "an image or a corrupted image."
            )

    # InMemoryUploadedFile - Used for small files
    # TemporaryUploadedFile - Used for larger files
    if isinstance(image_obj, InMemoryUploadedFile) or isinstance(
        image_obj, TemporaryUploadedFile
    ):

        # Check image file doesn't exceed maximum file size
        if image_obj.size > (maximum_file_size * 1024 * 1024):
            raise ValidationError("Maximum file size exceeded (3MB maximum).")

        # Check if image is of an allowed type an is a valid image
        is_valid_image(image_obj.file)


def textfield_not_empty(textfield):
    """
    Validator to ensure the ticket description TextField doesn't start with
    whitespace.
    """
    # Strip HTML tags and replace non-breaking spaces
    cleaned_data = strip_tags(textfield).replace("&nbsp;", " ")
    if cleaned_data.startswith(" "):
        raise ValidationError("Field cannot begin with whitespace.")
