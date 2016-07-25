# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_auto_20160722_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostuser',
            name='memo',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
