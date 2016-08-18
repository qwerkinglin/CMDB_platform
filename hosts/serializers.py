#_*_coding:utf-8_*_

import models
from rest_framework import serializers

class HostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        depth = 2
        fields = '__all__'
        #fields = ('hostname','wan_ip','lan_ip','domain','os_version')

