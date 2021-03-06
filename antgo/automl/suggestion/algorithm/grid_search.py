import json
import itertools
from antgo.automl.suggestion.algorithm.abstract_algorithm import *
from antgo.automl.suggestion.models import *
from random import sample
import random
import time
import time
import uuid
from datetime import datetime
from antgo.utils.utils import *


class GridSearchAlgorithm(AbstractSuggestionAlgorithm):
  def get_new_suggestions(self, study_name, trials=[], number=1):
    """
    Get the new suggested trials with grid search.
    """
    return_trial_list = []
    study = Study.get('name', study_name)
    if study is None:
      return []

    study_configuration_json = json.loads(study.study_configuration)
    params = study_configuration_json["params"]

    # [['8', '16', '32', '64'], ['sgd', 'adagrad', 'adam', 'ftrl'], ['true', 'false']]
    param_values_list = []
    param_name_list = []
    for param in params:
      # Check param type
      if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
        raise Exception("Grid search does not support DOUBLE and INTEGER")

      repeat_num = 1
      if 'num' in param:
        repeat_num = random.randint(0, int(param['num']))

      if repeat_num == 0:
        continue

      feasible_point_list = [
          value.strip() for value in param["feasiblePoints"].split(",")
      ]

      for repeat_index in range(repeat_num):
        if repeat_num == 1:
          param_name_list.append((param['parameterName'], param['superscript'] if 'superscript' in param else '', param['target'] if 'target' in param else ''))
        else:
          param_name_list.append(('%s/%d'%(param['parameterName'], repeat_index), param['superscript'] if 'superscript' in param else '', param['target'] if 'target' in param else ''))

        if param['type'] == 'COMPLEX_DISCRETE':
          temp = []
          for v in feasible_point_list:
            temp.append(v.split(';'))

          param_values_list.append(list(itertools.product(*temp)))
        else:
          param_values_list.append(feasible_point_list)

    param_number = len(param_name_list)

    # Example: [('8', 'sgd', 'true'), ('8', 'sgd', 'false'), ('8', 'adagrad', 'true'), ('8', 'adagrad', 'false'), ('8', 'adam', 'true'), ('8', 'adam', 'false'), ('8', 'ftrl', 'true'), ('8', 'ftrl', 'false'), ('16', 'sgd', 'true'), ('16', 'sgd', 'false'), ('16', 'adagrad', 'true'), ('16', 'adagrad', 'false'), ('16', 'adam', 'true'), ('16', 'adam', 'false'), ('16', 'ftrl', 'true'), ('16', 'ftrl', 'false'), ('32', 'sgd', 'true'), ('32', 'sgd', 'false'), ('32', 'adagrad', 'true'), ('32', 'adagrad', 'false'), ('32', 'adam', 'true'), ('32', 'adam', 'false'), ('32', 'ftrl', 'true'), ('32', 'ftrl', 'false'), ('64', 'sgd', 'true'), ('64', 'sgd', 'false'), ('64', 'adagrad', 'true'), ('64', 'adagrad', 'false'), ('64', 'adam', 'true'), ('64', 'adam', 'false'), ('64', 'ftrl', 'true'), ('64', 'ftrl', 'false')]
    combination_values_list = list(itertools.product(*param_values_list))

    # Example: [{"hidden2": "8", "optimizer": "sgd", "batch_normalization": "true"}, ......]
    all_combination_values_json = []

    for combination_values in combination_values_list:
      assert(len(combination_values) == len(param_name_list))

      combination_values_json = {}

      # Example: (u'8', u'sgd', u'true')
      for i in range(param_number):
        # Example: "sgd"
        combination_values_json[param_name_list[i][0]] = (combination_values[i], param_name_list[i][1], param_name_list[i][2])

      all_combination_values_json.append(combination_values_json)

    all_combination_number = len(all_combination_values_json)

    # Compute how many grid search params have been allocated
    allocated_trials = Trial.filter('study_name', study_name)
    return_trials_start_index = len(allocated_trials)

    if return_trials_start_index > all_combination_number:
      return_trials_start_index = 0
    elif return_trials_start_index + number > all_combination_number:
      return_trials_start_index = all_combination_number - number

    for i in range(number):
      trail_name = '%s-%s' % (str(uuid.uuid4()), datetime.fromtimestamp(timestamp()).strftime('%Y%m%d-%H%M%S-%f'))
      trial = Trial.create(Trial(study.name, trail_name, created_time=time.time(), updated_time=time.time()))
      trial.parameter_values = json.dumps(
          all_combination_values_json[return_trials_start_index + i])

      return_trial_list.append(trial)
    return return_trial_list


if __name__ == '__main__':
  study_configuration = {
          "goal": "MAXIMIZE",
          "maxTrials": 5,
          "maxParallelTrials": 1,
          "params": [
              {
                  "parameterName": "conv2d",
                  "type": "COMPLEX_DISCRETE",
                  "feasiblePoints": "1,1",
                  "superscript": "kernel_size_h,kernel_size_w",
                  "num": 2,
              },
              {
                  "parameterName": "separable_conv2d",
                  "type": "COMPLEX_DISCRETE",
                  "feasiblePoints": "3,3,1;3;6;9;11,1;3;6;9;11",
                  "superscript": "kernel_size_h,kernel_size_w,rate_h,rate_w",
                  "num": 4,
              },
              {
                  "parameterName": "spp",
                  "type": "COMPLEX_DISCRETE",
                  "feasiblePoints": "1;2;4;8,1;2;4;8",
                  "superscript": "grid_h,grid_w",
                  "num": 1,
              }

          ],
  }

  study_algorithm = 'grid_search'
  Study.create(Study('Hello', json.dumps(study_configuration), study_algorithm))

  gsa = GridSearchAlgorithm()
  result = gsa.get_new_suggestions('Hello')
  print(result[0].parameter_values)
  print("aa")