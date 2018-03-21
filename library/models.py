from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Auther(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.TextField()

    def __str__(self):
        return self.first_name+self.last_name

    def get_absolute_url(self):
        return (self)


class Publication(models.Model):
    name = models.CharField(max_length=100)
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return (self.name).replace(" ", "_")


class Books(models.Model):
    name = models.CharField(max_length=50)
    auther = models.ForeignKey(Auther, on_delete=models.CASCADE)
    published_on = models.DateField()
    publication = models.ManyToManyField(Publication)
    book_data = models.FileField(upload_to='library/', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return (self.name).replace(" ", "_")


class BookReview(models.Model):
    book_review = models.TextField()
    date_on = models.DateTimeField(auto_now=True, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)


    def __str__(self):
        return (self.book.name)

