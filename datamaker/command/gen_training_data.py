"""
@author: Eric Nelson
"""

import re
import argparse
import dotenv
import numpy as np
import json

from datamaker.experiment import Experiment

def gen_training_data():
  """
    Takes an experiment file, and generates training data for H2O
  """

  # Argparse
  dotenv.load_dotenv('.env')
  parser = argparse.ArgumentParser(description='Run an experiment')
  parser.add_argument('experiment', type=argparse.FileType('r'),
                      help='Experiment parameter JSON file')
  args = parser.parse_args()

  #Create our experiment, and training data
  experiment = Experiment(**json.load(args.experiment))
  data = experiment.calculate(experiment.input_training_data())

  # Make the column names useable in H2O
  name_regex = r"\('(\w+)', '(\w+)'\)"# '(parent)', '(child)' -> parent_child
  data.columns = [re.sub(name_regex, "\\1_\\2", col) for col in data.columns]

  validation_size = int(0.10 * len(data))

  validation_idx = np.random.choice(data.index, validation_size, replace=False)
  training_idx = np.setdiff1d(data.index.values, validation_idx)

  validation_set = data.ix[validation_idx]
  training_set = data.ix[training_idx]

  training_set.to_csv(experiment.training_set_file, index=False)
  validation_set.to_csv(experiment.validation_set_file, index=False)
