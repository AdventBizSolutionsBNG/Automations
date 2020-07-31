# Generated by Django 3.0.5 on 2020-06-27 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adbizWebUIEngine', '0013_auto_20200617_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdbizUserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=32, null=True, verbose_name='Module')),
                ('preference_value', models.CharField(max_length=256)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('last_updated_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last updated on')),
                ('last_updated_by', models.CharField(max_length=64, verbose_name='Last updated By')),
            ],
            options={
                'db_table': 'user_preferences',
            },
        ),
        migrations.RenameModel(
            old_name='UserAccess',
            new_name='AdbizUserAccess',
        ),
        migrations.RemoveField(
            model_name='adbizuser',
            name='is_systemuser',
        ),
        migrations.AddField(
            model_name='adbizpreferences',
            name='preference_code',
            field=models.CharField(max_length=32, null=True, unique=True, verbose_name='Preference Code'),
        ),
        migrations.AddField(
            model_name='adbizuiengine',
            name='catalog_details',
            field=models.TextField(null=True, verbose_name='Catalog Details'),
        ),
        migrations.AddField(
            model_name='adbizuiengine',
            name='datamodel_details',
            field=models.TextField(null=True, verbose_name='Datamodel Details'),
        ),
        migrations.AddField(
            model_name='adbizuser',
            name='is_super_user',
            field=models.BooleanField(default=False, verbose_name='Super User?'),
        ),
        migrations.AddField(
            model_name='adbizuser',
            name='is_system_user',
            field=models.BooleanField(default=False, verbose_name='System User?'),
        ),
        migrations.AlterField(
            model_name='adbizpreferences',
            name='module',
            field=models.CharField(max_length=32, null=True, verbose_name='Module'),
        ),
        migrations.AlterField(
            model_name='adbizuser',
            name='email',
            field=models.EmailField(max_length=64, unique=True, verbose_name='Login (email)'),
        ),
        migrations.AlterField(
            model_name='adbizuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active?'),
        ),
        migrations.AlterField(
            model_name='adbizuser',
            name='is_locked',
            field=models.BooleanField(default=False, verbose_name='Locked?'),
        ),
        migrations.AlterField(
            model_name='adbizuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='App Admin User?'),
        ),
        migrations.AlterField(
            model_name='adbizuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.DeleteModel(
            name='UserPreferences',
        ),
        migrations.AddField(
            model_name='adbizuserpreferences',
            name='preference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adbizWebUIEngine.AdbizPreferences'),
        ),
        migrations.AddField(
            model_name='adbizuserpreferences',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
