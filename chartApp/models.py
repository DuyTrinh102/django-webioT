from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class StationUser(models.Model):
	station_name = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="station_user")
	

class ParaMeasure(models.Model):
	name = models.CharField(max_length=255)
	unit = models.CharField(max_length=50)
	nameStation = models.ForeignKey(StationUser, on_delete=models.CASCADE,related_name="paraStation")
	

class DataMeasure(models.Model):
	value = models.CharField(max_length=255)
	label = models.CharField(max_length=255)
	last_updated = models.DateTimeField(auto_now_add=False)
	paraStation = models.ForeignKey(ParaMeasure, on_delete=models.CASCADE,related_name="paraMeasure")
	



