# Generated by Django 5.1.4 on 2025-01-03 16:13

import util.model_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0005_sitesetup_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, default='', upload_to='assets/favicon', validators=[util.model_validators.validate_image]),
        ),
    ]