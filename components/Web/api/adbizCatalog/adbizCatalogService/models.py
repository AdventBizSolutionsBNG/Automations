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


class CatalogEngine(models.Model):
    class Meta:
        db_table="engine_metadata"

    catalog_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Catalog Engine Code (generated)")
    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine Code", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant")
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time")
    host_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Host Name")
    host_ip_address = models.GenericIPAddressField(max_length=32, verbose_name="Host IP Address")
    os_release = models.CharField(max_length=32, null=True, verbose_name="OS Release Version")
    release_info = models.CharField(max_length=255, null=True, verbose_name="Version Details")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    engine_properties = models.TextField(verbose_name="Engine Details", null=True)    # json.
    core_engine_details = models.TextField(verbose_name="Core Engine Details", editable=False)  # json. Used by Catalog engine to connect to the Core Engine
    io_engine_details = models.TextField(verbose_name="IO Engine Details", editable=False)  # json. Used by Catalog engine to connect to the IO Engine
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# multiple activation/deactivation details for CE (History Table)
class CatalogEngineActivations(models.Model):
    class Meta:
        db_table="engine_activations"

    catalog_engine = models.ForeignKey(CatalogEngine, verbose_name="Catalog Engine", on_delete=models.CASCADE)
    core_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Core Engine Code", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant")
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], editable=False, verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time", editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# User defined hierarchy types that will be used to partition data and for data access controls (who gets to view what data).
# While setting up a Site, admin defines multiple hierarchies that exists in the organization (ex: Divisional based, plant based, distribution based etc).
# Post this step, admin defines multiple entities as per the hierarchy. Entities are involved in providing data for ingestion.
# Hierarchy Type is used while defining a catalog. Multiple catalogs can co-exists under a site with different hierarchy allowing the business to view the same information in multiple ways.
# Atleast one hierarchhy type has to be defined
class OrgHierarchyTypes(models.Model):
    class Meta:
        db_table = "org_hierarchy_types"

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
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

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
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
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
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

    catalog_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Catalog Code (generated)", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
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
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"],
                                     verbose_name="Environment/Instance", editable=False, null=True)  #*
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in Modules],  verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Datamodel Name", null=True)  #*
    datamodel_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], null=True, verbose_name="Datamodel Description")
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
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
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

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant",
                                     editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    lookup_name = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Lookup Name")
    parent_lookup = models.ForeignKey('self', verbose_name="Parent Lookup", null=True, on_delete=models.CASCADE)
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

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Attribute Name")
    attribute_class = models.CharField(max_length=constants["CLASS"]["maxLength"], verbose_name="Attribute Reference Class", null=True)
    attribute_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Attribute Description", null=True)
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
    is_encrypted = models.BooleanField(default=True, verbose_name="Encrypted ?")
    is_masked = models.BooleanField(default=False, verbose_name="Masked ?")
    is_partition_key = models.BooleanField(default=False, verbose_name="Partition Key ?") # if the object is of type "TimeSeries" atleast one attribute should be of datetime type.
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

class Dimensions(models.Model):
    class Meta:
        db_table = "dimensions"

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False,verbose_name="DataModel")
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False, verbose_name="Object")
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, editable=False)
    dimension_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Dimension Code (generated)", editable=False)
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

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False,verbose_name="DataModel")
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False, verbose_name="Object")
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE, editable=False)
    measure_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Measure Code (generated)", editable=False)
    measure_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Measure Description", null=True)
    measure_type = models.CharField(max_length=constants["LOV"]["maxLength"], choices= [x.value for x in MeasureTypes], verbose_name="Measure Types (multi-choice)")
    measure_operators = models.CharField(max_length=constants["LOV"]["maxLength"], choices=[x.value for x in MeasureOperators], verbose_name="Measure Operators (multi-choice)")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Each Object can have 1:many datasources to ingest data from.
