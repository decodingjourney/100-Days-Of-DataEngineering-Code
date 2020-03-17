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


def fetch_coord(tenant, entity_types, is_random_coords):
    coords_file_name = 'mutated_coords.csv' if is_random_coords else 'coords.csv'
    path = os.path.join('/home/anand/quantela_projects/learning_basic_python', coords_file_name)
    df_co_oords = pd.read_csv(path)
    df_co_oords.District = df_co_oords.District.apply(str.strip)
    df_loc_info = df_co_oords[df_co_oords['District'].str.lower() == tenant.lower()]
    df_loc_info.drop_duplicates(['Latitude', 'Longitude', 'AC'], inplace=True)

    sid_file_name = entity_types + '_sid_unique.csv'
    df_sensor_lists = pd.read_csv(os.path.join('/home/anand/quantela_projects/current_datascience/datascience-1.7.2/config/simulated_data_config', sid_file_name))
    df_sensor_lists = df_sensor_lists[['sid']]
    sensors = df_sensor_lists.sid
    if len(sensors) > df_loc_info.shape[0]:
        sensors = sensors[0:df_loc_info.shape[0]]
    else:
        df_loc_info = df_loc_info.iloc[0:sensors.shape[0]]
    df_loc_info['sid'] = sensors.values
    return df_loc_info


def generate_datetime(start_year, end_year, start_month, end_month, start_date, end_date, frequency):
    if frequency == 'half-hourly':
        freq = '30min'
    elif frequency == '8':
        freq = '480min'
    elif frequency == '4':
        freq = '240min'
    else:
        freq = '60min'

    date_start = str(start_year) + '-' + str(start_month) + '-' + str(start_date)
    date_end = str(end_year) + '-' + str(end_month) + '-' + str(end_date)

    if date_start == date_end:
        modified_end_date = (datetime.datetime.strptime(date_start, "%Y-%m-%d") + datetime.timedelta(days=1))
        date_end = datetime.datetime.strftime(modified_end_date, "%Y-%m-%d")
    my_dates = pd.date_range(date_start, date_end, freq=freq, closed='left').strftime('%Y-%m-%d %H:%M:%S')

    return my_dates


def simulate_data(tenant, property, entity_types, start_year, end_year, start_month=1, end_month=12, start_date=1, end_date=30,
                  frequency='hourly', is_random_coords=False):

    fetched_coords = fetch_coord(tenant, entity_types, is_random_coords)

    list_timestamp = pd.Series(generate_datetime(start_year=start_year, end_year=end_year, start_month=start_month,
                                                 end_month=end_month, start_date=start_date, end_date=end_date, frequency=frequency))
    fetched_coords.sid = fetched_coords.sid.str.strip()
    index = pd.MultiIndex.from_product([
        zip(fetched_coords.District, fetched_coords.AC, fetched_coords.Latitude, fetched_coords.Longitude, fetched_coords.sid), list_timestamp],
        names=["co-ords", "tmsp_value"
    ])
    df_indexed = pd.DataFrame(index=index).reset_index()
    print(df_indexed)
    return None



def raw_data_simulation():
    run_under_context = None
    current_date = datetime.datetime.today()
    previous_date = current_date - datetime.timedelta(days=1)
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
        
        simulated = simulate_data(tenant, property, entity_types, start_year, end_year,
                                                    start_month, end_month,
                                                    start_date,
                                                    end_date, frequency=frequency, is_random_coords=is_random_coords)
        print(simulated)




if __name__ == '__main__':
    # clean_up()
    raw_data_simulation()
