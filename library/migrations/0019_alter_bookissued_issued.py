# Generated by Django 4.1.7 on 2023-08-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_alter_bookissued_issued'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissued',
            name='Issued',
            field=models.CharField(default='No', max_length=10),
        ),
    ]