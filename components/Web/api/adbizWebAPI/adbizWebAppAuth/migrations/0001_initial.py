# Generated by Django 3.0.5 on 2020-04-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('siteCode', models.CharField(max_length=10)),
                ('siteName', models.CharField(max_length=128)),
                ('createDateTime', models.DateTimeField()),
                ('createdBy', models.CharField(max_length=128)),
            ],
        ),
    ]
