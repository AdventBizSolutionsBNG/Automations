import django
from django.db import models
from django.db.models import Model
import uuid
import re
import datetime
from django.utils import timezone
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from components.core.coreEngine import CoreEngine
from components.core.packages.lookups import *

ce = CoreEngine()
constants = ce.constants
lookups = ce.lookups



class EngineProperties(models.Model):
    class Meta:
        managed = False

    io_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="IO Engine Code (generated)")
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant")
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)

    setup_mode = models.BooleanField(default=False, verbose_name="Setup Mode ?") # Single or Multi
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], default = "ALL", verbose_name="Module", editable=False) # default = "ALL" if common IO Engine is hosted for all modules in an instance/env.

    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"],verbose_name="Core Engine Code", editable=False)
    core_engine_url = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine base URL", editable=False)
    core_engine_api_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine API Key", editable=False)

    catalog_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Catalog Engine Code", editable=False)
    core_engine_url = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Catalog Engine base URL", editable=False)
    core_engine_api_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Catalog Engine API Key", editable=False)


class EngineAPICalls(models.Model):
    class Meta:
        managed = False



# In an environnment: IO Engine can be hosted in 2 modes: Single or Multi
# Single Mode: Single IO engine hosted for all the modules
# Multi Mode: Multiple IO engines hosted. Each engine handles requests for a specific module
class IOEngine(models.Model):
    class Meta:
        db_table="engine_metadata"

    io_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="IO Engine Code (generated)")
    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine Code", editable=False)
    catalog_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Catalog Engine Code", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant")
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], default = "ALL", verbose_name="Module", editable=False) # default = "ALL" if common IO Engine is hosted for all modules in an instance/env.
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time")
    host_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Host Name")
    host_ip_address = models.GenericIPAddressField(max_length=32, verbose_name="Host IP Address")
    os_release = models.CharField(max_length=32, null=True, verbose_name="OS Release Version")
    release_info = models.CharField(max_length=255, null=True, verbose_name="Version Details")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    engine_properties = models.TextField(verbose_name="Engine Properties", editable=False)  # json.
    core_engine_details = models.TextField(verbose_name="Core Engine Details", editable=False)  # json. Used by IO engine to connect to the Core Engine
    catalog_engine_details = models.TextField(verbose_name="Catalog Engine Details", editable=False)  # json. Used by IO engine to connect to Catalog engine
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


    def __init__(self):
        data = {}
        data = self.engine_properties
        if data is not None or data != "":
            p = EngineProperties()
            p.io_engine_code = self.io_engine_code
            p.tenant_code = self.tenant_code
            p.site_code = self.site_code
            p.instance_code = self.instance_code
            p.core_engine_code = self.core_engine_code
            p.catalog_engine_code = self.catalog_engine_code
            for k,v in data.items:
                p.setup_mode = k["setup_mode"]
                if k["modules"] is not None:
                    p.module = k["modules"]
                else:
                    p.module = "ALL"


# multiple activation/deactivation details for CE (History Table)
class IOEngineActivations(models.Model):
    class Meta:
        db_table="engine_activations"

    io_engine = models.ForeignKey(IOEngine, verbose_name="IO Engine", on_delete=models.CASCADE)
    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine Code", editable=False)
    catalog_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Catalog Engine Code", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant")
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], editable=False, verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time", editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    catalog_engine_details = models.TextField(verbose_name="Catalog Engine Details", null=True)  # json. Used by IO engine to retrieve Catalog information
    core_engine_details = models.TextField(verbose_name="Core Engine Details", null=True)  # json. Used by IO engine to retrieve Core engine information
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# Data lake information is synchronized from CORE Engine. Only the applicable Data lake info (for a particular tenant, site, instance combination) is synchronized.
# This avoids frequent calls to CORE engine.

class DataLakes(models.Model):
    class Meta:
        managed = False

    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine Code", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Module", editable=False)
    storage_engine_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Storage Engine Class", editable=False)     # Specifies inbuilt storage engine class to used
    data_lake_type = models.CharField(max_length=255, verbose_name="Data Lake Type", editable=False)
    data_lake_sub_type = models.CharField(max_length=255, verbose_name="Data Lake Sub Type", editable=False)
    data_lake_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Data Lake Code", editable=False)
    data_lake_description =  models.TextField(verbose_name="Description", null=True, editable=False)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    is_primary = models.BooleanField(default=True, verbose_name="Is Primary Storage?", editable=False)  # replicas can be also created as backups
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)

    def __init__(self):
        pass

# This class stores the query details & the generated query for all the dashboard queries initiated by the user.
# Dashboard setups are role specific and it contains different widgets & indicators.
# Users, post login view these dashboards. UI triggers queries for each of the configured widget  (API calls) and get response from IO Engine with the data.
# IO engine receives the payload (request) with all the different parameters like filters used.
# IO Engine then generates SQL query using the inputs and extracts data from the Data lake.
# Also, the IO Engine saves the generated queries (per user) for the first time in this class
# it also maintains a log with the execution details.
class DashboardQuery(models.Model):
    class Meta:
        db_table = "query_log"

    # io_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"])
    #api_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"])

    data_lake = models.ForeignKey(DataLakes, on_delete=models.CASCADE, null=True)
    request_user_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Dimension Code", null=True)
    request_user_session = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Session")
    date_filter = models.TextField(null=True)    # json
    dimension_filter = models.TextField(null=True)   #json
    measures_filter = models.TextField(null=True)    # json
    dtf_dim_code = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Dimension Code", null=True)
    dtf_attribute_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name ="Attribute Name", null=True)
    dtf_quick_option = models.TextField(null=True, verbose_name= "Quick Option") # json
    dtf_qo_operator = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in QuickOptionsDateOperators], verbose_name="Quick Option - Data Operator", null=True)
    dtf_qo_value= models.CharField(max_length=255, null=True)
    dtf_qo_period = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in QuickOptionsDatePeriods], verbose_name="Quick Option - Data Operator", null=True)
    dtf_custom_option = models.TextField(null=True) #json
    dtf_co_operator = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in CustomOptionsDateOperators], verbose_name=" Operator", null=True)
    dtf_co_start_date = models.DateField(null=True)
    dtf_co_end_date = models.DateField(null=True)
    dmf_dim_code = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Dimension Code", null=True)
    dmf_attribute_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Attribute Name", null=True)
    dmf_custom_option = models.TextField(null=True)
    dmf_co_operator = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in DimensionOperators], verbose_name=" Operator", null=True)
    dmf_co_value = models.CharField(max_length=255, null=True)
    dmf_sort_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in SortTYpe], verbose_name=" Sort Type", null=True)
    msf_measure_code = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Measure Code", null=True)
    msf_attribute_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Attribute Name", null=True)
    msf_quick_option = models.TextField(null=True)
    msf_qo_operator = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in MeasureOperators], verbose_name=" Operator", null=True)
    msf_qo_value_1 = models.CharField(max_length=255, null=True)
    msf_qo_value_2 = models.CharField(max_length=255, null=True)
    msf_sort_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in SortTYpe], verbose_name=" Sort Type", null=True)
    generated_query = models.TextField(null=True)   #stores generated query for future use.
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    duration_ms = models.PositiveIntegerField(default=0)
    total_rows = models.PositiveIntegerField(default=0)
    query_log = models.TextField(null=True) # json. Output of query execution if any
    error_log = models.TextField(null=True) # json