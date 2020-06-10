from django.db import models
from django.db.models import Model
import django.utils
from django.utils import timezone
from django.forms import ModelForm, Textarea
from django_utils.choices import Choice, Choices
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from components.core.coreEngine import CoreEngine

from components.core.packages.lookups import *

ce = CoreEngine()
constants = ce.constants
lookups = ce.lookups


class Tenants(models.Model):
    class Meta:
        db_table = "tenants"

    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Product Engine Code", editable=False)
    tenant_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Tenant Name")
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Tenant Code (generated)", editable=False)
    tenant_namespace = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Tenant Namespace")
    registration_number = models.CharField(max_length=constants["REGISTRATION_NUMBER"]["maxLength"], unique=True, verbose_name="Unique Registration Number (any)")
    registration_dt = models.DateTimeField( verbose_name="Registration Date")
    company_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, verbose_name="Company Category")
    company_sub_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, verbose_name="Company Sub Category")  # , choices=lookups["CompanySubCategories"])
    company_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, verbose_name="Company Class")  # , choices=lookups["CompanySubCategories"])
    company_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, verbose_name="Company Type")
    city = models.CharField(max_length=constants["CITY"]["maxLength"], null=True, verbose_name="City")
    state = models.CharField(max_length=constants["STATE_CODE"]["maxLength"], null = True, verbose_name="State")
    country = models.CharField(max_length=constants["COUNTRY_CODE"]["maxLength"], verbose_name="Country")
    website_url = models.URLField(max_length=constants["URL"]["maxLength"], null = True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)



class LicensingInfo(models.Model):
    class Meta:
        db_table = "license_info"

    tenant = models.ForeignKey(Tenants,on_delete=models.CASCADE)
    license_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],  choices= [x.value for x in LicensingTypes ], default = LicensingTypes.get_value(LicensingTypes.SUBCRPTN))
    duration_days = models.PositiveIntegerField(default=0, verbose_name="Validity (days)")
    active_modules = models.CharField(max_length=255, choices= [x.value for x in Modules ], verbose_name="Modules")       # list
    active_engines = models.CharField(max_length=255, choices= [x.value for x in ProcessingEngines ], verbose_name="Engines")       # list
    active_envs = models.CharField(max_length=255, choices= [x.value for x in EnvTypes ], verbose_name="Instances")     # list
    active_from_dt = models.DateTimeField(verbose_name="Active since")
    active_end_dt = models.DateTimeField(null=True,verbose_name="Active till")
    activated_on_dt = models.DateTimeField(null=False, verbose_name="Activated On")
    deactivated_on_dt = models.DateTimeField(null=False, verbose_name="Deactivated On")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                     editable=False)


# Core Engine to be setup as a dedicated instance in a Tenant premise for one or more sites(only one Site recommended in a premise). Only one CE instance to be setup in a Tenant Premise.
# During setup, CoreEngine needs to be provided the API End point for Product Engine (PE) to receive the Licensing & Tenant Details.
# CoreEngine (CE) to sync the Licensing & Tenant details fromm PE and update its database (this info will not be editable in CoreEngine UI Module. Read only)
# Post successful update, CoreEngine to be activated manually and generate the activation key. Post this step CoreEngine will be operational.
# CE to setup Instances (like DEV, UAT etc) under the Site for the Tenant under consideration.
# Each Environment to host multiple modules (as governed by the Licensing info) and host set of dedicated Engines (like QueryEngine, KPI Engine, ETL etc).
# Tenant can setup multiple Instances but all connected to a single Core Engine which facilitates both: Authentication & Authorization
#   Authentication feature involves generating tokens for each User account and keeping track of them (expiry)
# CE will also handle activation & deactivation of sites, Instances, modules & engines etc


class CoreEngine(models.Model):
    class Meta:
        db_table="engine_metadata"

    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Core Engine Code (generated)")
    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Product Engine Code")
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, null=True, verbose_name="Tenant")       # to be populated post activation
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time")
    host_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Host Name")
    host_ip_address = models.GenericIPAddressField(max_length=32, verbose_name="Host IP Address")
    os_release = models.CharField(max_length=32, null=True, verbose_name="OS Release Version")
    release_info = models.CharField(max_length=255, null=True, verbose_name="Version Details")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    product_engine_details = models.TextField(verbose_name="Product Engine Details", editable=False, null=True)  # json. Used by Core engine to connect to the Product Engine
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# multiple activation/deactivation details for CE (History Table)
class CoreEngineActivations(models.Model):
    class Meta:
        db_table="engine_activations"

    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Product Engine Code", editable=False)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant", editable=False)
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"],
                                                verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], editable=False, verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time", editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)



