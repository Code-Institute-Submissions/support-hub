"""Signals for tickets application"""


from django.db.models.signals import pre_delete
from django.dispatch import receiver
import cloudinary
from .models import Ticket


# CREDIT: Nicholas Kajoh - https://alphacoder.xyz
# URL: https://alphacoder.xyz/image-upload-with-django-and-cloudinary/
@receiver(pre_delete, sender=Ticket)
def photo_delete(sender, instance, **kwargs):
    """Receiver function to delete cloudinary image when ticket is deleted
    using the delete view or the admin site.
    """
    if instance.ticket_image:
        cloudinary.uploader.destroy(instance.ticket_image.public_id)
