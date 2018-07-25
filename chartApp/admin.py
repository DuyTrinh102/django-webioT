
from django.contrib import admin
from .models import ParaMeasure, DataMeasure, StationUser

admin.site.register(ParaMeasure)
admin.site.register(DataMeasure)
admin.site.register(StationUser)
