# Generated by Django 3.1.7 on 2021-06-06 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kms', '0014_risque'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclamations',
            name='detector',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
