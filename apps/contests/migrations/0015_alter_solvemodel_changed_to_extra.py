# Generated by Django 4.2.6 on 2023-10-23 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0014_solvemodel_changed_to_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvemodel',
            name='changed_to_extra',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
