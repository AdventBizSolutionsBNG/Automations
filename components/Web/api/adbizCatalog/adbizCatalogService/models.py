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

# User defined hierarchy types that will be used to partition data and for data access controls (who gets to view what data).
# While setting up a Site, admin defines multiple hierarchies that exists in the organization (ex: Divisional based, plant based, distribution based etc).
# Post this step, admin defines multiple entities as per the hierarchy. Entities are involved in providing data for ingestion.
# Hierarchy Type is used while defining a catalog. Multiple catalogs can co-exists under a site with different hierarchy allowing the business to view the same information in multiple ways.

class OrgHierarchyTypes(models.Model):
    class Meta:
        db_table = "org_hierarchy_types"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment", editable=False)
    type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Hierarchy Type")
    description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Description", null=True)
    hierarchy_class_reference = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Hierarchy Class", null=True)  # Refers at any inbuilt hierarchy model
    is_system = models.BooleanField(default=False, verbose_name="System Based ?", editable=False)   # do not edit this flag if set
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=datetime.datetime.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(auto_now_add = True, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Example: A Legal Entity having multiple Business Units/Divisions Or a Manufacturer having multiple plants and warehouses or distribution centers
class OrgHierarchy(models.Model):
    class Meta:
        db_table = "org_hierarchies"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    hierarchy_type = models.ForeignKey(OrgHierarchyTypes, on_delete=models.CASCADE, verbose_name="Hierarchy Type")
    hierarchy_name = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Hierarchy Type")
    hierarchy_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Description", null=True)
    parent_hierarchy = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    level = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

# Entity Hierarchy
class Entities(models.Model):
    class Meta:
        db_table = "entities"

    entity_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name ="Entity Code", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    entity_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Entity Name")
    entity_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in EntityTypes],  verbose_name="Entity Type")
    entity_sub_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, choices= [x.value for x in EntitySubTypes],  verbose_name="Entity Sub Type")
    parent_entity = models.PositiveIntegerField(verbose_name="Parent Entity", null=True)
    hierarchy = models.ForeignKey(OrgHierarchy, verbose_name="Hierarchy", on_delete=models.CASCADE, default=2)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class EntityLocations(models.Model):
    class Meta:
        db_table = "entity_locations"

    entity = models.ForeignKey(Entities, on_delete=models.CASCADE, verbose_name="Entity")
    address_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in AddressTypes],  verbose_name="Address Type")
    address_line_1 = models.CharField(max_length=constants["ADDRESS_LINE"]["maxLength"], null=True, verbose_name="Address Line 1")
    address_line_2 = models.CharField(max_length=constants["ADDRESS_LINE"]["maxLength"], null=True, verbose_name="Address Line 2")
    address_line_3 = models.CharField(max_length=constants["ADDRESS_LINE"]["maxLength"], null=True, verbose_name="Address Line 3")
    city = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], null=True, verbose_name="City")
    state = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], null=True, verbose_name="State")
    country = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], null=True, verbose_name="Country")
    zip_code = models.CharField(max_length=8, null=True, verbose_name="ZipCode")
    is_primary_address = models.BooleanField(default=True, verbose_name="Is Primary ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class EntityContacts(models.Model):
    class Meta:
        db_table = "entity_contacts"

    entity = models.ForeignKey(Entities, on_delete=models.CASCADE)
    contact_person_first_name = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], null=True, verbose_name="First Name")
    contact_person_last_name = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], null=True, verbose_name="Last Name")
    contact_person_designation = models.CharField(max_length=32, null=True, verbose_name="Designation")
    contact_Email = models.EmailField(null=True, verbose_name="Email Id")
    contact_phone_number = models.CharField(max_length=64, null=True, verbose_name="Phone Numbers")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class Catalogs(models.Model):
    class Meta:
        db_table = "catalogs"

    catolog_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Catalog Code (generated)", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Catalog Name")
    catalog_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], null=True, verbose_name="Catalog Description")
    hierarchy_type = models.ForeignKey(OrgHierarchyTypes, verbose_name="Hierarchy Type", on_delete=models.CASCADE)    # models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in OrgHieararchyTypes],  verbose_name="Hierarchy Type")
    date_hierarchy = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in DateHierarchy], verbose_name="Date Hierarchy", editable=False)
    calendar_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in CalenderTypes],  verbose_name="Calendar Type")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class DataModels(models.Model):
    class Meta:
        db_table = "datamodels"

    datamodel_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Datamodel Code (generated)", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in Modules],  verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    version = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

