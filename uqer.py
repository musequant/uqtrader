#coding=utf-8
"""
封装优矿网的接口。

"""

import requests
import json
import datetime as dt
import time
import tushare as ts

headers = {'Content-Type':'application/json'}
login_url = 'https://gw.wmcloud.com/usermaster/authenticate.json'
order_url = 'https://gw.wmcloud.com/mercury_trade/strategy/%s/order'
strategy_url = 'https://gw.wmcloud.com/mercury_trade/strategy'

class Uqer(object):

    def __init__(self, user, pwd, percent=0.02, strategy_id=1):

        self.user, self.pwd            = user, pwd
        self.percent, self.strategy_id = percent, strategy_id

        self._login()

    def _login(self):
        """登陆优矿"""
        
        s = self.session = requests.Session()
        user, pwd = self.user, self.pwd

        if '@' in user:
            user, tenant = user.split("@") 
        else:
            tenant = ''
        
        data = dict(username=user, password=pwd, tenant=tenant)
        res = s.post(login_url, data)
        
        if not res.ok or not res.json().get('content', {}).get('accountId', 0):
            print res.json()
            raise Exception('login error!')


    def get_order(self, strategy_id, all=True):
        """获取订单列表
            :param all:True返回当日所有订单，False返回上次下单后新产生的订单。
        """

        s = self.session
        orders = s.get(order_url%strategy_id).json()
        
        percent = self.percent

        if all:
            return orders
        else:
            tmp_orders = []
            for order in orders:
                price = float(ts.get_realtime_quotes(order['ticker']).price)
                order['price'] = round(price*(order['side']=='BUY' and 1.+percent or 1.-percent), 2)
                tmp_orders.append(order)
            return tmp_orders


    def get_strategy_list(self):
        """获取订单列表
            :param all:True返回当日所有订单，False返回上次下单后新产生的订单。
        """

        s = self.session
        strategies = s.get(strategy_url).json()

        return {e['name']: e['id'] for e in strategies}
