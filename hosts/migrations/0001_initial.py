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
                'verbose_name': '\u7ec4\u4e0e\u4e3b\u673a\u7ed1\u5b9a',
                'verbose_name_plural': '\u7ec4\u4e0e\u4e3b\u673a\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='BindHostToUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4e0e\u4e3b\u673a\u7ed1\u5b9a',
                'verbose_name_plural': '\u7528\u6237\u4e0e\u4e3b\u673a\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=128)),
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
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('task_type', models.CharField(max_length=50, choices=[(b'multi_cmd', b'CMD'), (b'file_send', b'\xe6\x89\xb9\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe6\x89\xb9\xe9\x87\x8f\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')])),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('hosts', models.ManyToManyField(to='hosts.BindHostToUser')),
            ],
            options={
                'verbose_name': '\u6279\u91cf\u4efb\u52a1',
                'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1',
            },
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(default=b'unknown', max_length=30, choices=[(b'success', b'Success'), (b'failed', b'Failed'), (b'unknown', b'Unknown')])),
                ('note', models.CharField(max_length=100, blank=True)),
                ('bind_host', models.ForeignKey(to='hosts.BindHostToUser')),
                ('child_of_task', models.ForeignKey(to='hosts.TaskLog')),
            ],
            options={
                'verbose_name': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
                'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
            },
        ),
    ]
