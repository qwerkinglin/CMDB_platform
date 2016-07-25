#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
class Host(models.Model):
    hostname = models.CharField(max_length=64)
    wan_ip = models.GenericIPAddressField(unique=True)
    lan_ip = models.GenericIPAddressField(unique=True)
    domain = models.CharField(max_length=128)
    cpu = models.CharField(max_length=16)
    memory = models.CharField(max_length=16)
    disk = models.CharField(max_length=16)
    out_bandwidth = models.CharField(max_length=16)
    os_version = models.CharField(max_length=64)
    port = models.IntegerField(default=38096)
    idc = models.ForeignKey('IDC')
    enabled = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s(%s,%s)" %(self.hostname,self.lan_ip,self.wan_ip)

    class Meta:
        verbose_name = u'主机列表'
        verbose_name_plural = u"主机列表"

class IDC(models.Model):
    name = models.CharField(unique=True,max_length=64)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'IDC'
        verbose_name_plural = u"IDC"

class HostUser(models.Model):
    auth_type_choices = (
        ('ssh-password', 'SSH/PASSWORD'),
        ('ssh-key', 'SSH/KEY'),
    )
    auth_type = models.CharField(choices=auth_type_choices,max_length=32,default='ssh-password')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128,blank=True,null=True)
    memo = models.CharField(max_length=256,blank=True,null=True)

    def __unicode__(self):
        return "(%s)%s %s" %(self.memo,self.username,self.auth_type)

    class Meta:
        unique_together = ('auth_type','username','password')
        verbose_name = u'主机用户'
        verbose_name_plural = u"主机用户"

class HostGroup(models.Model):
    name = models.CharField(unique=True,max_length=64)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = u"主机组"

class BindHostToUser(models.Model):
    host = models.ForeignKey("Host")
    host_user = models.ForeignKey("HostUser")
    #host_user = models.ManyToManyField("HostUser")

    class Meta:
        unique_together = ('host','host_user')
        verbose_name = u'主机与用户绑定'
        verbose_name_plural = u"主机与用户绑定"

    def __unicode__(self):
        return "%s:%s" %(self.host.hostname, self.host_user.username)

class BindHostToGroup(models.Model):
    host_group = models.ForeignKey("HostGroup")
    bind_hosts = models.ManyToManyField("BindHostToUser")

    class Meta:
        verbose_name = u'主机与组绑定'
        verbose_name_plural = u"主机与组绑定"

    def __unicode__(self):
        return "%s" %(self.host_group.name,)

    def get_hosts(self):
        #return '_'.join([g.host.hostname+":"+g.host_user.username for g in self.bind_hosts.select_related()])
        return '_'.join([g.host.hostname for g in self.bind_hosts.select_related()])

