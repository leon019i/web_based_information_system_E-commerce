# Generated by Django 4.0.3 on 2022-05-06 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_is_suspended'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_suspended',
            new_name='is_activated_via_email',
        ),
    ]