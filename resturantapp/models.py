from django.db import models

# Create your models here.
class Address(models.Model):
  name = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  phone = models.IntegerField()
  message = models.CharField(max_length=1000)
  def __str__(self):
    return f'{self.name}-{self.phone}'