from django.db import models
from django.db.models import Model
from django.apps import apps
#from django_audit_fields.model_mixins import AuditModelMixin
import uuid
import re
import datetime
from django_utils.choices import Choice, Choices

#from core.coreEngine import CoreEngine
from components.product.productEngine import ProductEngine

pe = ProductEngine()
constants = pe.constants
lookups = pe.lookups



class ProductEngine(models.Model):
    class Meta:
        db_table = "product_engine"

    product_instance_id = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"], unique=True, verbose_name= "Product Instance ID")
    root_namespace = models.CharField(max_length=constants["CODE"]["maxLength"], verbose_name="Namespace")
    registered_to = models.CharField(max_length=constants["PERSON_NAME"]["maxLength"])
    activation_file_location = models.CharField(max_length=constants["FILE_LOCATION"]["maxLength"])
    engine_id = models.CharField(max_length=constants["GENERATED_ID"]["maxLength"])
    activation_key = models.CharField(max_length=constants["ACTIVATION_KEY"]["maxLength"])
    activation_dt = models.DateTimeField(editable=False)
    host_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"],editable=False)
    host_ip_address = models.GenericIPAddressField(max_length=32)
    os_release = models.CharField(max_length=32, null = True)
    release_info = models.CharField(max_length=255, null = True)



class Customer(models.Model):
    class Meta:
        db_table = "customer"

    class CATEGORY(Choices):
        Proprietorship = Choice('Proprietorship',('Proprietorship'))
        OPC = Choice('One Person Company',('One Person Company'))
        Partnership = Choice('Traditional Partnership',('Traditional Partnership'))
        LLP = Choice('Limited Liability Partnership (LLP)',('Limited Liability Partnership (LLP)'))
        PVT = Choice('Private Limited Company',('Private Limited Company'))

    customer_id = models.UUIDField(default=uuid.uuid4, unique=True)
    customer_name = models.CharField(max_length=constants["ENTITY_NAME"]["maxLength"])
    customer_code = models.CharField(max_length=constants["CODE"]["maxLength"], unique=True)
    registration_number = models.CharField(max_length=constants["REGISTRATION_NUMBER"]["maxLength"], unique=True)
    registered_dt = models.DateTimeField(null = True)
    country = models.CharField(max_length=constants["COUNTRY_CODE"]["maxLength"])
    state = models.CharField(max_length=constants["STATE_CODE"]["maxLength"], null = True)
    category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null = True, choices=CATEGORY.choices, default = CATEGORY.PVT)
    sub_category = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null = True) #, choices=lookups["CompanySubCategories"])
    type = models.CharField(max_length=constants["LOOKUP_VALUE"]["maxLength"], null = True) #, choices=lookups["CompanyTypes"])
    website_url = models.URLField(max_length=constants["URL"]["maxLength"], null = True)
    isActive = models.BooleanField(default = True)
    isActivated = models.BooleanField(default = False)



    # createdOn = models.DateTimeField(default=datetime.date.today,)
    # lastUpdatedOn = models.DateTimeField(default=datetime.date.today,)
    # lastUpdatedBy = models.CharField()

    #audit_log = AuditLog()



    @staticmethod
    def generate_customer_code(self):
        try:

            pass
        except Exception as e:
            print(e)



class LicensingInfo(models.Model):
    class Meta:
        db_table = "license_info"

    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE )
    #license_type = models.
#
# class CustomerContactDetails(models.Model):
#     class Meta:
#         db_table = "customer_contact_details"

    #customerId = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # contact_person_first_name = models.CharField()
    # contact_person_last_name = models.CharField()
    # contact_person_designation = models.CharField()
    # contact_Email = models.EmailField()
    # contact_phone_code = models.IntegerField()
    # contact_phone_number = models.IntegerField()


# class CustomerAddressDetails(models.Model):
#     class Meta:
#         db_table = "customer_address_details"

    #customerId = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # address_type =
    # address_line_1 =
    # address_line_2 =
    # address_line_3 =
    # country_code =
    # city =
    # state =
    # ZipCode =
    # is_active =


# class CustomerActivationDetails(models.Model):
#    class Meta:
#         db_table = "customer_activation_details"
#     customerId = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     activatedDateTime = models.DateTimeField(null=True)
#     deActivatedDateTime = models.DateTimeField()
#     secretPhrase  = models.CharField(max_length=constants["SECRET_PHRASE"]["maxLength"])
#     secretKey = models.TextField()
#     product_engine_id = models.ForeignKey(ProductEngine, on_delete = models.CASCADE)
#     customer_namespace = models.CharField(max_length=128)
#
#     def generate_scret_key(self):
#         try:
#             # uses the secret phrase defined by the customer to generate the secret key
#             pass
#         except Exception as e:
#             print(e)
# #
# class LicenseInfo(models.Model):
#     customerId = models.ForeignKey(Customer, )

#
# class CustomerAddress(models.Model):
#     customerId = models.ForeignKey(Customer)
#     addressType
#     address_1 =
#     address_2 =
#     address_3 =
#     city =
#     state =
#     country =
#     iActive = models.BooleanField()
#
#     class Meta:
#         db_table = "customer_address"