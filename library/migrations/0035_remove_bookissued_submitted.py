# Generated by Django 4.1.7 on 2023-08-25 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0034_bookissued_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookissued',
            name='Submitted',
        ),
    ]
