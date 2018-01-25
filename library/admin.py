
from django.contrib import admin
from .models import Books, Auther, Publication, BookReview

# Register your models here.
admin.site.register(Books)
admin.site.register(BookReview)
admin.site.register(Auther)
admin.site.register(Publication)
