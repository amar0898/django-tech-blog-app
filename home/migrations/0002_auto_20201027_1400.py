# Generated by Django 3.1.1 on 2020-10-27 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='content',
            new_name='message',
        ),
    ]
