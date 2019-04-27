
from django.shortcuts import render,HttpResponse
import socket
import base64
import sys
import time
import datetime
import json
import hmac
from hashlib import sha1 as sha
from music.models import Song

# 请填写您的AccessKeyId。
access_key_id = 'LTAI5AYKfHBArSBR'
# 请填写您的AccessKeySecret。
access_key_secret = 'zxUBEOnfPCP2NPrBVD5TdhwNROcZ9m'
# host的格式为 bucketname.endpoint ，请替换为您的真实信息。
host = 'http://pandacoderblog.oss-cn-shanghai.aliyuncs.com';
# callback_url为 上传回调服务器的URL，请将下面的IP和Port配置为您自己的真实信息。
callback_url = "http://pandacoder.top/oss/";
# 用户上传文件时指定的前缀。
upload_dir = 'music/'
expire_time = 30

# Create your views here.
def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def get_token():
    now = int(time.time())
    expire_syncpoint = now + expire_time
    expire_syncpoint = 1612345678
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(upload_dir);
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy.encode())
    h = hmac.new(access_key_secret.encode(), policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    album=3
    callback_dict = {}
    callback_dict['callbackUrl'] = callback_url;
    callback_dict['callbackBody'] = 'filename=${object}&size=${size}';
    callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded';
    callback_param = json.dumps(callback_dict).strip()
    print(callback_param)
    base64_callback_body = base64.b64encode(callback_param.encode());
    print(base64_callback_body)

    token_dict = {}
    token_dict['accessid'] = access_key_id
    token_dict['host'] = host
    token_dict['policy'] = policy_encode.decode()
    token_dict['signature'] = sign_result.decode()
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    # token_dict['callback'] = base64_callback_body.decode()
    result = json.dumps(token_dict)
    return result

def tem(request):
    if request.method == 'GET':
        return HttpResponse(get_token())
    else:
        print('88880000'+str(request.POST))
        return HttpResponse('{"Status":"OK"}'.encode())

def do_POST(request):
    Song.album=request.POST['albumid'][0]
    Song.song_title=request.POST['filename'][0]
    Song.audio_file='https://pandacoderblog.oss-cn-shanghai.aliyuncs.com/'+request.POST['filename'][0]
    Song.ytburl=request.POST['ytb'][0]
    Song.length=201
    Song.save()
