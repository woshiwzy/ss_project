# -*- coding: utf-8 -*-

import json
import math
import uuid

from django.db.models.functions import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app_ss import read_vpn_server
from models import Host, User, RewardHistory

global servers
servers = []


def initserver():
    avadata_gb = read_vpn_server.getTotalData()
    res = str(avadata_gb[0])
    global servers
    servers = avadata_gb[1]


# 获取所有服务器可用的数据
def getava_data(request):
    avadata_gb = read_vpn_server.getTotalData()
    res = str(avadata_gb[0])
    global servers
    servers = avadata_gb[1]
    return HttpResponse(outputJsonData(res), content_type="application/json")


def findServerByIp(ip):
    global servers
    if len(servers) == 0:
        initserver()
    for server in servers:
        if server.ip == ip:
            return server


# 服务器列表
def listservers(request):
    list = Host.objects.filter(enable=True, test=False).order_by('online')

    res = "["
    for r in range(0, list.__len__()):
        ser = list[r]
        if ser:
            server = findServerByIp(ser.ip)
            if server:
                res = res + (json.dumps(ser.to_dict()) + ("" if r == list.__len__() - 1 else ","))
    res = res + "]"
    if res.endswith(",]"):
        res = res.replace(",]", "]")

    print res
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

        totalRewardToday = checktotalRewardToday(uuid)

        print("已经获得奖励:" + str(totalRewardToday))

        if totalRewardToday < 500:

            if rewardsize > 100:  # reward should not above 200
                rewardsize = 100
            else:
                rewardsize = rewardsize

            print("===>>>>奖励：" + str(rewardsize) + " M")

            now = datetime.datetime.now()
            RewardHistory.objects.create(uuid=uuid, reward_size=rewardsize, descption=descption, username=user.username,
                                         year=now.year, month=now.month, day=now.day, brand=user.brand).save()

            user.remaining_bytes = user.remaining_bytes + (rewardsize * 1024)

            if user.remaining_bytes > 0 and user.enable is False:
                user.enable = True

            user.save()
            res = json.dumps(user.to_dict())
            return HttpResponse(outputJsonData(res), content_type="application/json")
        else:
            response = HttpResponse(outputJsonData("\"arrive max today\"", code=300), content_type="application/json")
            return response
    else:
        response = HttpResponse(outputJsonData("\"fail\"", code=404, message="use not exist"),
                                content_type="application/json")
        return response


def checktotalRewardToday(uuid):
    now = datetime.datetime.now()
    rewards = RewardHistory.objects.filter(uuid=uuid, year=now.year, month=now.month, day=now.day)
    print("reard his:" + str(rewards.__len__()))

    totalReward = 0
    for r in range(0, rewards.__len__()):
        totalReward = totalReward + rewards[r].reward_size;
    return totalReward


@csrf_exempt
def checkrewardHis(request):
    # date = now().date() + timedelta(days=-1)  # 昨天
    # date = now().date() + timedelta(days=0)  # 今天
    # date = now().date() + timedelta(days=1)  # 明天
    uuid = request.POST['uuid']

    # now = timezone.now()
    # start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)

    now = datetime.datetime.now()

    rewards = RewardHistory.objects.filter(uuid=uuid, year=now.year, month=now.month, day=now.day)

    print("reard his:" + str(rewards.__len__()))

    res = "["
    for r in range(0, rewards.__len__()):
        res = res + (json.dumps(rewards[r].to_dict()) + ("" if r == rewards.__len__() - 1 else ","))
    res = res + "]"

    response = HttpResponse(outputJsonData(res), content_type="application/json")
    return response


# 消耗流量
@csrf_exempt
def cost_traffic(request):
    uuid = request.POST['uuid']
    cost_size = math.fabs(int(request.POST['cost_size']))
    user = User.objects.get(uuid=uuid)
    print("===>>>>消耗：" + str(cost_size) + " KB")
    if user:
        afterUpdate = long(user.remaining_bytes - cost_size * 1.2)  # 默认消耗1.2倍，减少误差
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

            channel = request.POST['channel']
            totalbyte = 800 * 1024  # default 800M
            user = User.objects.create(username=username, mac=mac, ip=ip, brand=brand, imei=imei,
                                       system_version=system_version, country=country, app_version=app_version,
                                       usedByte=0, remaining_bytes=totalbyte, uuid=uuid.uuid4(), channel=channel)
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
