# Generated by Django 3.0.5 on 2020-06-13 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_account', models.CharField(max_length=255, unique=True, verbose_name='User Account (generated)')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=64, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, null=True, verbose_name='Last Name')),
                ('dob', models.DateField(null=True, verbose_name='Date of birth')),
                ('joined_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_super_user', models.BooleanField(default=False)),
                ('is_system_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('login_attempts', models.SmallIntegerField(default=0)),
                ('last_login_dt', models.DateTimeField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last updated on')),
                ('last_updated_by', models.CharField(max_length=64, verbose_name='Last updated By')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='AdbizPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_name', models.CharField(max_length=64, verbose_name='Preference Name')),
                ('preference_description', models.CharField(max_length=256, verbose_name='Preference Description')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('default_value', models.CharField(max_length=32, verbose_name='Default Value')),
            ],
            options={
                'db_table': 'preferences',
            },
        ),
        migrations.CreateModel(
            name='AdbizPrivileges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege_name', models.CharField(max_length=64, verbose_name='Privilege Name')),
                ('privilege_description', models.CharField(max_length=256, verbose_name='Privilege Description')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('is_create', models.BooleanField(default=False, verbose_name='Create?')),
                ('is_read', models.BooleanField(default=True, verbose_name='Read?')),
                ('is_update', models.BooleanField(default=False, verbose_name='Update?')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Delete?')),
                ('is_execute', models.BooleanField(default=False, verbose_name='Execute?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
            ],
            options={
                'db_table': 'privileges',
            },
        ),
        migrations.CreateModel(
            name='AdbizRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=64, verbose_name='Role Name')),
                ('role_description', models.CharField(max_length=256, verbose_name='Role Description')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('role_reference_id', models.PositiveSmallIntegerField()),
                ('is_system', models.BooleanField(default=False, verbose_name='Is System?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='AdbizUIEngine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ui_engine_code', models.CharField(max_length=255, unique=True, verbose_name='UI Engine Code (generated)')),
                ('core_engine_code', models.CharField(editable=False, max_length=255, verbose_name='Core Engine Code')),
                ('tenant_code', models.CharField(max_length=255, verbose_name='Tenant')),
                ('site_code', models.CharField(editable=False, max_length=255, verbose_name='Site')),
                ('instance_code', models.CharField(editable=False, max_length=255, verbose_name='Environment/Instance')),
                ('activation_file_location', models.CharField(max_length=255, verbose_name='Activation File Location')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name=' Activation Key (generated)')),
                ('activation_dt', models.DateTimeField(verbose_name='Activation Date Time')),
                ('host_name', models.CharField(max_length=128, verbose_name='Host Name')),
                ('host_ip_address', models.GenericIPAddressField(verbose_name='Host IP Address')),
                ('os_release', models.CharField(max_length=32, null=True, verbose_name='OS Release Version')),
                ('release_info', models.CharField(max_length=255, null=True, verbose_name='Version Details')),
                ('validity_start_date', models.DateTimeField(null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(null=True, verbose_name='Validity End Date')),
                ('engine_properties', models.TextField(null=True, verbose_name='Engine Details')),
                ('core_engine_details', models.TextField(null=True, verbose_name='Core Engine Details')),
                ('catalog_engine_details', models.TextField(null=True, verbose_name='Catalog Engine Details')),
                ('io_engine_details', models.TextField(null=True, verbose_name='IO Engine Details')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Activated ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=32, verbose_name='Last Updated By')),
            ],
            options={
                'db_table': 'engine_metadata',
            },
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('preference_value', models.CharField(max_length=256)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last updated on')),
                ('last_updated_by', models.CharField(max_length=64, verbose_name='Last updated By')),
                ('preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizPreferences')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_preferences',
            },
        ),
        migrations.CreateModel(
            name='UserAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last updated on')),
                ('last_updated_by', models.CharField(max_length=64, verbose_name='Last updated By')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizRoles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_access',
            },
        ),
        migrations.CreateModel(
            name='AdbizUIEngineActivations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('core_engine_code', models.CharField(editable=False, max_length=64, verbose_name='Core Engine ID')),
                ('activation_key', models.CharField(editable=False, max_length=64, verbose_name='Activation Key')),
                ('validity_start_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity End Date')),
                ('activation_dt', models.DateTimeField(editable=False, verbose_name='Activation Date Time')),
                ('deactivation_dt', models.DateTimeField(editable=False, null=True, verbose_name='Deactivation Date Time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=32, verbose_name='Last Updated By')),
                ('ui_engine_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizUIEngine', verbose_name='UI Engine ID (generated)')),
            ],
            options={
                'db_table': 'engine_activations',
            },
        ),
        migrations.CreateModel(
            name='AdbizModuleActivations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(editable=False, max_length=32)),
                ('activation_key', models.CharField(editable=False, max_length=64, verbose_name='Activation Key')),
                ('validity_start_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity End Date')),
                ('activation_dt', models.DateTimeField(editable=False, verbose_name='Activation Date Time')),
                ('deactivation_dt', models.DateTimeField(editable=False, null=True, verbose_name='Deactivation Date Time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=32, verbose_name='Last Updated By')),
                ('ui_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizUIEngine', verbose_name='UI Engine ID (generated)')),
            ],
            options={
                'db_table': 'module_activations',
            },
        ),
        migrations.CreateModel(
            name='AdbizMenuItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=64, verbose_name='Menu Name')),
                ('menu_description', models.CharField(max_length=256, verbose_name='Menu Description')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('menu_tooltip', models.CharField(max_length=256, verbose_name='Tooltip')),
                ('menu_url', models.CharField(max_length=256, verbose_name='URL')),
                ('parent_menu_id', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('display_seq', models.PositiveSmallIntegerField()),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
                ('privilege', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizPrivileges')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizRoles', verbose_name='Roles')),
            ],
            options={
                'db_table': 'menu_items',
            },
        ),
        migrations.AddField(
            model_name='users',
            name='engine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizUIEngine', verbose_name='UI Engine ID (generated)'),
        ),
    ]