class Objects(models.Model):
    class Meta:
        db_table = "objects"

    object_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique = True, verbose_name ="Object Code (generated)", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    object_name = models.CharField(max_length=constants["OBJECT"]["maxLength"], verbose_name="Object Name")
    object_reference_class = models.CharField(max_length=constants["CLASS"]["maxLength"], verbose_name="Object Class")    # Reference to internal list of objects (like invoices) for that particular module
    object_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Object Name")
    object_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in ObjectClass],  verbose_name="Object Class")
    is_validate_data = models.BooleanField(default=True, verbose_name="Validate Data ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

class LookupValues(models.Model):
    class Meta:
        db_table = "lookups"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer",
                                     editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    lookup_name = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Lookup Name")
    parent_lookup = models.ForeignKey('self', verbose_name="Parent Lookup", null=True)
    lookup_code = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Lookup Code")
    lookup_value = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Lookup Value")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class Attributes(models.Model):
    class Meta:
        db_table = "attributes"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Attribute Name")
    attribute_class = models.CharField(max_length=constants["CLASS"]["maxLength"], verbose_name="Attribute Reference Class")
    attribute_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Attribute Description")
    attribute_display_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Attribute Display Name")
    attribute_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in AttributeType],  verbose_name="Attribute Type")
    attribute_reference = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Attribute Reference", null=True)
    attribute_data_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in DataTypes],  verbose_name="Attribute Data Type")
    attribute_check_condition = models.CharField(max_length=constants["CHECK_CONDITION"]["maxLength"], verbose_name="Attribute Check Condition", null=True)
    attribute_min_length = models.PositiveSmallIntegerField(null=True)
    attribute_max_length = models.PositiveIntegerField(null=True)
    attribute_precision = models.PositiveSmallIntegerField(null=True)
    attribute_scale = models.PositiveSmallIntegerField(null=True)
    attribute_import_seq = models.PositiveSmallIntegerField(null=True)
    attribute_save_seq = models.PositiveSmallIntegerField(null=True)
    attribute_text_pattern = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Attribute Text/Date Pattern (regex)", null=True)
    attribute_format_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in InbuiltDataFormats],  verbose_name="Attribute Data Formats (inbuilt)", null=True)
    attribute_custom_format = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in InbuiltDataFormats],  verbose_name="Attribute Custom Data Formats", null=True)
    attribute_enums = models.CharField(max_length=constants["LOV"]["maxLength"], verbose_name="Attribute Enums", null=True)
    attribute_formula = models.CharField(max_length=constants["FORMULA"]["maxLength"], verbose_name="Attribute Formula (derived column)", null=True)
    attribute_default_value = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Attribute Default Value", null=True)
    attribute_pii_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in PIITypes], verbose_name="Attribute PII Category", null=True)
    is_required = models.BooleanField(default=False, verbose_name="Required ?")
    is_unique = models.BooleanField(default=False, verbose_name="Unique ?")
    is_identity = models.BooleanField(default=False, verbose_name="Identity ?")
    is_editable = models.BooleanField(default=False, verbose_name="Editable ?")
    is_visible = models.BooleanField(default=True, verbose_name="Visible ?")
    is_pii = models.BooleanField(default=False, verbose_name="Personal Identifiable Information ?")
    is_ignore_validations = models.BooleanField(default=False, verbose_name="Ignore Validations ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

class Dimensions(models.Model):
    class Meta:
        db_table = "dimensions"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, editable=False)
    dimension_code = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Dimension Code (generated)", editable=False)
    dimension_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Dimension Description", null=True)
    dimension_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in DimensionTypes], verbose_name="Dimension Type")
    is_hierarchy = models.BooleanField(default=False, verbose_name="Hierarchy ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class Measures(models.Model):
    class Meta:
        db_table = "measures"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, editable=False)
    measure_code = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Measure Code (generated)", editable=False)
    measure_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Measure Description", null=True)
    measure_type = models.CharField(max_length=constants["LOV"]["maxLength"], choices= [x.value for x in MeasureTypes], verbose_name="Measure Types (multi-choice)")
    measure_operators = models.CharField(max_length=constants["LOV"]["maxLength"], choices=[x.value for x in MeasureOperators], verbose_name="Measure Operators (multi-choice)")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Datasets enables multiple data ingress and egress for the whole system.
# One or more datasets can be configured for each object.
# Each Dataset can have multiple datasources and datatargets
# ETL Engine will use the Dataset configuration to execute the to ingest data and execute the data processing workflow
class Datasets(models.Model):
    class Meta:
        db_table = "datasets"

    dataset_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name ="Dataset Code", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False)
    dataset_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Dataset Name")
    dataset_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Dataset Description", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Each Dataset to have 1:many datasources to ingest data from.
# Each active datasource will have a global unique ID and an indiviudal schedule which ETL Engine will check and execute the ingestion process.
# Ingestion can be Batch (default) or Streaming (to be done). Only Batch type ingestion will have a schedule defined.
# Ingestion can be Incremental or Full Load Type. For Incremental: ETL/Workflow Engine will do an append on the destination (default)
# For Full Load: ETL Engine will do a delete and load every time on the destinations

