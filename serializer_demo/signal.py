from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProductSerializerModel


@receiver(post_save, sender=ProductSerializerModel)
def index_post(sender, instance, **kwargs):
    instance.indexing()