# Each active datasource will have a global unique ID and an indiviudal schedule which ETL Engine will check and execute the ingestion process.
# Ingestion can be Batch (default) or Streaming (to be done). Only Batch type ingestion will have a schedule defined.
# Ingestion can be Incremental or Full Load Type. For Incremental: ETL/Workflow Engine will do an append on the destination (default)
# For Full Load: System will do a delete and load every time on the destinations
class DataSources(models.Model):
    class Meta:
        db_table = "data_sources"

    source_connection_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name ="Datasource Connection Code (generated)", editable=False)
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False, verbose_name="Data model")
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules],verbose_name="Module", editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False, verbose_name="Object")
    source_connector_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in SourceConnectorCategories], verbose_name="Data Source Connector Category", editable=False)
    source_connector_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],
                                                 choices=[x.value for x in SourceConnectorTypes],
                                                 verbose_name="Data Source Connector Type", editable=False)
    datasource_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Data Source Name")
    datasource_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Data Source Description", null=True)
    datasource_schedule = models.CharField(max_length=constants["SCHEDULE"]["maxLength"]) # as CRON Schedule
    is_batch = models.BooleanField(default=True, verbose_name="Batch Type Ingestion ?")  # Default mode. Batch uploads.
    is_streaming = models.BooleanField(default=False, verbose_name="Streaming Ingestion ?",
                                       editable=False)  # Streaming flag is allowed to be set only if the Connector type supports
    is_incremental_load = models.BooleanField(default=True,
                                              verbose_name="Incremental Load ?")  # System perform incremental update. Will check if the existing file is newer and has not been uploaded.
    is_full_load = models.BooleanField(default=False,
                                       verbose_name="Full Load ?")  # system performs complete upload of the file. Wont check for datetime stamp of the file
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Datasets is created to capture the metadata involved in mapping the source with the destination (object)
# multiple data sources can be mapped to a single dataset if the source structure and mappings are the same.
# For example: If there are multiple folders sending in similar file format data to the system, all these data sources will be mapped to a single dataset
class Datasets(models.Model):
    class Meta:
        db_table = "datasets"

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE,verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False, verbose_name="Object/Schema")
    data_source = models.ForeignKey(DataSources, verbose_name="DataSource", on_delete=models.CASCADE)
    dataset_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name ="Dataset Code (generated)", editable=False)
    dataset_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Dataset Name")
    dataset_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Dataset Description", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# Maps Source format with the Object Schema.
