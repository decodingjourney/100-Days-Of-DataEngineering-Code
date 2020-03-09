import json
import os
from glob import glob
import pandas as pd
import datetime
import sys



def clean_up():
    path = '/home/anand/quantela_projects/learning_basic_python'
    ext = '*.csv'

    all_csv_files = [file
                     for path, subdir, files in os.walk(path)
                     for file in glob(os.path.join(path, ext))]

    data = pd.read_csv('/home/anand/quantela_projects/learning_basic_python/2020-02-19.csv')

    column_remove = [col for col in data.columns if 'isIndependent' in col]
    print(column_remove)
    try:
        data = data.drop(column_remove, axis=1)
    except Exception as e:
        print(e.args[0])

    data.to_csv('/home/anand/quantela_projects/learning_basic_python/2020-02-19.csv')


def raw_data_simulation():
    run_under_context = None
    current_date = datetime.datetime.today()
    previous_date = current_date - datetime.timedelta(days=1)
    print(current_date)
    print(previous_date)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'daily':
            start_month = previous_date.month
            start_date = previous_date.day
            start_year = previous_date.year
        elif sys.argv[1] == 'hourly':
            start_month = current_date.month
            start_date = current_date.day
            start_year = current_date.year
    json_path = os.path.join('/home/anand/quantela_projects/learning_basic_python/config', 'simulated_data_config', 'final_config.json')
    with open(json_path) as json_data:
        schedule_data = json.load(json_data)

    for data in schedule_data:
        tenant_id = data['tenant_id']
        domain = data['domain']
        property = data['property']
        property_folder_name = data['property_folder_name']
        entity_types = data['entity_types']

        is_random_coords = data['is_random_coords']
        # if running for daily context didn't get data from config json
        if run_under_context is None:
            start_month = int(data['start_month'])
            end_month = int(data['end_month'])
            start_date = int(data['start_date'])
            end_date = int(data['end_date'])
            start_year = int(data['start_year'])
            end_year = int(data['end_year'])

        # Pass frequency here
        # Possible value : hourly, half-hourly, 8, 4
        frequency = data['frequency']
        tenant = tenant_id.split(".")[0]




if __name__ == '__main__':
    # clean_up()
    raw_data_simulation()
