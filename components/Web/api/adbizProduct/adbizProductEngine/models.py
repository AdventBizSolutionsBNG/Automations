from django.db import models
from django.db.models import Model
from django.apps import apps
import uuid
import django.utils
from django.utils import timezone
from django.forms import ModelForm, Textarea
from django_utils.choices import Choice, Choices
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from components.product.productEngine import ProductEngine
from components.product.packages.lookups import *

pe = ProductEngine()
constants = pe.constants
lookups = pe.lookups

# Custom Product Engine (PE) model to manage the product activation. PE will be installed on a separate host on cloud accessible by all the Customer installation sites.
# PE can be also hosted in the Clients environment managing the Client specific installations. Ony product Admin should be able to manage the PE instance in this case.
# PE houses all the customers and their licensing needs (new & renewals). PE also generates unique activation keys for customer specific installations.
# Activation keys are then retrieved by Core Engine (CE) inside Customer Installations to activate instances/modules/engines.
#


class ProductEngine(models.Model):
    class Meta:
        db_table = "engine_metadata"

    product_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Product Engine Code (generated)", editable=False)
    root_namespace = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Root Namespace")
    registered_to = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], verbose_name="Registered To")
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"], verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], verbose_name=" Activation Key (generated)", editable = False )
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time")
    host_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"],   verbose_name="Host Name")
    host_ip_address = models.GenericIPAddressField(max_length=32, verbose_name="Host IP Address")
    os_release = models.CharField(max_length=32, null = True, verbose_name="OS Release Version")
    release_info = models.CharField(max_length=255, null = True, verbose_name="Version Details")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                     editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                         editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                     editable=False)
#
#
# class ProductEngineForm(Model.Form):
#     class Meta:
#         model = ProductEngine
#         fields = '__all__'
#         exclude = ['engine_instanace_id', 'activation_file_location', 'created_on', 'last_updated_on', 'last_updated_by',]
#         localized_fields = ('created_on', 'last_updated_on')


class Customers(models.Model):
    class Meta:
        db_table = "customers"

    product_engine= models.ForeignKey(ProductEngine, verbose_name="Product Engine", on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"], verbose_name="Customer Name")
    customer_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Customer Code (generated)", editable=False)
    customer_namespace = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Customer Namespace")
    registration_number = models.CharField(max_length=constants["REGISTRATION_NUMBER"]["maxLength"], unique=True, verbose_name="Unique Registration Number (any)")
    registration_dt = models.DateTimeField( verbose_name="Registration Date")
    company_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],
                                        choices=[x.value for x in CompanyCategories],
                                        default=CompanyCategories.get_value(CompanyCategories.PVT), null=True, verbose_name="Company Category")
    company_sub_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],
                                            choices=[x.value for x in CompanySubCategories],
                                            default=CompanySubCategories.get_value(CompanySubCategories.PVT), null=True,
                                            verbose_name="Company Sub Category")  # , choices=lookups["CompanySubCategories"])
    company_class = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null=True,
                                     verbose_name="Company Class")  # , choices=lookups["CompanySubCategories"])
    company_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],
                                    choices=[x.value for x in CompanyTypes],
                                    default=CompanyTypes.get_value(CompanyTypes.L), null=True, verbose_name="Company Type")
    city = models.CharField(max_length=constants["CITY"]["maxLength"], null=True, verbose_name="City")
    state = models.CharField(max_length=constants["STATE_CODE"]["maxLength"], null = True, verbose_name="State")
    country = models.CharField(max_length=constants["COUNTRY_CODE"]["maxLength"], verbose_name="Country")
    website_url = models.URLField(max_length=constants["URL"]["maxLength"], null = True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                     editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                         editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                     editable=False)


    @staticmethod
    def generate_customer_code(self):
        try:
            pass
        except Exception as e:
            print("Error in generating Customer Code!!!", e )


    def generate_customer_id(self):
        try:
            pass
        except Exception as e:
            print("Error in generating Customer ID!!!", e )


class CustomerContactDetails(models.Model):
    class Meta:
        db_table = "customer_contact_details"

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    contact_person_first_name = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], verbose_name="First Name")
    contact_person_last_name = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], verbose_name="Last Name", null=True)
    contact_person_designation = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], verbose_name="Designation", null=True)
    contact_Email = models.EmailField(null=True, verbose_name="Email")
    contact_phone_code = models.IntegerField(null=True, verbose_name="Country Code")
    contact_phone_number = models.IntegerField(null=True, verbose_name="Phone")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                     editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                         editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                     editable=False)


class CustomerLocations(models.Model):
    class Meta:
        db_table = "customer_locations"

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Customer")
    address_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],  choices= [x.value for x in AddressTypes], default = AddressTypes.get_value(AddressTypes.O)),
    address_line_1 = models.CharField(max_length=constants["ADDRESS_LINE"]["maxLength"], verbose_name="Address Line 1", null=True)
    address_line_2 = models.CharField(max_length=constants["ADDRESS_LINE"]["maxLength"], verbose_name="Address Line 2", null=True)
    address_line_3 = models.CharField(max_length=constants["ADDRESS_LINE"]["maxLength"], verbose_name="Address Line 2", null=True)
    country_code = models.CharField(max_length=constants["COUNTRY_CODE"]["maxLength"], verbose_name="Country", null=True),
    city = models.CharField(max_length=constants["CITY"]["maxLength"], verbose_name="City", null=True),
    state = models.CharField(max_length=constants["STATE_CODE"]["maxLength"], verbose_name="State", null=True),
    ZipCode = models.CharField(max_length=10, verbose_name="Zip Code", null=True),
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False )
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By", editable=False)


