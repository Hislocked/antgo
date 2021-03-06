# -*- coding: UTF-8 -*-
# @Time    : 2018/11/21 5:14 PM
# @File    : stublayer.py
# @Author  : jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function


class StubLayer(object):
  def __init__(self, input=None, output=None, **kwargs):
    self.input = input
    self.output = output
    self.id = -1
    self.weights = None
    self.spatial_change = False
    self._layer_type = None
    self._layer_name = None
    self._n_dim = -1
    self._layer_width = 0
    self.nickname = kwargs['nickname'] if 'nickname' in kwargs else ''
    self.cell_name = kwargs['cell_name'] if 'cell_name' in kwargs else ''
    self.block_name = kwargs['block_name'] if 'block_name' in kwargs else ''
    self._layer_factory = kwargs['layer_factory'] if 'layer_factory' in kwargs else None

    self.layer_group = []
    group_parent = kwargs.get('group', None)
    if group_parent is not None:
      group_parent.add_to(self)

  def set_input(self, node):
    self.input = node

  def get_input(self):
    return self.input

  def set_output(self, node):
    self.output = node

  def get_output(self):
    return self.output

  def set_weights(self, weights):
    self.weights = weights

  def get_weights(self):
    return self.weights

  def import_weights(self, layer):
    pass

  def export_weights(self, layer):
    pass

  def size(self):
    return 0

  @property
  def output_shape(self):
    return self.input.shape

  @property
  def is_spatial_change(self):
    return self.spatial_change

  @is_spatial_change.setter
  def is_spatial_change(self, val):
    self.spatial_change = val

  def __call__(self, *args, **kwargs):
    raise NotImplementedError

  @property
  def layer_type(self):
    return self._layer_type

  @layer_type.setter
  def layer_type(self, val):
    self._layer_type = val

  @property
  def layer_type_encoder(self):
    return 0

  @property
  def layer_name(self):
    return self._layer_name

  @layer_name.setter
  def layer_name(self, val):
    self._layer_name = val

  @property
  def n_dim(self):
    return self._n_dim

  @n_dim.setter
  def n_dim(self, val):
    self._n_dim = val

  @property
  def layer_width(self):
    return self._layer_width

  @layer_width.setter
  def layer_width(self, val):
    self._layer_width = val

  def flops(self):
    return 0

  @property
  def layer_factory(self):
    return self._layer_factory

  @layer_factory.setter
  def layer_factory(self, val):
    self._layer_factory = val
    for v in self.layer_group:
      v.layer_factory = val

  def add_to(self, val):
    self.layer_group.append(val)