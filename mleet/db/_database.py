import sqlite3
from sklearn.base import BaseEstimator
from joblib import dump
import re
import pandas as pd
from os import mkdir, path


class _Database:
    def __init__(self,
                 project_name: str,
                 metric_names: list[str]):
        project_name = project_name.lower().replace(' ', '')
        if not path.exists('exps'):
            mkdir('exps')
        if not path.exists(f'exps/{project_name}'):
            mkdir(f'exps/{project_name}')
        if not path.exists(f'exps/{project_name}/models'):
            mkdir(f'exps/{project_name}/models')
        db_path = f'exps/{project_name}/db.sqlite'

        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()
        self.__models_path = f'exps/{project_name}/models'
        self.__columns = ['id', 'exp_name'] + metric_names + ['model_path']

        self._cursor.execute(
          f'''CREATE TABLE IF NOT EXISTS Experiments(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  exp_name TEXT,
    {',\n'.join([f'\t\t  {metric} DECIMAL(10, 5)'
                 for metric in metric_names])},
                  model_path TEXT
              );'''
        )
        self._connection.commit()

    def add_experiment(self,
                       experiment_name: str,
                       metrics: dict[str, float]):#,
                       # model: BaseEstimator):
        model_path = f'{self.__models_path}/{experiment_name}.bin'
        # dump(model, model_path)
        self._cursor.execute(
          f'''INSERT INTO  Experiments(
                  exp_name,
    {',\n'.join([f'\t\t  {metric}'
                 for metric in metrics.keys()])},
                  model_path
              )
              VALUES
              (
                  '{experiment_name}',
                  {',\n\t\t  '.join(map(str, metrics.values()))},
                  '{model_path}'
              );'''
        )
        self._connection.commit()

    def select_experiments_data(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=self.__columns)

        self._cursor.execute(
           '''SELECT *
              FROM Experiments;'''
        )
        selected_data = self._cursor.fetchall()
        for row in selected_data[::-1]:
            df.loc[-1] = row
            df.index = df.index + 1
            df = df.sort_index()

        return df
