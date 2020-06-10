# Generated by Django 3.0.5 on 2020-06-04 17:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoreEngine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('core_engine_code', models.CharField(max_length=255, unique=True, verbose_name='Core Engine Code (generated)')),
                ('product_engine_code', models.CharField(max_length=255, verbose_name='Product Engine Code')),
                ('activation_file_location', models.CharField(max_length=255, verbose_name='Activation File Location')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name=' Activation Key (generated)')),
                ('activation_dt', models.DateTimeField(verbose_name='Activation Date Time')),
                ('host_name', models.CharField(max_length=128, verbose_name='Host Name')),
                ('host_ip_address', models.GenericIPAddressField(verbose_name='Host IP Address')),
                ('os_release', models.CharField(max_length=32, null=True, verbose_name='OS Release Version')),
                ('release_info', models.CharField(max_length=255, null=True, verbose_name='Version Details')),
                ('validity_start_date', models.DateTimeField(null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(null=True, verbose_name='Validity End Date')),
                ('product_engine_details', models.TextField(editable=False, null=True, verbose_name='Product Engine Details')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Activated ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
            ],
            options={
                'db_table': 'engine_metadata',
            },
        ),
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_code', models.CharField(editable=False, max_length=255, unique=True, verbose_name='Environment/Instance Code (generated)')),
                ('environment_type', models.CharField(choices=[('DEV', 'Development'), ('QA', 'QA or SIT'), ('UAT', 'UAT'), ('PROD', 'Production')], default='DEV', max_length=32, null=True, verbose_name='Environment Type')),
                ('environment_description', models.TextField(max_length=255, null=True)),
                ('activation_file_location', models.CharField(max_length=255, verbose_name='Activation File Location')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name=' Activation Key (generated)')),
                ('activation_dt', models.DateTimeField(verbose_name='Activation Date Time')),
                ('host_name', models.CharField(max_length=128, verbose_name='Host Name')),
                ('host_ip_address', models.GenericIPAddressField(verbose_name='Host IP Address')),
                ('os_release', models.CharField(max_length=32, null=True, verbose_name='OS Release Version')),
                ('release_info', models.CharField(max_length=255, null=True, verbose_name='Version Details')),
                ('validity_start_date', models.DateTimeField(null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(null=True, verbose_name='Validity End Date')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Activated ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
            ],
            options={
                'db_table': 'instances',
            },
        ),
        migrations.CreateModel(
            name='Tenants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_engine_code', models.CharField(editable=False, max_length=255, verbose_name='Product Engine Code')),
                ('tenant_name', models.CharField(max_length=128, verbose_name='Tenant Name')),
                ('tenant_code', models.CharField(editable=False, max_length=255, unique=True, verbose_name='Tenant Code (generated)')),
                ('tenant_namespace', models.CharField(max_length=6, verbose_name='Tenant Namespace')),
                ('registration_number', models.CharField(max_length=32, unique=True, verbose_name='Unique Registration Number (any)')),
                ('registration_dt', models.DateTimeField(verbose_name='Registration Date')),
                ('company_category', models.CharField(max_length=32, null=True, verbose_name='Company Category')),
                ('company_sub_category', models.CharField(max_length=32, null=True, verbose_name='Company Sub Category')),
                ('company_class', models.CharField(max_length=32, null=True, verbose_name='Company Class')),
                ('company_type', models.CharField(max_length=32, null=True, verbose_name='Company Type')),
                ('city', models.CharField(max_length=32, null=True, verbose_name='City')),
                ('state', models.CharField(max_length=3, null=True, verbose_name='State')),
                ('country', models.CharField(max_length=3, verbose_name='Country')),
                ('website_url', models.URLField(max_length=128, null=True, verbose_name='URL')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
            ],
            options={
                'db_table': 'tenants',
            },
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_code', models.CharField(editable=False, max_length=255, unique=True, verbose_name='Site ID (generated)')),
                ('site_name', models.CharField(max_length=128, verbose_name='Site Name')),
                ('site_description', models.TextField(max_length=255, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'sites',
            },
        ),
        migrations.CreateModel(
            name='ProcessingEngines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processing_engine_type', models.CharField(choices=[('PE', 'ProductEngine'), ('CE', 'CoreEngine'), ('EE', 'ETLEngine'), ('IO', 'IOEngine'), ('UI', 'WEB UI ENGINE')], max_length=32, null=True, verbose_name='Processing Engine')),
                ('processing_engine_code', models.CharField(editable=False, max_length=255, unique=True, verbose_name='Processing Engine Code (generated)')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name=' Activation Key (generated)')),
                ('engine_properties', models.TextField(null=True, verbose_name='Engine Properties')),
                ('activation_dt', models.DateTimeField(editable=False, null=True, verbose_name='Activation Date Time')),
                ('validity_start_date', models.DateTimeField(null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(null=True, verbose_name='Validity End Date')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Activated ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Instances', verbose_name='Instance')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'processing_engines',
            },
        ),
        migrations.CreateModel(
            name='ProcessingEngineActivations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name='Activation Key')),
                ('validity_start_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity End Date')),
                ('activation_dt', models.DateTimeField(editable=False)),
                ('deactivation_dt', models.DateTimeField(editable=False, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Instances', verbose_name='Instance')),
                ('processing_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.ProcessingEngines', verbose_name='Processing Engine')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'processing_engine_activations',
            },
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(choices=[('ACTPBL', 'ACCOUNT PAYABLES'), ('ACTRBL', 'ACCOUNT RECEIVABLES'), ('BANK_RECO', 'BANK_RECONCILIATIONS')], max_length=255, verbose_name='Modules')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name=' Activation Key (generated)')),
                ('activation_dt', models.DateTimeField(editable=False, null=True, verbose_name='Module Activation Date Time')),
                ('validity_start_date', models.DateTimeField(null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(null=True, verbose_name='Validity End Date')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Activated ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Instances', verbose_name='Instance')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'modules',
            },
        ),
        migrations.CreateModel(
            name='ModuleActivations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name='Activation Key')),
                ('validity_start_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity End Date')),
                ('activation_dt', models.DateTimeField(editable=False)),
                ('deactivation_dt', models.DateTimeField(editable=False, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Instances', verbose_name='Instance')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'module_activations',
            },
        ),
        migrations.CreateModel(
            name='LicensingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_type', models.CharField(choices=[('SUBCRPTN', 'Subscription Based'), ('PRPTL', 'Perpetual'), ('EVAL', 'Evaluation')], default='SUBCRPTN', max_length=32)),
                ('duration_days', models.PositiveIntegerField(default=0, verbose_name='Validity (days)')),
                ('active_modules', models.CharField(choices=[('ACTPBL', 'ACCOUNT PAYABLES'), ('ACTRBL', 'ACCOUNT RECEIVABLES'), ('BANK_RECO', 'BANK_RECONCILIATIONS')], max_length=255, verbose_name='Modules')),
                ('active_engines', models.CharField(choices=[('PE', 'ProductEngine'), ('CE', 'CoreEngine'), ('EE', 'ETLEngine'), ('IO', 'IOEngine'), ('UI', 'WEB UI ENGINE')], max_length=255, verbose_name='Engines')),
                ('active_envs', models.CharField(choices=[('DEV', 'Development'), ('QA', 'QA or SIT'), ('UAT', 'UAT'), ('PROD', 'Production')], max_length=255, verbose_name='Instances')),
                ('active_from_dt', models.DateTimeField(verbose_name='Active since')),
                ('active_end_dt', models.DateTimeField(null=True, verbose_name='Active till')),
                ('activated_on_dt', models.DateTimeField(verbose_name='Activated On')),
                ('deactivated_on_dt', models.DateTimeField(verbose_name='Deactivated On')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Activated ?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants')),
            ],
            options={
                'db_table': 'license_info',
            },
        ),
        migrations.AddField(
            model_name='instances',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site'),
        ),
        migrations.AddField(
            model_name='instances',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant'),
        ),
        migrations.CreateModel(
            name='InstanceActivations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name='Activation Key')),
                ('validity_start_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity End Date')),
                ('activation_dt', models.DateTimeField(editable=False)),
                ('deactivation_dt', models.DateTimeField(editable=False, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Instances', verbose_name='Instance')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'instance_activations',
            },
        ),
        migrations.CreateModel(
            name='DataLakes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=32, verbose_name='Module')),
                ('storage_engine_class', models.CharField(max_length=32, verbose_name='Storage Engine Class')),
                ('data_lake_type', models.CharField(choices=[('RDBMS', 'ANY RDBMS ENGINE'), ('BD', 'ANY BIG DATA STORAGES LIKE HIVE OR HBASE'), ('NS', 'ANY NOSQL DATABASES'), ('CL', 'CLOUD DATABASES')], max_length=255, verbose_name='Data Lake Type')),
                ('data_lake_sub_type', models.CharField(choices=[('ORCL', 'RDBMS - ORACLE DATABASE'), ('MYSQL', 'RDBMS - MYSQL DATABASE'), ('PGRES', 'RDBMS - POSTGRES DATABASE'), ('HV', 'BD - HIVE DATABASE'), ('PQ', 'BD - PARQUET FILES')], max_length=255, verbose_name='Data Lake Sub Type')),
                ('data_lake_code', models.CharField(editable=False, max_length=255, verbose_name='Data Lake Code')),
                ('data_lake_description', models.TextField(null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('is_primary', models.BooleanField(default=True, verbose_name='Is Primary Storage?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Instances', verbose_name='Environment/Instance')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Sites', verbose_name='Site')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'data_lakes',
            },
        ),
        migrations.CreateModel(
            name='CoreEngineActivations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_engine_code', models.CharField(editable=False, max_length=255, verbose_name='Product Engine Code')),
                ('activation_file_location', models.CharField(max_length=255, verbose_name='Activation File Location')),
                ('activation_key', models.CharField(editable=False, max_length=255, verbose_name='Activation Key')),
                ('validity_start_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity Start Date')),
                ('validity_end_date', models.DateTimeField(editable=False, null=True, verbose_name='Validity End Date')),
                ('activation_dt', models.DateTimeField(editable=False, verbose_name='Activation Date Time')),
                ('deactivation_dt', models.DateTimeField(editable=False, null=True, verbose_name='Deactivation Date Time')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=64, verbose_name='Last Updated By')),
                ('core_engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.CoreEngine', verbose_name='Core Engine')),
                ('tenant', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant')),
            ],
            options={
                'db_table': 'engine_activations',
            },
        ),
        migrations.AddField(
            model_name='coreengine',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adbizCoreEngine.Tenants', verbose_name='Tenant'),
        ),
    ]
