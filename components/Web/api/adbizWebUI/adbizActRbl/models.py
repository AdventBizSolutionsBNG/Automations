import django
from django.db import models
from django.utils import timezone

#from adbizWebUIEngine.models import AdbizDashboards

import uuid
import datetime
# Create your models here.


class ModuleSettings(models.Model):
    class Meta:
        #managed = False
        db_table = "module_settings"

    config_key = models.CharField(max_length=32, unique=True, verbose_name="Config Key")
    config_value = models.TextField(verbose_name="Config Value")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=32, verbose_name="Last Updated By", editable=False)