# Includes Transformation logic (to do)
class Mappings(models.Model):
    class Meta:
        db_table = "mappings"

    dataset = models.ForeignKey(Datasets,verbose_name="Dataset", on_delete=models.CASCADE)
    data_source = models.ForeignKey(DataSources, verbose_name="DataSource", on_delete=models.CASCADE)
    source_attribute = models.CharField(max_length=255, verbose_name="Source Attribute Name (column)")
    target_attribute = models.CharField(max_length=255, verbose_name="Source Attribute Name (column)")
    transformation_function = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, choices=[x.value for x in TransformationFunction], verbose_name="Transformation Function", editable=False)
    transformed_value = models.CharField(max_length=255, verbose_name="Transformed Value", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


#Batch Logs is used to maintain a log of all the ingress & egress events
class BatchLogs(models.Model):
    class Meta:
        db_table = "batch_logs"

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    batch_id = models.UUIDField(default = uuid.uuid4(), verbose_name="Batch Id")        # unique batch id is created for each ingestion attempt
    dataset = models.ForeignKey(Datasets, verbose_name="Datasets", on_delete=models.CASCADE)
    batch_status = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in BatchStatus], default=BatchStatus.N, verbose_name="Batch Status", editable=False)
    start_time = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Start Time")
    end_time = models.DateTimeField(default=django.utils.timezone.now, verbose_name="End Time")
    duration = models.PositiveIntegerField(default=0, verbose_name="Duration (msec)")  # default = 0
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# This class is used for file type data source properties
class DataSourcesLocalFile(models.Model):
    class Meta:
        db_table = "data_sources_file"

    datasource = models.ForeignKey(DataSources, on_delete=models.CASCADE, verbose_name = "DataSource")
    file_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in DataSourceFileTypes], verbose_name=" File Type")
    file_extension = models.CharField(max_length=5, null=True, verbose_name="File Extension")
    file_name = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True)  # used for fixed file name
    file_name_regex = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True, verbose_name="File Name Pattern")  # used for varying file names
    base_folder_path = models.TextField(verbose_name="Base Folder Path")  # absolute path of the source data
    error_folder_path = models.TextField(verbose_name="Error Folder Path", null=True)  # absolute path. Move error files to this folder if set
    archive_folder_path = models.TextField(verbose_name="Archive Folder Path", null=True)  # absolute path
    delimiter = models.CharField(max_length=2, verbose_name="Delimiter")
    ignore_header = models.BooleanField(default=False, verbose_name="Ignore Header ?")  #ignores first line of the data
    start_line_number = models.PositiveSmallIntegerField(default=0) # starting row number to be read
    end_line_number = models.PositiveIntegerField(default=0)    # default 0 means till EOF
    skip_lines_from_end = models.PositiveSmallIntegerField(default=0)    # default 0 means no skip lines
    max_file_size_mb = models.PositiveIntegerField(default=0, verbose_name="Max File size allowed (MB)")    # default 0 means any size. No limit
    hierarchy = models.ForeignKey(OrgHierarchy, null=True, verbose_name="Org Hierarchy", on_delete=models.CASCADE)  # use user defined hierarchy along with the is_enforce_hierarchy flag (to be set)
    is_archive_enabled = models.BooleanField(default=True, verbose_name="To be Archived ?")        # allows auto archival. Datasets history is persisted for 30 days (by default) in the system. Older one are deleted.
    is_partial_ingestion = models.BooleanField(default=False, verbose_name="Partial Ingestion?")        # allows bad records to be segregated and saved in the error file. Good records are persisted in the system
    is_encrypted = models.BooleanField(default=False, verbose_name="Is Encrypted ?")
    encryption_key = models.TextField(null=True, verbose_name="Public Key for decryption")
    is_folder_source = models.BooleanField(default=False, verbose_name="Use Folder as Source ?")     # system will pick up all files from this folder (file name shouldnt be specified in this case)
    is_enforce_hierarchy = models.BooleanField(default=False, verbose_name="Enforce Org Hierarchy on the folder ?") # System will enforce the user defined hierarchy on the folder structure
    is_zipped = models.BooleanField(default=False, verbose_name="Is Zipped ?")
    is_password_protected = models.BooleanField(default=False, verbose_name="Is Password Protected ?")
    file_password = models.CharField(max_length=128, null=True,verbose_name="File Password")
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
    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules],verbose_name="Module", editable=False)
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False)
    dataset = models.ForeignKey(Datasets,on_delete=models.CASCADE, editable=False)
    datatarget_connector_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in DestinationConnectors], verbose_name="Data target Connector Type", editable=False)
    datatarget_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Data target Name")
    datatarget_description = models.CharField(max_length=constants["DESCRIPTION"]["maxLength"], verbose_name="Data target Description", null=True)
    datatarget_properties = models.TextField(null=True) # as json
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

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, verbose_name="Catalog")
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module")
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, editable=False, verbose_name="Object/Schema")
    container_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Container Code (generated)", editable=False)
    container_type = models.CharField(max_length=255,  choices=[x.value for x in ContainerTypes], verbose_name="Container Type")
    container_name = models.CharField(max_length=255, verbose_name="Container Name")
    container_description = models.TextField(verbose_name="Description", null=True)
    processing_sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")
    container_category = models.CharField(max_length=255, choices=[x.value for x in ContainerCategories], verbose_name="Container Category")
    container_storage_properties = models.TextField(verbose_name="Storage Properties",null=True)  #json. Engine Type, Default Location etc
    container_schema = models.TextField(verbose_name="Schema Definition", editable=False, null=True)    # json defining the Column attributes for the container
    filter_conditions = models.TextField(null=True, verbose_name="Filter Conditions")   # json
    filter_columns = models.TextField(null=True, verbose_name="Filter Columns")   # json
    is_default = models.BooleanField(default=False, verbose_name="Is Default ?")    # atleast 1 default container to be set. This container will hold the raw data from all the datasets
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

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    container = models.ForeignKey(Containers, verbose_name="Container", on_delete=models.CASCADE)
    aggregate_code  = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Aggregate Code (generated)", editable=False)
    aggregate_storage_properties = models.TextField(verbose_name="Storage Properties", null=True)  #json. Engine Type, Default Location etc
    aggregate_description = models.TextField(verbose_name="Description", null=True)
    aggregate_schema = models.TextField(verbose_name="Schema Definition", editable=False, null=True)  # json defining the Column attributes for the aggregate
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")
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
    dimension_display_name = models.CharField(max_length=255, verbose_name="Dimension Display Name", null=True)
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



