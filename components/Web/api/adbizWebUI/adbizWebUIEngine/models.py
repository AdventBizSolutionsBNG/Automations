import django
from django.db import models
import uuid
import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random

# Create your models here.

class AdbizUIEngine(models.Model):

    class Meta:
        db_table = "engine_metadata"

    ui_engine_code = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="UI Engine Code (generated)", editable=False)
    core_engine_code = models.CharField(max_length=64, verbose_name="Core Engine ID",  editable=False)
    customer_code = models.CharField(max_length=64, editable=False)
    customer_namespace = models.CharField(max_length=24, editable=False)
    site_code = models.CharField(max_length=64, editable=False)
    environment_code = models.CharField(max_length=64, editable=False)
    activated_dt = models.DateTimeField(editable=False, null=True)
    activation_key = models.CharField(max_length=64, editable=False)
    validity_start_date = models.DateTimeField(null=True, editable=False)
    validity_end_date = models.DateTimeField(null=True, editable=False)
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


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_system_user(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_system_user = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        engine = AdbizUIEngine.objects.filter(is_active=True)
        user = self.create_user(
            email,
            password=password,
        )
        user.is_super_user = True
        user.is_system_user = True
        user.save(using=self._db)
        return user


# Custom User Model. Each UI Engine Instance will have its own set of UI Users for particular Module
class Users(AbstractBaseUser):
    class Meta:
        db_table = "users"

    user_account = models.CharField(max_length=64, unique=True, verbose_name="User Account (generated)")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=64, verbose_name="First Name", null=True)
    last_name = models.CharField(max_length=64, null=True, verbose_name="Last Name")
    dob = models.DateField(verbose_name="Date of birth", null=True)
    engine = models.ForeignKey(AdbizUIEngine, verbose_name="UI Engine ID (generated)", on_delete=models.CASCADE)
    joined_dt = models.DateTimeField(default=timezone.now)
    is_super_user = models.BooleanField(default=False)
    is_system_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    login_attempts = models.SmallIntegerField(default=0)
    last_login_dt = models.DateTimeField()
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created on")
    last_updated_on = models.DateTimeField(default=timezone.now, verbose_name="Last updated on")
    last_updated_by = models.CharField(max_length=64, verbose_name="Last updated By")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
        return self.is_super_user

    @property
    def check_system_user(self):
        return self.is_system_user

    @property
    def check_active(self):
        return self.is_active

    @property
    def check_locked(self):
        return self.is_locked

    def get_engine_instance(self):
        return self.engine_id

    objects = UserManager()


# Set of Roles defined for each Module. Roles can be System or User defined. System Defined roles cannot be added or modified from UI.
# User defined roles can be added by the module admin only and can be mapped to an existing system role only.
class AdbizRoles(models.Model):

    class Meta:
        db_table = 'roles'

    role_name = models.CharField(max_length=64, verbose_name="Role Name")
    role_description = models.CharField(max_length=256, verbose_name="Role Description")
    module = models.CharField(max_length=32, verbose_name="Module")
    role_reference_id = models.PositiveSmallIntegerField()
    is_system = models.BooleanField(default=False, verbose_name="Is System?")
    is_active = models.BooleanField(default=True,  verbose_name="Is Active?")


class AdbizPrivileges(models.Model):

    class Meta:
        db_table = "privileges"

    privilege_name = models.CharField(max_length=64, verbose_name="Privilege Name")
    privilege_description = models.CharField(max_length=256, verbose_name="Privilege Description")
    module = models.CharField(max_length=32, verbose_name="Module")
    is_create = models.BooleanField(default=False, verbose_name="Create?")
    is_read = models.BooleanField(default=True, verbose_name="Read?")
    is_update = models.BooleanField(default=False, verbose_name="Update?")
    is_delete = models.BooleanField(default=False, verbose_name="Delete?")
    is_execute = models.BooleanField(default=False, verbose_name="Execute?")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")


class AdbizMenuItems(models.Model):

    class Meta:
        db_table = "menu_items"

    menu_name = models.CharField(max_length=64, verbose_name="Menu Name")
    menu_description = models.CharField(max_length=256, verbose_name="Menu Description")
    module = models.CharField(max_length=32, verbose_name="Module")
    role = models.ForeignKey(AdbizRoles, on_delete=models.CASCADE, verbose_name="Roles")
    menu_tooltip = models.CharField(max_length=256, verbose_name="Tooltip")
    menu_url = models.CharField(max_length=256, verbose_name="URL")
    parent_menu_id = models.PositiveSmallIntegerField(null=True, blank=True)
    display_seq = models.PositiveSmallIntegerField()
    privilege = models.ForeignKey(AdbizPrivileges, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")


class AdbizPreferences(models.Model):

    class Meta:
        db_table = "preferences"

    preference_name = models.CharField(max_length=64, verbose_name="Preference Name")
    preference_description = models.CharField(max_length=256, verbose_name="Preference Description")
    module = models.CharField(max_length=32, verbose_name="Module")
    default_value = models.CharField(max_length=32, verbose_name="Default Value")


class UserPreferences(models.Model):

    class Meta:
        db_table = "user_preferences"

    module = models.CharField(max_length=32, verbose_name="Module")
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    preference = models.ForeignKey(AdbizPreferences, on_delete=models.CASCADE)
    preference_value = models.CharField(max_length=256)
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created on")
    last_updated_on = models.DateTimeField(default=timezone.now, verbose_name="Last updated on")
    last_updated_by = models.CharField(max_length=64, verbose_name="Last updated By")


# Maps Users with predefined Roles (one or many) for each Module (one or many)
# Final Permission set for a user is a superset of all the privileges
class UserAccess(models.Model):

    class Meta:
        db_table = "user_access"

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    module = models.CharField(max_length=32, verbose_name="Module")
    role = models.ForeignKey(AdbizRoles, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created on")
    last_updated_on = models.DateTimeField(default=timezone.now, verbose_name="Last updated on")
    last_updated_by = models.CharField(max_length=64, verbose_name="Last updated By")


