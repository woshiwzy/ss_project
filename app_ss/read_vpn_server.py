# -*- coding: utf-8 -*-
import json

import requests

from app_ss.VPNServer import VPNServer


def toServer(jsobObj):
    return VPNServer(name=jsobObj['name'], veid=jsobObj['veid'], api_key=jsobObj['api_key'])


def readConfig():
    # f = open("vpn_server_config.json", "r")
    # ds = json.load(f)

    list = []
    servervps1 = VPNServer(name="vps1", ip="23.252.103.103", veid="755716", api_key="private_OyPT79iVOdyv779cn7hebjUw")
    list.append(servervps1)

    servervps2 = VPNServer(name="vps2", ip="23.252.103.122", veid="981366", api_key="private_fIF0wAGnvKrdfhCQmFiU4p80")
    list.append(servervps2)

    servervps3 = VPNServer(name="vps2", ip="23.252.103.122", veid="988929", api_key="private_ZSZN4IBebO3WXfP1zsAqkpRM")
    list.append(servervps3)

    servervps4 = VPNServer(name="vps4", ip="68.168.143.207", veid="997077", api_key="private_7tQYGEi60BEvOCuW1mHy21Hg")
    list.append(servervps4)

    servervps5 = VPNServer(name="vps5", ip="68.168.143.207", veid="997081", api_key="private_NRZxmLWJV64W3zXZRXv4Bp1g")
    list.append(servervps5)

    for server in list:
        veid = server.veid
        api_key = server.api_key
        url = 'https://api.64clouds.com/v1/getLiveServiceInfo?'
        payload = {'veid': veid, 'api_key': api_key}
        responsetext = requests.get(url, params=payload).json()
        server.suspend = bool(responsetext['suspended'])
        server.ip = responsetext['ip_addresses'][0]
        server.name = responsetext['hostname']
        server.data_counter = responsetext['data_counter']
        server.plan_monthly_data = responsetext['plan_monthly_data']
        server.dataremaind = (float(responsetext['data_counter']) / (
                responsetext['plan_monthly_data'] * responsetext['monthly_data_multiplier']))
    return list


def getTotalData():
    servers = readConfig()
    total = 0
    for server in servers:
        print server.name, server.ip, server.dataremaind, server.suspend, server.avaliable()
        if not server.suspend:
            total = total + server.avaliable()
    print "total", total / 1024 / 1024 / 1024
    return total / 1024 / 1024 / 1024,servers


if __name__ == '__main__':
    getTotalData()
    print "----------"
