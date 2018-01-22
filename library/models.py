from django.db import models

# Create your models here.

class users(models.Model):
    user_id = models.EmailField()
    user_password = models.CharField( max_length=20)


class auther(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.TextField()

    def __str__(self):
        return self.first_name+self.last_name

    def get_absolute_url(self):
        return (self)

class publication(models.Model):
    name = models.CharField(max_length=100)
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ((self.name).replace(" ","_"))

class books(models.Model):
    name = models.CharField(max_length=50)
    auther = models.ForeignKey(auther, on_delete=models.CASCADE)
    published_on = models.DateField()
    publication = models.ManyToManyField(publication)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ((self.name).replace(" ","_"))




