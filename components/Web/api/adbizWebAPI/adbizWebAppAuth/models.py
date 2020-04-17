from django.db import models

# Create your models here.

class Site(models.Model):
    siteCode = models.CharField(max_length = 8)
    siteName = models.CharField(max_length = 128)
    #isActive = models.
    createDateTime = models.DateTimeField()
    createdBy = models.CharField(max_length = 128)

