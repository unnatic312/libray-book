from django.contrib import admin
from .models import ProductSerializerModel, ServiceSerializerModel
# Register your models here.

admin.site.register(ProductSerializerModel)
admin.site.register(ServiceSerializerModel)