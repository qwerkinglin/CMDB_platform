#_*_coding:utf-8_*_
from django.db import models
# Create your models here.

class ProjectList(models.Model):
    developer = models.CharField(u'开发者',max_length=128,default='unknow')
    role = models.CharField(u'角色',max_length=128,default='unknow')
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
    name = models.CharField(u'组名',max_length=128,unique=True)
    cycle = models.CharField(u'播出时间',max_length=128,null=True,blank=True)
    start_time = models.DateTimeField(u'上线时间',null=True,blank=True)
    end_time = models.DateTimeField(u'下线时间',null=True,blank=True)
    pm = models.CharField(u'产品经理',max_length=64,null=True,blank=True)
    om = models.CharField(u'运营经理',max_length=64,null=True,blank=True)
    url = models.CharField(u'访问地址',max_length=128,null=True,blank=True)
    enabled = models.BooleanField(u'启用',default=True)
    memo = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s" %(self.name)

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

class ProjectTaskLog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)
    task_type_choices = (('update','更新项目'),('check','检测项目'),)
    task_type = models.CharField(choices=task_type_choices,max_length=50)
    user = models.ForeignKey('myauth.UserProfile')
    hosts = models.ManyToManyField('hosts.BindHostToUser')
    expire_time = models.IntegerField(default=30)
    task_pid = models.IntegerField(default=0)
    note = models.CharField(max_length=100,blank=True,null=True)
    belong_to_project = models.ForeignKey('ProjectList')

    def __unicode__(self):
        return "taskid:%s cmd:%s" %(self.id,self.task_type)

    class Meta:
        verbose_name = u'项目任务日志'
        verbose_name_plural = u'项目任务日志'

class ProjectTaskLogDetail(models.Model):
    child_of_task = models.ForeignKey('ProjectTaskLog')
    bind_host = models.ForeignKey('hosts.BindHostToUser')
    date = models.DateTimeField(auto_now_add=True) #finished date
    event_log = models.TextField()
    result_choices = (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices,max_length=30,default='unknown')
    note = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return "child of:%s bindhost:%s result:%s" %(self.child_of_task.id,self.bind_host,self.result)

    class Meta:
        verbose_name = u'项目任务日志详情'
        verbose_name_plural = u'项目任务日志详情'