class DataSources(models.Model):
    class Meta:
        db_table = "data_sources"

    datasource_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name ="Datasource Code (generated)", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False, verbose_name="Data model")
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules],verbose_name="Module", editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False, verbose_name="Object")
    dataset = models.ForeignKey(Datasets,on_delete=models.CASCADE, editable=False, verbose_name="Dataset")
    datasource_connector_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in SourceConnectors], verbose_name="Data Source Connector Type", editable=False)
    datasource_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Data Source Name")
    datasource_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Data Source Description", null=True)
    datasource_properties = models.TextField() # as json
    datasource_schedule = models.CharField(max_length=constants["SCHEDULE"]["maxLength"]) # as CRON Schedule
    is_batch = models.BooleanField(default=True, verbose_name="Batch Type Ingestion ?")
    is_streaming = models.BooleanField(default=False, verbose_name="Streaming Ingestion ?")
    is_incremental_load = models.BooleanField(default=True, verbose_name="Incremental Load ?")
    is_full_load = models.BooleanField(default=False, verbose_name="Full Load ?")
    version = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)



class DataTargets(models.Model):
    class Meta:
        db_table = "data_targets"

    datatarget_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Datatarget Code (generated)", editable=False)
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules],verbose_name="Module", editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False)
    dataset = models.ForeignKey(Datasets,on_delete=models.CASCADE, editable=False)
    datatarget_connector_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in DestinationConnectors], verbose_name="Data target Connector Type", editable=False)
    datatarget_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Data target Name")
    datatarget_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Data target Description", null=True)
    datatarget_properties = models.TextField() # as json
    version = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

