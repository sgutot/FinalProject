# Generated by Django 5.1.6 on 2025-04-05 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_pet_owner_alter_productrequest_descrption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrequest',
            name='requestDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
