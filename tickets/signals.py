from django.dispatch import receiver
from django.db.models.signals import pre_delete
import cloudinary
from .models import Ticket


# Receiver function to delete cloudinary image when ticket is deleted
# CREDIT: Nicholas Kajoh - https://alphacoder.xyz
# URL: https://alphacoder.xyz/image-upload-with-django-and-cloudinary/
@receiver(pre_delete, sender=Ticket)
def photo_delete(sender, instance, **kwargs):
    if instance.ticket_image:
        cloudinary.uploader.destroy(instance.ticket_image.public_id)