# Containers are physical locations that store data as a part of the ingestion process (aka. data lake/repository).
# Container are of 2 types: Generic & User Defined
# Generic containers are default ones that stores the incoming data in raw format (incl derived columns etc). Mandatory. Cannot be configured.
# User Defined containers help segmentation of incoming data on the fly. Select columns from the Source can be chosen to be a part of this container type.
class Containers(models.Model):
    class Meta:
        db_table = "containers"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    dataset  = models.ForeignKey(Datasets, on_delete=models.CASCADE, verbose_name="Dataset")
    container_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Container Code (generated)", editable=False)
    container_type = models.CharField(max_length=255,  choices=[x.value for x in ContainerTypes], verbose_name="Container Type")
    container_name = models.CharField(max_length=255, verbose_name="Container Name")
    container_description = models.TextField(verbose_name="Description", null=True)
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")
    container_category = models.CharField(max_length=255, choices=[x.value for x in ContainerCategories], verbose_name="Container Category")
    container_location = models.CharField(max_length=255, verbose_name="Container Location", editable=False)
    filter_conditions = models.TextField(null=True, verbose_name="Filter Conditions")   # json
    filter_columns = models.TextField(null=True, verbose_name="Filter Columns")   # json
    is_incremental =  models.BooleanField(default=True, verbose_name="Incremental ?")
    is_initial_load = models.BooleanField(default=True, verbose_name="Initial Load ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

# Aggregates are physical locations that store aggregated data from a container.
# Each Aggregate table has Dimension (one Time Based and the other is Lookup based) and multiple measures configured.
# Each measure has defined operators (sum, count, min, max, avg) configured and aggregation is performed during the ingestion (etl/workflow)
class Aggregates(models.Model):
    class Meta:
        db_table = "aggregates"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    dataset  = models.ForeignKey(Datasets, on_delete=models.CASCADE, verbose_name="Dataset")
    container = models.ForeignKey(Containers, verbose_name="Container", on_delete=models.CASCADE)
    aggregate_code  = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Aggregate Code (generated)", editable=False)
    aggregate_location = models.CharField(max_length=255, verbose_name="Container Location", editable=False)
    aggregate_description = models.TextField(verbose_name="Description", null=True)
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")
    dimensions = models.TextField(null=True, verbose_name="Dimensions")   # json
    measures = models.TextField(null=True, verbose_name="Measures")   # json
    is_incremental =  models.BooleanField(default=True, verbose_name="Incremental ?")
    is_rebuild = models.BooleanField(default=True, verbose_name="Rebuild Everytime ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class AggregateDimensions(models.Model):
    class Meta:
        db_table = "aggregate_dimensions"

    aggregate = models.ForeignKey(Aggregates, verbose_name="Aggregate", on_delete=models.CASCADE)
    dimension_type = models.CharField(max_length=255, choices=[x.value for x in DimensionTypes], verbose_name="Dimension Type")
    dimension = models.ForeignKey(Dimensions, verbose_name="Dimension", on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attributes, verbose_name="Attribute", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class AggregateMeasures(models.Model):
    class Meta:
        db_table = "aggregate_measures"

    aggregate = models.ForeignKey(Aggregates, verbose_name="Aggregate", on_delete=models.CASCADE)
    measure = models.ForeignKey(Measures, verbose_name="Measure", on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attributes, verbose_name="Attribute", on_delete=models.CASCADE)
    measure_display_name = models.CharField(max_length=255, verbose_name="Measure Display Name")
    operators = models.CharField(max_length=255, choices=[x.value for x in Operators], verbose_name="Operators") # multichoice
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)



# KPI's are user defined pre-aggregated / run time aggregated data based on business functions and at the module level. Permissions are granted to specific roles to view the KPI's
# KPI's are populated post aggregation step during the ingestion process by ETL/Workflow engine
# Each KPI consists of 1 or many components used for further aggregating and displaying data related to business sub-function
# System provides out of box KPI's for each module. User can define their own custom KPI's and define the data population mode.
# Data Population: 2 types Per-Aggregated and Run time.
# Pre-Aggregated KPIS - Data is aggregated during the ingestion process and stored in the repository
# Run Time: KPI definitions are decoded at run time and dynamic queries are formed and executed by the Query Engine and results are returned in the format defined in the KPI
# Each component controls how the aggregated data should be displayed on the UI. 2 Types: Widget and Tabular
# Widget based KPI display data as an independent control using Graphs and Indicators (singular value based display) - Multiple queries are used for this
# Tabular type KPI's displays data as a table (single Query is used)
class KPIs(models.Model):
    class Meta:
        db_table = "kpis"

    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Customer", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    env_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment",
                                editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, editable=False)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    kpi_type = models.CharField(max_length=255, choices=[x.value for x in KPIType], verbose_name="KPI Data Population type")
    kpi_code  = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="KPI Code (generated)", editable=False)
    kpi_location = models.CharField(max_length=255, verbose_name="KPI Location", editable=False)
    kpi_class = models.CharField(max_length=255, verbose_name="KPI Class", editable=False, null=True)  # Refer to Adbiz Namespace for KPI's (out of box offerings)
    kpi_name = models.CharField(max_length=255, verbose_name="KPI Name")
    kpi_description = models.TextField(verbose_name="KPI Description", null=True)
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")     # Priority when rebuilding
    is_incremental =  models.BooleanField(default=True, verbose_name="Incremental ?")   # Entire KPI and its components data population gets appended during data ingestion process
    is_rebuild = models.BooleanField(default=False, verbose_name="Rebuild Everytime ?") # Entire KPI and its components data population get rebuilt every time using the source Container during the data ingestion process
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class KPIComponents(models.Model):
    class Meta:
        db_table = "kpi_components"

    kpi = models.ForeignKey(KPIs, on_delete=models.CASCADE, editable=False)
    container = models.ForeignKey(Containers, verbose_name="Container", on_delete=models.CASCADE)
    aggregate = models.ForeignKey(Aggregates, verbose_name="Aggregate", on_delete=models.CASCADE)
    component_code  = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="KPI Code (generated)", editable=False)
    component_class = models.CharField(max_length=255, verbose_name="Component Class Reference", null=True) # Refer to Adbiz Namespace for inbuilt components
    component_type = models.CharField(max_length=255, choices=[x.value for x in ComponentType], verbose_name="Component Type")
    component_display_type = models.CharField(max_length=255, choices=[x.value for x in ComponentDisplayType], verbose_name="Component Display Type")
    display_properties = models.TextField(verbose_name="Display Properties")    #JSON: Contains Display settings (ex: Graph Type, Color, x Axis, Y Axis Parameters)
    data_filter = models.TextField(verbose_name="Data Filters") # JSON: Contains filters for each Dimension & Measures as per the selected Aggregate in the component definition
    date_filter = models.TextField(verbose_name="Date Filters")  # JSON: Contains filters for Date Dimension
    sort_by = models.TextField(verbose_name="Sort by", null=True) # JSON: Sorting criteria
    indicators = models.TextField(verbose_name="Indicators", null=True) # JSON: Defines indicators (singular values)
    indicator_class = models.CharField(max_length=255, null=True)   # Refers to adbiz Namespace definitions for inbuilt indicators
    component_name = models.CharField(max_length=255, verbose_name="KPI Name")
    component_description = models.TextField(verbose_name="KPI Description", null=True)
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")     # Priority when rebuilding
    is_incremental =  models.BooleanField(default=True, verbose_name="Incremental ?")   # components data population gets appended during data ingestion process. Overrides KPI settings
    is_rebuild = models.BooleanField(default=False, verbose_name="Rebuild Everytime ?")  # components data population get rebuilt every time using the source Container during the data ingestion process. Overrides KPI settings
    refresh_interval  = models.PositiveSmallIntegerField(default=0, verbose_name="Refresh Interval (sec)")  # data refresh happens on the UI every X seconds as set. Default=0 means On Demand Refresh.
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)