# Summary table for all Licenses issued
# Keeps track of all the activations of different Engines & modules carried out at different customers.
# Single Product Engine will keep track of all these activations.
# Product Engine is involved in activation of Core Engines only (at customer premises). Passes on the licensing information (incl updates) to respective Core Engine.
# Core Engine will manage activations of all the engines hosted in Customer Premises.
# Core Engine will sync the activations to the Product Engine from time to time.
class LicensingInfo(models.Model):
    class Meta:
        db_table = "license_info"

    product_engine = models.ForeignKey(ProductEngine, verbose_name="Product Engine", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE, verbose_name="Customer")
    license_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"],  choices= [x.value for x in LicensingTypes ], default = LicensingTypes.get_value(LicensingTypes.SUBCRPTN))
    license_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="License Key (generated)")
    duration_days = models.PositiveIntegerField(default=0, verbose_name="Validity (days)")
    active_modules = models.CharField(max_length=255, choices=[x.value for x in Modules], verbose_name="Modules")  # list
    active_engines = models.CharField(max_length=255, choices=[x.value for x in ProcessingEngines], verbose_name="Engines")  # list
    active_envs = models.CharField(max_length=255, choices=[x.value for x in EnvTypes], verbose_name="Environments")  # list
    active_from_dt = models.DateTimeField(verbose_name="Active since")
    active_end_dt = models.DateTimeField(null=True,verbose_name="Active till")
    activated_on_dt = models.DateTimeField(null=True, verbose_name="Activated On")
    deactivated_on_dt = models.DateTimeField(null=True, verbose_name="Deactivated On")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                     editable=False)

# Initially a Site will be activated for a Customer.
# A Customer can host multiple Sites. Only one site per customer is recommended
class LicenseSiteActivations(models.Model):
    class Meta:
        db_table = "license_site_activations"

    license = models.ForeignKey(LicensingInfo, on_delete=models.CASCADE)
    site = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Activation Key")
    activation_dt = models.DateTimeField(editable=False, verbose_name="Activation Date Time")
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    validity_start_date = models.DateTimeField(verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Each Site will host multiple environments. Each environment needs to be first activated to configure engines and module access
class LicenseEnvActivations(models.Model):
    class Meta:
        db_table = "license_env_activations"


    license = models.ForeignKey(LicensingInfo, on_delete=models.CASCADE)
    site = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site")
    env = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in EnvTypes], verbose_name="Environment")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Activation Key")
    activation_dt = models.DateTimeField(editable=False, verbose_name="Activation Date Time")
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    validity_start_date = models.DateTimeField(verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Each Environment will host multiple Engines for data processing. Each Engine/Module needs to be activated individually
class LicenseEngineActivations(models.Model):
    class Meta:
        db_table = "license_engine_activations"

    license = models.ForeignKey(LicensingInfo, on_delete=models.CASCADE)
    site = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site")
    env = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in EnvTypes], verbose_name="Environment")
    processing_engine_type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in ProcessingEngines], verbose_name="Processing Engine")
    processing_engine_code = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Processing Engine")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Activation Key")
    activation_dt = models.DateTimeField(editable=False, verbose_name="Activation Date Time")
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    validity_start_date = models.DateTimeField(verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


# Each Environment will host multiple Modules for Business Users. Each Engine/Module needs to be activated individually
class LicenseModuleActivations(models.Model):
    class Meta:
        db_table = "license_module_activations"

    license = models.ForeignKey(LicensingInfo, on_delete=models.CASCADE)
    site = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], verbose_name="Site")
    env = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices=[x.value for x in EnvTypes], verbose_name="Environment")
    module = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], choices= [x.value for x in Modules], verbose_name="Module")
    activation_key = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"], unique=True, verbose_name="Activation Key")
    activation_dt = models.DateTimeField(editable=False, verbose_name="Activation Date Time")
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    validity_start_date = models.DateTimeField(verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                      editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                       editable=False)


class ContactUs(models.Model):
    class Meta:
        db_table = "contact_us"

    first_name = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], verbose_name="First Name", null = False)
    last_name = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"], verbose_name="Last Name")
    person_email = models.EmailField(null = False, verbose_name="Your Email", help_text='Please provide your email for further communication')
    person_phone = models.TextField(null = True, verbose_name="Your Phone")
    comments = models.TextField(null = True, max_length=1024, verbose_name="Your Comments")
    source = models.CharField(max_length = 64, null = True)
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On",
                                     editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                         editable=False)
    last_updated_by = models.CharField(max_length=constants["USER_NAME"]["maxLength"], verbose_name="Last Updated By",
                                     editable=False)

#
# class ContactUsForm(ModelForm):
#     class Meta:
#         model = ContactUs
#         fields = '__all__'
#         exclude = ['created_on']
#         widgets = {
#                     'comments': Textarea(attrs={'cols': 80, 'rows': 5}),
#                 }
#         labels = {
#             'first_name': _('First Name'),
#         }
#         help_texts = {
#             'first_name': _('Your good name..'),
#         }
#         error_messages = {
#             'first_name': {
#                 'max_length': _("Your name is too long."),
#             },
#         },
#         localized_fields = ('created_on',)
#
#     def validate_data(self):
#         try:
#             fname = self.cleaned_data['first_name']
#             if len(fname)<= 10:
#                 raise ModelForm.ValidationError("First Name too short")
#             return fname
#         except Exception as e:
#             print(e)