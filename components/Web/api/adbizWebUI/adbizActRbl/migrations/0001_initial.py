# Generated by Django 3.0.5 on 2020-06-27 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_key', models.CharField(max_length=32, unique=True, verbose_name='Config Key')),
                ('config_value', models.TextField(verbose_name='Config Value')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active ?')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created On')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Updated On')),
                ('last_updated_by', models.CharField(editable=False, max_length=32, verbose_name='Last Updated By')),
            ],
            options={
                'db_table': 'module_settings',
            },
        ),
    ]
