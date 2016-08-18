#_*_coding:utf-8_*_

from rest_framework import viewsets
from serializers import HostsSerializer
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
import models
from django.contrib.auth.models import Permission

class HostsViewSet(viewsets.ModelViewSet):
    queryset = models.Host.objects.all()
    serializer_class = HostsSerializer