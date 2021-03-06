# -*- coding: UTF-8 -*-
# @Time    : 2018/11/22 3:27 PM
# @File    : constant.py
# @Author  : jian<jian@mltalker.com>
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function


class Constant:
  # Data

  VALIDATION_SET_SIZE = 0.08333
  CUTOUT_HOLES = 1
  CUTOUT_RATIO = 0.5

  # Searcher

  MAX_MODEL_NUM = 1000
  BETA = 2.576
  KERNEL_LAMBDA = 0.1
  T_MIN = 0.0001
  N_NEIGHBOURS = 8
  MAX_MODEL_SIZE = (1 << 25)
  MAX_LAYER_WIDTH = 4096
  MAX_LAYERS = 100

  # Model Defaults

  DENSE_DROPOUT_RATE = 0.5
  CONV_DROPOUT_RATE = 0.25
  MLP_DROPOUT_RATE = 0.25
  CONV_BLOCK_DISTANCE = 2
  DENSE_BLOCK_DISTANCE = 1
  MODEL_LEN = 3
  MLP_MODEL_LEN = 3
  MLP_MODEL_WIDTH = 5
  MODEL_WIDTH = 64
  POOLING_KERNEL_SIZE = 2

  # ModelTrainer

  DATA_AUGMENTATION = True
  MAX_ITER_NUM = 200
  MIN_LOSS_DEC = 1e-4
  MAX_NO_IMPROVEMENT_NUM = 5
  MAX_BATCH_SIZE = 128
  LIMIT_MEMORY = False
  SEARCH_MAX_ITER = 200

  # text preprocessor

  EMBEDDING_DIM = 100
  MAX_SEQUENCE_LENGTH = 400
  MAX_NB_WORDS = 5000
  EXTRACT_PATH = "glove/"
  # Download file name
  FILE_PATH = "glove.zip"
  PRE_TRAIN_FILE_LINK = "http://nlp.stanford.edu/data/glove.6B.zip"
  PRE_TRAIN_FILE_NAME = "glove.6B.100d.txt"

  # skip type
  NO_SKIP = 0
  ADD_SKIP = 1
  CONCAT_SKIP = 2
