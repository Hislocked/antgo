# -*- coding: UTF-8 -*-
# Time: 1/6/18
# File: crowdsource_server.py
# Author: jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import pipes
import json
import uuid
from tornado.options import define, options
define('port', default=8000, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
  def get_current_user(self):
    return self.get_secure_cookie('user')
  
  @property
  def server_pipe(self):
    return self.settings['client_pipe']
  
  @property
  def query_html(self):
    return self.settings['query_html']
  
  @property
  def query_js(self):
    return self.settings['query_js']
  
  @property
  def task_name(self):
    return self.settings['task_name']
  
  @property
  def is_random_layout(self):
    return self.settings['is_random_layout']
  
  @property
  def crowdsource_helper(self):
    return self.settings['crowdsource_helper']

  
class IndexHandler(BaseHandler):
  def get(self):
    # client id
    if self.get_secure_cookie('user') is None:
      self.set_secure_cookie('user', str(uuid.uuid4()))
    
    task = {'content': self.crowdsource_helper,
            'query_html': self.query_html,
            'query_js': self.query_js,
            'title': self.task_name,
            'is_random_layout': 1 if self.is_random_layout else 0}
    self.render('crowdsource.html', task=task)


class CustomRender(BaseHandler):
  def post(self):
    self.write(json.dumps(self.settings['custom_response_html']))


class ClientQuery(BaseHandler):
  def post(self):
    if self.get_current_user() is None:
      self.send_error(500)
    
    client_query = {}
    client_query['QUERY'] = self.get_argument('QUERY')
    client_query['CLIENT_ID'] = self.get_current_user().decode('utf-8')
    client_query['CLIENT_RESPONSE'] = {}
    client_query['CLIENT_RESPONSE']['WORKSITE'] = self.get_argument('CLIENT_RESPONSE_WORKSITE', None)
    client_query['CLIENT_RESPONSE']['CONCLUSION'] = self.get_argument('CLIENT_RESPONSE_CONCLUSION', None)
    client_query['QUERY_INDEX'] = int(self.get_argument('QUERY_INDEX', -1))
    client_query['QUERY_STATUS'] = self.get_argument('QUERY_STATUS', '')
    
    # send client query to server backend
    self.server_pipe.send(client_query)
    # waiting server response
    server_response = self.server_pipe.recv()
    
    # return
    self.write(json.dumps(server_response))


def crowdsrouce_server_start(client_pipe,
                             dump_dir,
                             crowdsource_helper,
                             task_name,
                             query_html,
                             query_js,
                             custom_response_html,
                             is_random_layout):
  tornado.options.parse_command_line()
  static_folder = '/'.join(os.path.dirname(__file__).split('/')[0:-1])

  settings={'template_path': os.path.join(static_folder, 'html', 'templates'),
            'static_path': dump_dir,
            'client_pipe': client_pipe,
            'crowdsource_helper': crowdsource_helper,
            'task_name': task_name,
            'query_html': query_html,
            'query_js': query_js,
            'custom_response_html': custom_response_html,
            'is_random_layout': is_random_layout,
            'cookie_secret': str(uuid.uuid4())}
  app = tornado.web.Application(handlers=[(r"/", IndexHandler),
                                          (r"/crowdsource/query", ClientQuery),
                                          (r"/crowdsource/render", CustomRender), ],
                                **settings)
  http_server = tornado.httpserver.HTTPServer(app)

  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()