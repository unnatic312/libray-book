from django.db import models

# Create your models here.

class auther(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.TextField()

    def __str__(self):
        return self.first_name+self.last_name

    def get_absolute_url(self):
        return (self)

class books(models.Model):
    name = models.CharField(max_length=50)
    auther = models.ForeignKey(auther, on_delete=models.CASCADE)
    published_on = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ((self.name).replace(" ","_"))