# Dashboards are user defined pre-aggregated / run time aggregated data based on business functions and at the module level. Permissions are granted to specific roles to view the Dashboards
# Dashboards are populated post aggregation step during the ingestion process by ETL/Workflow engine
# Each DASHBOARD consists of 1 or many components used for further aggregating and displaying data related to business sub-function
# System provides out of box Dashboards for each module. User can define their own custom Dashboards and define the data population mode.
# Data Population: 2 types Per-Aggregated and Run time.
# Pre-Aggregated DASHBOARDS - Data is aggregated during the ingestion process and stored in the repository
# Run Time: DASHBOARD definitions are decoded at run time and dynamic queries are formed and executed by the Query Engine and results are returned in the format defined in the DASHBOARD
# Each component controls how the aggregated data should be displayed on the UI. 2 Types: Widget and Tabular
# Widget based DASHBOARD display data as an independent control using Graphs and Indicators (singular value based display) - Multiple queries are used for this
# Tabular type Dashboards displays data as a table (single Query is used)
class Dashboards(models.Model):
    class Meta:
        db_table = "dashboards"

    tenant_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Tenant", editable=False)
    site_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Environment/Instance", editable=False)
    catalog = models.ForeignKey(Catalogs, on_delete=models.CASCADE, editable=False)
    datamodel = models.ForeignKey(DataModels, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in Modules], verbose_name="Module", editable=False)
    dashboard_type = models.CharField(max_length=255, choices=[x.value for x in DashboardType], verbose_name="Dashboard Data Population type")
    dashboard_code  = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Dashboard Code (generated)", editable=False)
    dashboard_storage_properties = models.TextField(verbose_name="Storage Properties", null=True)  #json. Engine Type, Default Location etc
    dashboard_reference_class = models.CharField(max_length=255, verbose_name="Dashboard Reference Class", editable=False, null=True)  # Refer to Adbiz Namespace for Dashboards (out of box offerings)
    dashboard_name = models.CharField(max_length=255, verbose_name="Dashboard Name", null=True) #*
    dashboard_title = models.CharField(max_length=255, verbose_name="Dashboard Title", null=True)  #* remove null
    dashboard_sub_title = models.CharField(max_length=255, verbose_name="Dashboard Sub Title", null=True)  #* remove null
    dashboard_description = models.TextField(verbose_name="Dashboard Description", null=True)
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")     # Priority when rebuilding
    is_system_defined = models.BooleanField(default=True, verbose_name="Is System Defined?")    # if true need to set the dashboard_class
    is_incremental =  models.BooleanField(default=True, verbose_name="Incremental ?")   # Entire DASHBOARD and its components data population gets appended during data ingestion process
    is_rebuild = models.BooleanField(default=False, verbose_name="Rebuild Everytime ?") # Entire DASHBOARD and its components data population get rebuilt every time using the source Container during the data ingestion process
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

