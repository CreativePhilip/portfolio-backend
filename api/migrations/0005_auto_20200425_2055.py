# Generated by Django 3.0.5 on 2020-04-25 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200425_1751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='description',
            new_name='text',
        ),
    ]
