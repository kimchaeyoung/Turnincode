# Generated by Django 2.2.3 on 2019-10-09 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turninApp', '0003_remove_homework_duedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='hw_duedate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
