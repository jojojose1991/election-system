# Generated by Django 3.2.15 on 2022-10-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electoral', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='logo',
            field=models.ImageField(upload_to=''),
        ),
    ]