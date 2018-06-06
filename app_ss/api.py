# -*- coding: utf-8 -*-

import json
import math
import uuid

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Host, User, RewardHistory


# 服务器列表
def listservers(request):
    list = Host.objects.filter(enable=True)
    res = "["
    for r in range(0, list.__len__()):
        res = res + (json.dumps(list[r].to_dict()) + ("" if r == list.__len__() - 1 else ","))
    res = res + "]"
    return HttpResponse(outputJsonData(res), content_type="application/json")


# 增加在线人数
def online(request):
    id = request.GET['hostid']  # hostid
    host = Host.objects.get(id=id)
    host.online = (host.online + 1)
    host.save()
    return HttpResponse(outputJsonData(json.dumps(host.to_dict())), content_type="application/json")


# 离线
def offline(request):
    id = request.GET['hostid']  # hostId
    host = Host.objects.get(id=id)
    oldline = host.online

    if oldline <= 0:
        host.online = 0
    else:
        host.online = oldline - 1

    host.save()
    return HttpResponse(outputJsonData(json.dumps(host.to_dict())), content_type="application/json")


# 更新流量
@csrf_exempt
def update_traffic(request):
    uuid = request.POST['uuid']
    used_size = request.POST['used_size']
    used_sizeNumber = math.fabs(float(used_size))
    user = User.objects.get(uuid=uuid)

    print("流量减少" + str(used_sizeNumber) + " kb ")
    if user:
        if user.remaining_bytes <= 1000:  # 流量用完了
            user.enable = False
            user.disableMessage = "Out of traffic"
            user.disableMessageCn = "没有流量了"
        else:
            user.remaining_bytes = user.remaining_bytes - used_sizeNumber

        user.save()

        res = json.dumps(user.to_dict())
        return HttpResponse(outputJsonData(res), content_type="application/json")
    else:
        response = HttpResponse(outputJsonData("\"fail\"", code=404, message="use not exist"),
                                content_type="application/json")
        return response


# 奖励流量
@csrf_exempt
def reward_traffic(request):
    uuid = request.POST['uuid']
    rewardsize = int(request.POST['rewardsize'])
    descption = request.POST['descption']
    user = User.objects.get(uuid=uuid)
    if user:
        if rewardsize > 200:  # reward should not above 200
            rewardsize = 200
        else:
            rewardsize = rewardsize

        print("===>>>>奖励：" + str(rewardsize) + " M")

        RewardHistory.objects.create(uuid=uuid, reward_size=rewardsize, descption=descption,
                                     username=user.username).save()

        user.remaining_bytes = user.remaining_bytes + (rewardsize * 1024)
        user.save()
        res = json.dumps(user.to_dict())
        return HttpResponse(outputJsonData(res), content_type="application/json")
    else:
        response = HttpResponse(outputJsonData("\"fail\"", code=404, message="use not exist"),
                                content_type="application/json")
        return response


@csrf_exempt
def cost_traffic(request):
    uuid = request.POST['uuid']
    cost_size = math.fabs(int(request.POST['cost_size']))
    user = User.objects.get(uuid=uuid)
    print("===>>>>消耗：" + str(cost_size) + " KB")
    if user:
        afterUpdate = long(user.remaining_bytes - cost_size)
        if afterUpdate > 0:
            user.remaining_bytes = afterUpdate
            user.enable = True
        else:
            user.remaining_bytes = 0
            user.enable = False
            user.disableMessage = "Out of Traffic"
            user.disableMessageCn = "没有流量了"

        user.usedByte = user.usedByte + cost_size
        user.save()
        res = json.dumps(user.to_dict())
        return HttpResponse(outputJsonData(res), content_type="application/json")
    else:
        response = HttpResponse(outputJsonData("\"fail\"", code=404, message="use not exist"),
                                content_type="application/json")
        return response


@csrf_exempt
def register_device(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            if user:
                if user.remaining_bytes < 1000:
                    user.enable = False
                    user.disableMessage = "Out of traffic"
                    user.disableMessageCn = "没有流量了"

                res = json.dumps(user.to_dict())
                return HttpResponse(outputJsonData(res), content_type="application/json")
        except Exception:
            mac = request.POST['mac']
            ip = request.POST['ip']
            brand = request.POST['brand']
            imei = request.POST['imei']
            system_version = request.POST['system_version']
            country = request.POST['country']
            app_version = request.POST['app_version']
            totalbyte = 800 * 1024  # default 800M
            user = User.objects.create(username=username, mac=mac, ip=ip, brand=brand, imei=imei,
                                       system_version=system_version, country=country, app_version=app_version,
                                       usedByte=0, remaining_bytes=totalbyte, uuid=uuid.uuid4())
            uuidlabel = user.uuid

            user = User.objects.get(uuid=uuidlabel)

            res = json.dumps(user.to_dict())
            return HttpResponse(outputJsonData(res), content_type="application/json")


# 输出json格式返回值
def outputJsonData(data, message="OK", code=200):
    res = "{"
    res = res + "\"message\":\"" + message + "\","
    res = res + "\"code\":" + str(code) + ","
    res = res + "\"data\":"
    res = res + data
    res = res + "}"
    return res
