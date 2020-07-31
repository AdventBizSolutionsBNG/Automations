import django
from django.db import models
import uuid
import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import login
import random

# Create your models here.

class AdbizUIEngine(models.Model):

    class Meta:
        db_table = "engine_metadata"

    ui_engine_code = models.CharField(max_length=255, unique=True, verbose_name="UI Engine Code (generated)")
    core_engine_code = models.CharField(max_length=255, verbose_name="Core Engine Code", editable=False)
    tenant_code = models.CharField(max_length=255, verbose_name="Tenant")
    site_code = models.CharField(max_length=255, verbose_name="Site", editable=False)
    instance_code = models.CharField(max_length=255, verbose_name="Environment/Instance", editable=False)
    tenant_namespace = models.CharField(max_length=8, verbose_name="Tenant Namespace", editable=False, null= True)  #*
    activation_file_location = models.CharField(max_length=255, verbose_name="Activation File Location")
    activation_key = models.CharField(max_length=255, verbose_name=" Activation Key (generated)", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time")
    host_name = models.CharField(max_length=128, verbose_name="Host Name")
    host_ip_address = models.GenericIPAddressField(max_length=32, verbose_name="Host IP Address")
    os_release = models.CharField(max_length=32, null=True, verbose_name="OS Release Version")
    release_info = models.CharField(max_length=255, null=True, verbose_name="Version Details")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date")
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date")
    engine_properties = models.TextField(verbose_name="Engine Details", null=True)  # json.
    core_engine_details = models.TextField(verbose_name="Core Engine Details", null=True)  # json. Used by UI engine to connect to the Core Engine
    catalog_engine_details = models.TextField(verbose_name="Catalog Engine Details", null=True)  # json. Used by UI engine to connect to Catalog engine
    io_engine_details = models.TextField(verbose_name="IO Engine Details", null=True)  # json. Used by UI engine to connect to IO engine
    catalog_details = models.TextField(null=True, verbose_name="Catalog Details") # Json for Catalog details
    datamodel_details = models.TextField(null=True, verbose_name="Datamodel Details") # json for data model details
    is_activated = models.BooleanField(default=False, verbose_name="Activated ?")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=32, verbose_name="Last Updated By", editable=False)


class AdbizUIEngineActivations(models.Model):

    class Meta:
        db_table = "engine_activations"

    ui_engine_code = models.ForeignKey(AdbizUIEngine, verbose_name="UI Engine ID (generated)", on_delete=models.CASCADE)
    core_engine_code = models.CharField(max_length=64, verbose_name="Core Engine ID", editable=False)
    activation_key = models.CharField(max_length=64, editable=False, verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time", editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On", editable=False)
    last_updated_by = models.CharField(max_length=32, verbose_name="Last Updated By", editable=False)


class AdbizModuleActivations(models.Model):
    class Meta:
        db_table = "module_activations"

    ui_engine = models.ForeignKey(AdbizUIEngine, verbose_name="UI Engine ID (generated)", on_delete=models.CASCADE)
    module = models.CharField(max_length=32, editable=False)
    activation_key = models.CharField(max_length=64, editable=False, verbose_name="Activation Key")
    validity_start_date = models.DateTimeField(null=True, verbose_name="Validity Start Date", editable=False)
    validity_end_date = models.DateTimeField(null=True, verbose_name="Validity End Date", editable=False)
    activation_dt = models.DateTimeField(verbose_name="Activation Date Time", editable=False)
    deactivation_dt = models.DateTimeField(editable=False, null=True, verbose_name="Deactivation Date Time")
    is_active = models.BooleanField(default=True, verbose_name="Active ?")
    created_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Created On", editable=False)
    last_updated_on = models.DateTimeField(default=django.utils.timezone.now, verbose_name="Last Updated On",
                                           editable=False)
    last_updated_by = models.CharField(max_length=32, verbose_name="Last Updated By", editable=False)


class AdbizUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_account = uuid.uuid4()
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_system_user(self, email, password, **extra_fields):
        """
        Creates and saves a system user with the given email and password.
        """
        extra_fields.setdefault('is_system_user', True)
        extra_fields.setdefault('is_staff_user', False)
        user = self.create_user(email, password=password, **extra_fields)
        #user.save(using=self._db)
        #return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_super_user', True)
        extra_fields.setdefault('is_system_user', True)
        extra_fields.setdefault('is_staff_user', False)

        engine = AdbizUIEngine.objects.filter(is_active=True)
        user = self.create_user(email, password=password, **extra_fields)

        #user.save(using=self._db)
        #return user


# Custom User Model. Each UI Engine Instance will have its own set of UI Users for particular Module
class AdbizUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "users"

    user_account = models.CharField(max_length=255, null=True, unique=True, verbose_name="User Account (generated)")
    email = models.EmailField(max_length=64, unique=True, verbose_name="Login (email)")
    first_name = models.CharField(max_length=64, verbose_name="First Name", null=True)
    last_name = models.CharField(max_length=64, null=True, verbose_name="Last Name")
    dob = models.DateField(verbose_name="Date of birth", null=True)
    engine = models.ForeignKey(AdbizUIEngine, verbose_name="UI Engine ID (generated)", on_delete=models.CASCADE)
    joined_dt = models.DateTimeField(default=timezone.now, verbose_name="Joining Date")
    is_staff = models.BooleanField(default=False, verbose_name="App Admin User?")
    is_super_user = models.BooleanField(default=False, verbose_name="Super User?")
    is_system_user = models.BooleanField(default=False, verbose_name="System User?")
    is_active = models.BooleanField(default=True,verbose_name="Active?")
    is_locked = models.BooleanField(default=False, verbose_name="Locked?")
    login_attempts = models.SmallIntegerField(default=0 , verbose_name="Login Attempts", editable=False)
    last_login_dt = models.DateTimeField(null=True, verbose_name="Last Login", editable=False)
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created on")
    last_updated_on = models.DateTimeField(default=timezone.now, verbose_name="Last updated on")
    last_updated_by = models.CharField(max_length=64, verbose_name="Last updated By")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email

    def get_permissions(self):
        return True

    @property
    def check_super_user(self):
        return self.is_superuser

    @property
    def check_system_user(self):
        return self.is_systemuser

    @property
    def check_active(self):
        return self.is_active

    @property
    def check_locked(self):
        return self.is_locked

    def get_engine_instance(self):
        return self.engine_id

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    objects = AdbizUserManager()


# Set of Roles defined for each Module. Roles can be System or User defined. System Defined roles cannot be added or modified from UI.
# User defined roles can be added by the module admin only and can be mapped to an existing system role only.
# Service Accounts are created for backend operation like ETL's or any downstream applications that calls Adbiz API
class AdbizRoles(models.Model):

    class Meta:
        db_table = 'roles'

    role_name = models.CharField(max_length=64, verbose_name="Role Name")
    role_description = models.CharField(max_length=256, verbose_name="Role Description")
    module = models.CharField(max_length=32, verbose_name="Module")
    role_code = models.CharField(max_length=32, verbose_name="Role Code",  null=True) #*
    system_role_reference = models.CharField(max_length=255, verbose_name="System Role", null=True)    #refers to inbuilt system role
    is_system = models.BooleanField(default=False, verbose_name="Is System?", editable=False)
    is_service_account = models.BooleanField(default=False, verbose_name="Is a Service Account?", editable=False) # for running background jobs
    is_module_admin = models.BooleanField(default=False, verbose_name="Is Module Admin?", editable=False)
    is_active = models.BooleanField(default=True,  verbose_name="Is Active?")


# Privilege: Permission set for each module. Roles are granted applicable privilges. Users are assiged to Roles which in turn inherit the Privileges.
class AdbizPrivileges(models.Model):

    class Meta:
        db_table = "privileges"

    privilege_name = models.CharField(max_length=64, verbose_name="Privilege Name")
    privilege_description = models.CharField(max_length=256, verbose_name="Privilege Description")
    module = models.CharField(max_length=32, verbose_name="Module")
    privilege_code = models.CharField(max_length=32, null=True, verbose_name="Privilege Code") #*
    is_create = models.BooleanField(default=False, verbose_name="Create?")
    is_read = models.BooleanField(default=True, verbose_name="Read?")
    is_update = models.BooleanField(default=False, verbose_name="Update?")
    is_delete = models.BooleanField(default=False, verbose_name="Delete?")
    is_execute = models.BooleanField(default=False, verbose_name="Execute?")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")


