#_*_coding:utf-8_*_
import os,random,time,hashlib,json
from django.core.exceptions import ObjectDoesNotExist
from CMDB_platform import settings
from django.shortcuts import HttpResponse
from myauth import models

def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %H:%M:%S")

def handle_upload_file(request,file_obj):
    random_dir = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',10))
    upload_dir = '%s/%s' %(settings.FileUploadDir,request.user.id)
    upload_dir2 = '%s/%s' %(upload_dir,random_dir)
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
    if not os.path.isdir(upload_dir2):
        os.mkdir(upload_dir2)

    with open('%s/%s' %(upload_dir2,file_obj.name),'wb') as destination :
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return  "%s/%s" %(random_dir,file_obj.name)

def gen_token(username,timestamp,token):
    token_format = "%s\n%s\n%s" %(username,timestamp,token)
    obj = hashlib.md5()
    obj.update(token_format)
    #print '--->token format:[%s]'% token_format
    return obj.hexdigest()[7:17]

def token_required(func):
    def wrapper(*args,**kwargs):
        response = {"errors":[]}
        get_args = args[0].GET
        username = get_args.get("user")
        token_md5_from_client = get_args.get("token")
        timestamp = get_args.get("timestamp")
        if not username or not timestamp or not token_md5_from_client:
            response['errors'].append({"auth_failed":"This api requires token authentication!"})
            return HttpResponse(json.dumps(response))
        try:
            user_obj = models.UserProfile.objects.get(email=username)
            token_md5_from_server = gen_token(username,timestamp,user_obj.token)
            if token_md5_from_client != token_md5_from_server:
                response['errors'].append({"auth_failed":"Invalid username or token_id"})
            else:
                if abs(time.time() - int(timestamp)) > settings.TOKEN_TIMEOUT:  # default timeout 120
                    response['errors'].append({"auth_failed":"The token is expired!"})
                else:
                    pass #print "\033[31;1mPass authentication\033[0m"      #留给扩展暂存md5值数据库做对比认证      注：建议采用redis或memcached作为缓存数据库，如果采用列表暂存数据 但重启Django后会丢失数据
                # print "\033[41;1m;%s ---client:%s\033[0m" %(time.time(),timestamp), time.time() - int(timestamp)
        except ObjectDoesNotExist,e:
            response['errors'].append({"auth_failed":"Invalid username or token_id"})
        if response['errors']:
            return HttpResponse(json.dumps(response))
        else:
            return func(*args,**kwargs)
    return wrapper



