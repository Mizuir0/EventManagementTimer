from django.db import models

# Create your models here.
class Timers(models.Model):
  band_name = models.CharField(max_length=20)
  minutes = models.IntegerField(default=15)
  item1 = models.CharField(max_length=10)
  item2 = models.CharField(max_length=10)
  item3 = models.CharField(max_length=10)
  uuid = models.IntegerField(default=0)