# mapping table between roles and privileges
class AdbizRolePrivileges(models.Model):
    class Meta:
        db_table = "role_privileges"

    module = models.CharField(max_length=32, verbose_name="Module")
    role = models.ForeignKey(AdbizRoles, verbose_name="Role", on_delete=models.CASCADE)
    privileges = models.ForeignKey(AdbizPrivileges, on_delete=models.CASCADE, verbose_name="Privileges")     # multi-select


class AdbizMenuItems(models.Model):

    class Meta:
        db_table = "menu_items"

    module = models.CharField(max_length=32, verbose_name="Module")
    menu_name = models.CharField(max_length=64, verbose_name="Menu Name")
    menu_description = models.CharField(max_length=256, verbose_name="Menu Description")
    menu_code = models.CharField(max_length=32, null=True, verbose_name="Menu Item Code", unique=True)
    menu_tooltip = models.CharField(max_length=256, verbose_name="Tooltip")
    menu_url = models.CharField(max_length=256, verbose_name="URL")
    menu_properties = models.TextField(null=True, verbose_name="Properties")
    parent_menu_id = models.PositiveSmallIntegerField(null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=1)
    display_seq = models.PositiveSmallIntegerField(default=1)
    privilege = models.ForeignKey(AdbizPrivileges, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

# Mapping between Menu Items and the System provided roles
class AdbizMenuRoles(models.Model):
    class Meta:
        db_table = "menu_roles"

    menu_items = models.ForeignKey(AdbizMenuItems, on_delete=models.CASCADE)
    role = models.ForeignKey(AdbizRoles, on_delete=models.CASCADE)

class AdbizPreferences(models.Model):

    class Meta:
        db_table = "preferences"

    preference_name = models.CharField(max_length=64, verbose_name="Preference Name")
    preference_description = models.CharField(max_length=256, verbose_name="Preference Description")
    preference_code = models.CharField(max_length=32, null=True, verbose_name="Preference Code", unique=True) #*
    module = models.CharField(max_length=32, verbose_name="Module", null=True)
    default_value = models.CharField(max_length=32, verbose_name="Default Value")


class AdbizUserPreferences(models.Model):

    class Meta:
        db_table = "user_preferences"

    module = models.CharField(max_length=32, verbose_name="Module",null=True)   # For generic settings, module value will be null
    user = models.ForeignKey(AdbizUser, on_delete=models.CASCADE)
    preference = models.ForeignKey(AdbizPreferences, on_delete=models.CASCADE)
    preference_value = models.CharField(max_length=256)
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created on")
    last_updated_on = models.DateTimeField(default=timezone.now, verbose_name="Last updated on")
    last_updated_by = models.CharField(max_length=64, verbose_name="Last updated By")


# Maps Users with predefined Roles (one or many) for each Module (one or many)
# Final Permission set for a user is a superset of all the privileges
class AdbizUserAccess(models.Model):

    class Meta:
        db_table = "user_access"

    user = models.ForeignKey(AdbizUser, on_delete=models.CASCADE)
    module = models.CharField(max_length=32, verbose_name="Module")
    role = models.ForeignKey(AdbizRoles, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created on")
    last_updated_on = models.DateTimeField(default=timezone.now, verbose_name="Last updated on")
    last_updated_by = models.CharField(max_length=64, verbose_name="Last updated By")



class AdbizDashboards(models.Model):

    class Meta:
        managed = False
        db_table = "Dashboards"
        # abstract = False

    module = models.CharField(max_length=32, verbose_name="Module")
    dashboard_code = models.CharField(max_length=255, verbose_name="Dashboard Code")
    dashboard_class = models.CharField(max_length=32, verbose_name="Dashboard Reference Class")
    dashboard_title = models.CharField(max_length=32, verbose_name="Dashboard Title")
    dashboard_sub_title = models.CharField(max_length=32, verbose_name="Dashboard Sub Title")

