# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BindHostToGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4e0e\u7ec4\u7ed1\u5b9a',
                'verbose_name_plural': '\u4e3b\u673a\u4e0e\u7ec4\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=64)),
                ('wan_ip', models.GenericIPAddressField(unique=True)),
                ('lan_ip', models.GenericIPAddressField(unique=True)),
                ('domain', models.CharField(max_length=128)),
                ('cpu', models.CharField(max_length=16)),
                ('memory', models.CharField(max_length=16)),
                ('disk', models.CharField(max_length=16)),
                ('out_bandwidth', models.CharField(max_length=16)),
                ('os_version', models.CharField(max_length=64)),
                ('port', models.IntegerField(default=38096)),
                ('enabled', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('memo', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u5217\u8868',
                'verbose_name_plural': '\u4e3b\u673a\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7ec4',
                'verbose_name_plural': '\u4e3b\u673a\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_type', models.CharField(default=b'ssh-password', max_length=32, choices=[(b'ssh-password', b'SSH/PASSWORD'), (b'ssh-key', b'SSH/KEY')])),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=128, null=True, blank=True)),
                ('memo', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7528\u6237',
                'verbose_name_plural': '\u4e3b\u673a\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'IDC',
                'verbose_name_plural': 'IDC',
            },
        ),
        migrations.AlterUniqueTogether(
            name='hostuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(to='hosts.IDC'),
        ),
        migrations.AddField(
            model_name='bindhosttogroup',
            name='bind_hosts',
            field=models.ManyToManyField(to='hosts.Host'),
        ),
        migrations.AddField(
            model_name='bindhosttogroup',
            name='host_group',
            field=models.ForeignKey(to='hosts.HostGroup'),
        ),
    ]
