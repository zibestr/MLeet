metrics = {
    'rmse': 0.75,
    'mae': 0.9
}
experiment_name = 'linear regression'
model_path = 'linear regression.bin'
print(f'''
              INSERT INTO  Experiments(
                  exp_name,
    {',\n'.join([f'\t\t  {metric}'
                 for metric in metrics.keys()])},
                  model_path
              )
              VALUES
              (
                  {experiment_name},
                  {',\n\t\t  '.join(map(str, metrics.values()))},
                  {model_path}
              )
        ''')
