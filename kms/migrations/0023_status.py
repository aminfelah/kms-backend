# Generated by Django 3.1.7 on 2021-06-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kms', '0022_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200)),
            ],
        ),
    ]