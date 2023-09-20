# Generated by Django 4.1.7 on 2023-08-14 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0005_rename_roll_no_bookissued_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookIssuedRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_issued_request', to='library.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_issued_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
