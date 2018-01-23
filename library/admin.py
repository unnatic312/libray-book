
from django.contrib import admin
from .models import books, auther, publication

# Register your models here.
admin.site.register(books)
admin.site.register(auther)
admin.site.register(publication)
