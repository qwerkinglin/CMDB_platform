#_*_coding:utf-8_*_
from django.db import models
# Create your models here.

class ProjectList(models.Model):
    developer = models.CharField(u'开发者',max_length=128,default='unknow')
    jetty_name = models.CharField(u'jetty实例名',max_length=128)
    jetty_root = models.CharField(u'jetty根目录名',max_length=128)
    jetty_port = models.IntegerField(u'jetty端口')
    lb_server = models.ForeignKey('hosts.HostGroup')
    db = models.ForeignKey('DatabaseList')
    db_name = models.CharField(u'数据库名',max_length=128,default='None')
    db_user = models.CharField(u'数据库账户',max_length=128,default='None')
    db_pd = models.CharField(u'数据库密码',max_length=128,default='None')
    memcached = models.ForeignKey('MemList')
    mem_port = models.IntegerField(u'缓存端口',default=0)
    project_path = models.CharField(u'jetty路径',max_length=256)
    conf_path = models.CharField(u'配置文件路径',max_length=512,blank=True,null=True)
    project_group = models.ForeignKey('ProjectGroup')
    online_state = models.BooleanField(u'启用',default=True)
    create_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    memo = models.TextField(u'备注',blank=True,null=True)

    def __unicode__(self):
        return "%s(%s,%s)" %(self.developer,self.jetty_name,self.jetty_root)

    class Meta:
        unique_together = ('jetty_name','jetty_root')
        verbose_name = u'Jetty项目列表'
        verbose_name_plural = u"Jetty项目列表"

class ProjectGroup(models.Model):
    name = models.CharField(max_length=128)
    cycle = models.CharField(u'上线周期(单位:周)',max_length=128,null=True,blank=True)
    start_time = models.TimeField(u'开始时间',null=True,blank=True)
    end_time = models.TimeField(u'结束时间',null=True,blank=True)
    pm = models.CharField(u'产品经理',max_length=64,null=True,blank=True)
    om = models.CharField(u'运营经理',max_length=64,null=True,blank=True)
    url = models.CharField(u'访问地址',max_length=128,null=True,blank=True)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s(%s,%s)" %(self.name,self.pm,self.om)

    class Meta:
        verbose_name = u'Jetty项目组列表'
        verbose_name_plural = u"Jetty项目组列表"

class DatabaseList(models.Model):
    instance_name = models.CharField(max_length=64,blank=True,null=True)
    alias_name = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=3306)
    user = models.CharField(max_length=64,default='root')
    passwd = models.CharField(max_length=128)
    url = models.CharField(max_length=128,blank=True,null=True)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s" %(self.alias_name)

    class Meta:
        verbose_name = u'MySQL实例列表'
        verbose_name_plural = u"MySQL实例列表"

class MemList(models.Model):
    instance_name = models.CharField(max_length=64,blank=True,null=True)
    alias_name = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(unique=True)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s" %(self.alias_name)

    class Meta:
        verbose_name = u'Memcached实例列表'
        verbose_name_plural = u"Memcached实例列表"
