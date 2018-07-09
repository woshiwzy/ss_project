# -*- coding: utf-8 -*-

class VPNServer:

    def __init__(self, name="", ip="", veid="", api_key="", data_counter=0, plan_monthly_data=0,
                 monthly_data_multiplier=1):
        self.name = name
        self.ip = ip
        self.veid = veid
        self.api_key = api_key
        self.suspend = False
        self.dataremaind = 0.0
        self.data_counter = data_counter
        self.plan_monthly_data = plan_monthly_data
        self.monthly_data_multiplier = monthly_data_multiplier

    def avaliable(self):

        delta = self.plan_monthly_data * self.monthly_data_multiplier - self.data_counter
        if delta <= 0:
            return 0
        else:
            return delta
