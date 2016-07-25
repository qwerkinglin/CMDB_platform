# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bindhosttouser',
            options={'verbose_name': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a', 'verbose_name_plural': '\u4e3b\u673a\u4e0e\u6237\u7ed1\u5b9a'},
        ),
        migrations.AlterModelOptions(
            name='host',
            options={'verbose_name': '\u4e3b\u673a\u5217\u8868', 'verbose_name_plural': '\u4e3b\u673a\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='hostgroup',
            options={'verbose_name': '\u4e3b\u673a\u7ec4', 'verbose_name_plural': '\u4e3b\u673a\u7ec4'},
        ),
        migrations.AlterModelOptions(
            name='hostuser',
            options={'verbose_name': '\u4e3b\u673a\u7528\u6237', 'verbose_name_plural': '\u4e3b\u673a\u7528\u6237'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'verbose_name': 'IDC', 'verbose_name_plural': 'IDC'},
        ),
        migrations.AddField(
            model_name='hostuser',
            name='memo',
            field=models.TextField(null=True, blank=True),
        ),
    ]
