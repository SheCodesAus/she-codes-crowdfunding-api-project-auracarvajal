# Generated by Django 4.1.5 on 2023-01-21 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='goal',
            field=models.FloatField(),
        ),
    ]
