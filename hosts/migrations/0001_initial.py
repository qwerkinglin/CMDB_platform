# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BindHostToUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
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
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_type', models.CharField(default=b'ssh-password', max_length=32, choices=[(b'ssh-password', b'SSH/PASSWORD'), (b'ssh-key', b'SSH/KEY')])),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=128, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.TextField(null=True, blank=True)),
            ],
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
            model_name='bindhosttouser',
            name='host',
            field=models.ForeignKey(to='hosts.Host'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_groups',
            field=models.ManyToManyField(to='hosts.HostGroup'),
        ),
        migrations.AddField(
            model_name='bindhosttouser',
            name='host_user',
            field=models.ForeignKey(to='hosts.HostUser'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosttouser',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
