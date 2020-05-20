from django.db import models
from django.db.models import Model
import django.utils
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


class Customers(models.Model):
    class Meta:
        db_table = "customers"

    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Product Engine Code", editable=False)
    customer_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Customer Name")
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Customer Code (generated)", editable=False)
    customer_namespace = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Customer Namespace")
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

    customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
    license_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],  choices= [x.value for x in LicensingTypes ], default = LicensingTypes.get_value(LicensingTypes.SUBCRPTN))
    duration_days = models.PositiveIntegerField(default=0, verbose_name="Validity (days)")
    active_modules = models.CharField(max_length=255, choices= [x.value for x in Modules ], verbose_name="Modules")       # list
    active_engines = models.CharField(max_length=255, choices= [x.value for x in ProcessingEngines ], verbose_name="Engines")       # list
    active_envs = models.CharField(max_length=255, choices= [x.value for x in EnvTypes ], verbose_name="Environments")     # list
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


class Sites(models.Model):
    class Meta:
        db_table="sites"

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
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




# Core Engine to be setup as a dedicated instance in a Customer premise for one or more sites(only one Site recommended in a premise). Only one CE instance to be setup in a Customer Premise.
# During setup, CoreEngine needs to be provided the API End point for Product Engine (PE) to receive the Licensing & Customer Details.
# CoreEngine (CE) to sync the Licensing & Customer details fromm PE and update its database (this info will not be editable in CoreEngine UI Module. Read only)
# Post successful update, CoreEngine to be activated manually and generate the activation key. Post this step CoreEngine will be operational.
# CE to setup environments (like DEV, UAT etc) under the Site for the Customer under consideration.
# Each Environment to host multiple modules (as governed by the Licensing info) and host set of dedicated Engines (like QueryEngine, KPI Engine, ETL etc).
# Customer can setup multiple environments but all connected to a single Core Engine which facilitates both: Authentication & Authorization
#   Authentication feature involves generating tokens for each User account and keeping track of them (expiry)
# CE will also handle activation & deactivation of sites, environments, modules & engines etc


class CoreEngine(models.Model):
    class Meta:
        db_table="engine_metadata"

    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Core Engine Code (generated)")
    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Product Engine Code")
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer", null=True)       # to be populated post activation
    #site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site", null=True)                   # to be populated post activation
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable=False)
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
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# multiple activation/deactivation details for CE (History Table)
class CoreEngineActivations(models.Model):
    class Meta:
        db_table="engine_activations"

    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Product Engine Code", editable=False)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer", editable=False)
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


class Environments(models.Model):
    class Meta:
        db_table="environments"

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    core_engine = models.ForeignKey(CoreEngine, verbose_name="Core Engine", on_delete=models.CASCADE)
    environment_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Environment ID (generated)", editable = False)
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
class EnvironmentActivations(models.Model):
    class Meta:
        db_table="environment_activations"

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    environment = models.ForeignKey(Environments, on_delete=models.CASCADE, verbose_name="Environment")
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

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    environment = models.ForeignKey(Environments, on_delete=models.CASCADE, verbose_name="Environment")
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

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    environment = models.ForeignKey(Environments, on_delete=models.CASCADE, verbose_name="Environment")
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
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    environment = models.ForeignKey(Environments, on_delete=models.CASCADE, verbose_name="Environment")
    processing_engine_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, choices= [x.value for x in ProcessingEngines], verbose_name="Processing Engine")
    processing_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Processing Engine Code (generated)", editable=False)
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable=False)
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
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    site = models.ForeignKey(Sites, on_delete=models.CASCADE, verbose_name="Site")
    environment = models.ForeignKey(Environments, on_delete=models.CASCADE, verbose_name="Environment")
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

#
# class Tokens(models.Model):
#     class Meta:
#         db_table = "tokens"

