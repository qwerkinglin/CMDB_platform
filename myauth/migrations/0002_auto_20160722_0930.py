# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bind_hosts',
            field=models.ManyToManyField(to='hosts.BindHostToUser', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='host_groups',
            field=models.ManyToManyField(to='hosts.HostGroup', blank=True),
        ),
    ]
