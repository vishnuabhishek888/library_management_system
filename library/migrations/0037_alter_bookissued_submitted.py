# Generated by Django 4.1.7 on 2023-08-28 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0036_bookissued_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissued',
            name='Submitted',
            field=models.CharField(default='No', max_length=5),
        ),
    ]
