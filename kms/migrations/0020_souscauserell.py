# Generated by Django 3.1.7 on 2021-06-10 18:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kms', '0019_consrell'),
    ]

    operations = [
        migrations.CreateModel(
            name='SousCauseRell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptionSous_Causes', models.CharField(max_length=200)),
                ('dateHeure_detection', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Dates création')),
            ],
        ),
    ]
