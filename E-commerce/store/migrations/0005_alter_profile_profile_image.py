# Generated by Django 4.0.3 on 2022-05-28 14:12

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='/static/upload/default_profile_pic.png', upload_to=store.models.get_file_path),
        ),
    ]