class Sites(models.Model):
    class Meta:
        db_table="sites"

    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", null=True, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Site ID (generated)", editable=False)
    site_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Site Name")
    site_description = models.TextField(max_length=constants["DESCRIPTION"]["maxLength"], null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)




class Instances(models.Model):
    class Meta:
        db_table="instances"

    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Environment/Instance Code (generated)", editable = False)
    environment_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, choices= [x.value for x in EnvTypes], default = EnvTypes.get_value(EnvTypes.DEV), verbose_name="Environment Type")
    environment_description = models.TextField(max_length=constants["DESCRIPTION"]["maxLength"], null=True)
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"],
                                                verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"],
                                      verbose_name=" Activation Key (generated)", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time")
    host_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Host Name")
    host_ip_address = models.GenericIPAddressField(max_length=32, verbose_name="Host IP Address")
    os_release = models.CharField(max_length=32, null=True, verbose_name="OS Release Version")
    release_info = models.CharField(max_length=255, null=True, verbose_name="Version Details")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# CE to track multiple activation/deactivation details
class InstanceActivations(models.Model):
    class Meta:
        db_table="instance_activations"

    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    instance = models.ForeignKey(Instances, on_delete=models.CASCADE, verbose_name="Instance")
    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], editable=False,
                                      verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

# CE to manage multiple modules.
# Each Module will be individually activated for each environment using licensing details from PE/CE
class Modules(models.Model):
    class Meta:
        db_table="modules"

    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    instance = models.ForeignKey(Instances, on_delete=models.CASCADE, verbose_name="Instance")
    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    module = models.CharField(max_length=255,  choices=[x.value for x in Modules], verbose_name="Modules")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"],
                                      verbose_name=" Activation Key (generated)", editable=False)
    activation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Module Activation Date Time")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# CE to track multiple activation/deactivation details (history log)
class ModuleActivations(models.Model):
    class Meta:
        db_table="module_activations"

    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    instance = models.ForeignKey(Instances, on_delete=models.CASCADE, verbose_name="Instance")
    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], editable=False,
                                      verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# CE to manage multiple Engines for Processing of Data
class ProcessingEngines(models.Model):
    class Meta:
        db_table="processing_engines"

    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    instance = models.ForeignKey(Instances, on_delete=models.CASCADE, verbose_name="Instance")
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], default="ALL", null=True, verbose_name="Module")
    processing_engine_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in ProcessingEngines], verbose_name="Processing Engine")
    processing_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Processing Engine Code (generated)", editable=False)
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable=False)
    engine_properties = models.TextField(null=True, verbose_name="Engine Properties") # json. stores engine specific properties

    activation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Activation Date Time")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# CE to track multiple activation/deactivation details for all Processing Engines configured as per the licensing (history log)
class ProcessingEngineActivations(models.Model):
    class Meta:
        db_table="processing_engine_activations"

    processing_engine = models.ForeignKey(ProcessingEngines, on_delete=models.CASCADE, verbose_name="Processing Engine")
    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    instance = models.ForeignKey(Instances, on_delete=models.CASCADE, verbose_name="Instance")

    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], editable=False,
                                      verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# This class holds information of the target systems that contains both Raw & processed data including aggregates & KPI's, temporary tabels etc
# Individual datalakes will be created for a unique combination of tenant + site + instance + catalog + module. Creation of data lakes is dynamic and this metadata table gets updated.
# Individual data lakes can be managed independently like backups or performance tuning.
# Query/ETL engine will use this class to identify the target data lake and retrieve data.
# Data lakes can be hosted on any target platforms like rdbms, hive, Cloud databases.

class DataLakes(models.Model):
    class Meta:
        db_table = "data_lakes"

    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, verbose_name="Tenant")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    instance = models.ForeignKey(Instances, on_delete=models.CASCADE, verbose_name="Environment/Instance")
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Module")
    storage_engine_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Storage Engine Class")     # Specifies inbuilt storage engine class to be used
    data_lake_type = models.CharField(max_length=255, choices=[x.value for x in DataLakeTypes], verbose_name="Data Lake Type")
    data_lake_sub_type = models.CharField(max_length=255, choices=[x.value for x in DataLakeSubTypes], verbose_name="Data Lake Sub Type")
    data_lake_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Data Lake Code", editable=False)
    data_lake_description =  models.TextField(verbose_name="Description", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    is_primary = models.BooleanField(default=True, verbose_name="Is Primary Storage?")  # replicas can be also created as backups
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)

#
# class Tokens(models.Model):
#     class Meta:
#         db_table = "tokens"

