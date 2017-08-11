#encoding=utf-8
from __future__ import division
from __future__ import unicode_literals

import os
from ..utils.serialize import loads,dumps
from ..utils import logger
import zmq
import uuid
import time
import json
import sys


class AntBase(object):
    def __init__(self, ant_name, ant_context, ant_token):
        self.ant_name = ant_name
        self.app_token = os.environ.get('APP_TOKEN',ant_token)
        self.app_connect = os.environ.get('APP_CONNECT','tcp://127.0.0.1:2345')

        # config zmq connect
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.REQ)
        self.zmq_socket.connect(self.app_connect)

        # core
        self.ant_context = ant_context
        self.ant_context.ant = self

        # time
        self.ant_time = time.time()

    def send(self,data,stage):
        if self.app_token is not None:
            # 0.step add extra data
            data['APP_TOKEN'] = self.app_token
            data['APP_TIME'] = str(self.ant_time)
            data['APP_HYPER_PARAMETER'] = json.dumps(self.ant_context.params)
            data['APP_RPC'] = "INFO"
            data['APP_STAGE'] = stage
            data['APP_NOW_TIME'] = str(time.time())
            data["APP_NAME"] = self.ant_name

            # 1.step send info
            self.zmq_socket.send(dumps(data))

            # 2.step ignore any receive info
            self.zmq_socket.recv(copy=False)

    def rpc(self,cmd=""):
        if self.app_token is not None:
            # 0.step config data
            data = {}
            data['APP_TOKEN'] = self.app_token
            data['APP_TIME'] = str(self.ant_time)
            data['APP_RPC'] = cmd
            data['APP_STAGE'] = 'RPC'
            data['APP_NOW_TIME'] = str(time.time())
            data["APP_NAME"] = self.ant_name

            # 1.step send rpc
            self.zmq_socket.send(dumps(data))

            # 2.step receive info
            try:
                response = loads(self.zmq_socket.recv(copy=False))
                if len(response) == 0:
                    return None
                return response
            except:
                return None

        return None

    @property
    def stage(self):
        return self.ant_context.stage
    @stage.setter
    def stage(self,val):
        self.ant_context.stage = val

    @property
    def token(self):
        return self.app_token
    @token.setter
    def token(self,val):
        self.app_token = val

    @property
    def name(self):
        return self.ant_name

    @property
    def context(self):
        return self.ant_context