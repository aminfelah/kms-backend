# Generated by Django 3.1.7 on 2021-06-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_cmd', models.IntegerField()),
                ('num_lots', models.IntegerField()),
                ('dateHeure_debut', models.DateTimeField()),
                ('dateHeure_Fin', models.DateTimeField()),
            ],
        ),
    ]