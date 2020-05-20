from django.db import models
from audit_log.models.managers import AuditLog
from audit_log.models import AuthStampedModel

# Create your models here.


class Site(models.Model):

    siteCode = models.CharField(unique = True, max_length = 8)
    siteName = models.CharField(max_length = 128)

    #isActive = models.
    createDateTime = models.DateTimeField()
    createdBy = models.CharField(max_length = 128)


class Organization(models.Model):
    organizationName =
    organizationCode =