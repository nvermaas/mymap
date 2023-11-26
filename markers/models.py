from django.db import models
from django.utils import timezone
class Sniffer(models.Model):
    ip = models.CharField(db_index=True,max_length=15)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    longtitude = models.FloatField()
    latitude = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    def __str__(self):
        return self.ip + ' - ' + str(self.address)