#Each Dashboard will have set of components. Each component defines the type of graph, display properties & data
class DashboardComponents(models.Model):
    class Meta:
        db_table = "dashboard_components"

    dashboard = models.ForeignKey(Dashboards, on_delete=models.CASCADE, editable=False, verbose_name="Dashboard")
    container = models.ForeignKey(Containers, verbose_name="Container", on_delete=models.CASCADE)
    aggregate = models.ForeignKey(Aggregates, verbose_name="Aggregate", on_delete=models.CASCADE)
    component_code  = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Dashboard Code (generated)", editable=False)
    component_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in ComponentCategory], verbose_name="Component Category")
    component_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in ComponentDisplayType], verbose_name="Component Type")
    component_sub_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], default =  ComponentSubDisplayType.G, choices=[x.value for x in ComponentSubDisplayType], verbose_name="Component Sub Type")
    component_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Dashboard Name")
    component_title = models.CharField(max_length=255, verbose_name="Component Title", null=True)  # * remove null
    component_tooltip = models.CharField(max_length=255, verbose_name="Component Tooltip", null=True)  # * remove null
    component_description = models.TextField(verbose_name="Dashboard Description", null=True)
    component_reference_class = models.CharField(max_length=255, verbose_name="Component Class Reference", null=True) # Refer to Adbiz Namespace for inbuilt components
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")  # Priority when rebuilding
    display_properties = models.TextField(verbose_name="Display Properties")    #JSON: Contains Display settings (ex: if used iwth Chart.js lib - Graph Type, Color, x Axis labels, Y Axis Parameters)
    data_filters = models.TextField(verbose_name="Data Filters", null=True) # JSON: Contains filters for each Dimension & Measures as per the selected Aggregate in the component definition
    data_source_methods = models.TextField(verbose_name="Data Source")  # JSON. Defines the API URL and the request header along with the payload.
    component_query = models.TextField(verbose_name="Component Query", null=True)  # *
    is_system_defined = models.BooleanField(default=True, verbose_name="Is System Defined?")  # if true need to set the component_class
    is_incremental =  models.BooleanField(default=True, verbose_name="Incremental ?")   # components data population gets appended during data ingestion process. Overrides Dashboard settings
    is_rebuild = models.BooleanField(default=False, verbose_name="Rebuild Everytime ?")  # components data population get rebuilt every time using the source Container during the data ingestion process. Overrides Dashboard settings
    is_auto_referesh = models.BooleanField(default=False, verbose_name="Auto Refresh ?")
    refresh_interval  = models.PositiveSmallIntegerField(default=0, verbose_name="Auto Refresh Interval (ms)")  # data refresh happens on the UI every X seconds as set. Default=0 means On Demand Refresh.
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class DashboardIndicators(models.Model):
    class Meta:
        db_table = "dashboard_component_indicators"

    dashboard = models.ForeignKey(Dashboards, on_delete=models.CASCADE, editable=False, verbose_name="Dashboard")
    component = models.ForeignKey(DashboardComponents, on_delete=models.CASCADE, editable=False, verbose_name="Component")
    component_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"],
                                      verbose_name="Dashboard Code (generated)", editable=False)
    indicators = models.TextField(verbose_name="Indicators", null=True)  # JSON: Defines indicators (singular values)
    indicator_reference_class = models.CharField(max_length=255, null=True, verbose_name="Indicator Reference Class")  # Refers to adbiz Namespace definitions for inbuilt indicators
    indicator_name = models.CharField(max_length=255, verbose_name="Indicator Name")
    indicator_description = models.TextField(verbose_name="Indicator Description", null=True)
    query_definition = models.TextField(verbose_name="Query definition", null=True, editable=False)  # json. defines the query structure to be later converted into a SQL
    sequence = models.PositiveSmallIntegerField(default=1, verbose_name="Sequence")  # Priority when rebuilding
    is_system_defined = models.BooleanField(default=True, verbose_name="Is System Defined?")  # if true need to set the component_class
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)

# Data lake information is synchronized from CORE Engine. Only the applicable Data lake info (for a particular tenant, site, instance combination) is synchronized.
# This avoids frequent calls to CORE engine.

class DataLakes(models.Model):
    class Meta:
        managed= False

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