#_*_coding:utf-8_*_
__author__ = 'Alex hao'

import json,models
from django.core.exceptions import ObjectDoesNotExist

class Asset(object):
    def __init__(self,request):
        self.request = request
        self.mandatory_fields = ['sn','asset_id','asset_type']  #强制检测传过来必须有的字段
        self.response = {
            'error':[],
            'info':[],
            'warning':[]
        }

    def response_msg(self,msg_type,key,msg):
        if self.response.has_key(msg_type):
            self.response[msg_type].append({key:msg})
        else:
            raise ValueError

    def mandatory_check(self,data,only_check_sn=False):
        for field in self.mandatory_fields:
            if not data.has_key(field):
                self.response_msg('error','MandatoryCheckFailed', "The field [%s] is mandatory and not provided in your reporting data" % field)
        else:
            if self.response['error']:
                return False
        try:
            if not only_check_sn:
                self.asset_obj = models.Host.objects.get(id=int(data['asset_id']),sn=data['sn'])
            else:
                self.asset_obj = models.Host.objects.get(sn=data['sn'])
            return True
        except ObjectDoesNotExist,e:
            self.response_msg('error','AssetDataInvalid', "Cannot find asset object in DB by using asset id [%s] and SN [%s] " % (data['asset_id'],data['sn']))
            self.waiting_approval = True
            return False

    def get_asset_id_by_sn(self):
        data = self.request.POST.get("asset_data")
        response = {}
        if data:
            try:
                data = json.loads(data)
                if self.mandatory_check(data,only_check_sn=True):
                    response = {'asset_id': self.asset_obj.id}
                else:
                    if hasattr(self,'waiting_approval'):
                        response = {'needs_aproval': "this is a new asset,needs IT admin's approval to create the new asset id."}
                        self.clean_data = data
                        self.save_new_asset_to_approval_zone()
                    else:
                        response = self.response
            except ValueError,e:
                self.response_msg('error','AssetDataInvalid', str(e))
                response = self.response
        else:
            self.response_msg('error','AssetDataInvalid', "The reported asset data is not valid or provided")
            response = self.response
        return response

    def save_new_asset_to_approval_zone(self):
        '''When find out it is a new asset, will save the data into approval zone to waiting for IT admin's approvals'''
        asset_sn = self.clean_data.get('sn')
        try:
            models.NewAssetApprovalZone.objects.get_or_create(sn=asset_sn,
                                                              data=json.dumps(self.clean_data),
                                                              asset_type=self.clean_data.get('asset_type'),
                                                              wan_ip=self.clean_data.get('wan_ip'),
                                                              lan_ip=self.clean_data.get('lan_ip'),
                                                              cpu_num=self.clean_data.get('cpu_num'),
                                                              memory_size=self.clean_data.get('memory_size'),
                                                              disk_size=self.clean_data.get('disk_size'),
                                                              os_version=self.clean_data.get('os_version'),
                                                              ssh_port=self.clean_data.get('ssh_port'),
                                                              )
        except Exception,e:
            print 'ERR: %s' %e
        return True

    def __is_new_asset(self):
        if not hasattr(self.asset_obj,self.clean_data['asset_type']):
            return True
        else:
            return False

    def __verify_field(self,data_set,field_key,data_type,required=True):
        field_val = data_set.get(field_key)
        if field_val:
            try:
                data_set[field_key] = data_type(field_val)
            except ValueError,e:
                self.response_msg('error','InvalidField', "The field [%s]'s data type is invalid, the correct data type should be [%s] " % (field_key,data_type) )
        elif required == True:
                self.response_msg('error','LackOfField', "The field [%s] has no value provided in your reporting data [%s]" % (field_key,data_set) )

    def data_is_valid_without_id(self):
        '''when there's no asset id in reporting data ,goes through this function fisrt'''
        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)
                asset_obj = models.Host.objects.get_or_create(sn=data.get('sn'),
                                                              hostname=data.get('sn'),
                                                              wan_ip=data.get('wan_ip'),
                                                              lan_ip=data.get('lan_ip'),
                                                              cpu=data.get('cpu_num'),
                                                              memory=data.get('memory_size'),
                                                              disk=data.get('disk_size'),
                                                              os_version=data.get('os_version'),
                                                              port=data.get('ssh_port'),
                                                              idc_id=1,
                                                              ) #push asset id into reporting data before doing the mandatory check
                data['asset_id'] = asset_obj[0].id
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError,e:
                self.response_msg('error','AssetDataInvalid', str(e))
        else:
            self.response_msg('error','AssetDataInvalid', "The reported asset data is not valid or provided")

    def data_is_valid(self):
        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError,e:
                self.response_msg('error','AssetDataInvalid', str(e))
        else:
            self.response_msg('error','AssetDataInvalid', "The reported asset data is not valid or provided")
