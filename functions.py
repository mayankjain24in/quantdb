import polars as pl
import pandas as pd
from datetime import datetime, date, time
import os, glob, zipfile, io

def is_time(obj):
    '''
    to check if a variable is time object 
    '''
    return isinstance(obj, time)

def round_to_nearest_25(n):
    return round(n / 25) * 25

def round_to_nearest_50(n):
    return round(n / 50) * 50

def round_to_nearest_100(n):
    return round(n / 100) * 100

#### Function to get atm_strike - selecting nearest (to spot) strike value from the filtered options_ieod dataframe
def get_atm_strike(opt_ieod_df, strike_col_name, spot_px):
    '''
    returns nearest strike price to given spot price, from the given option_ieod dataframe strike column
    '''
    nearest_strike = opt_ieod_df.loc[(opt_ieod_df[strike_col_name] - spot_px).abs().idxmin(), 'strike_price']
    return nearest_strike

# def find_nearest_row_polars(df, column, value):
#     '''
#     using polars, find nearest strike row from spot_ltp
#     '''
#     # Find the index of the row with the nearest value
#     df = df.with_columns((pl.col(column) - value).abs().alias('difference'))
#     # Return the row as a Series
#     return df.sort('difference').row(0)

def find_nearest_row(df, column, value):
    '''
    using pandas, find nearest strike row from spot_ltp
    '''
    # Find the index of the row with the nearest value
    idx = (df[column] - value).abs().idxmin()
    # Return the row as a Series
    return df.loc[idx]

def time_to_serial(time_str):
    # Define the start time

    start_time_str = '09:15'
    start_time = datetime.strptime(start_time_str, '%H:%M')
    
    # Convert the input time to datetime
    input_time = datetime.strptime(time_str, '%H:%M')
    
    # Calculate the difference in minutes
    time_diff = (input_time - start_time).seconds // 60
    
    # Serial number is the difference in minutes plus 1 (since 09:15 AM is serial number 1)
    serial_number = time_diff + 1
    return serial_number

def find_all_opt_tick_zip_folders(root_folder):
    zip_folders = []
    for folder_path, _, _ in os.walk(root_folder):
        # zip_files = glob.glob(os.path.join(folder_path, '*.zip'))
        zip_files = glob.glob(os.path.join(folder_path, 'NSE_OPT_TICK*.zip'))
        zip_folders.extend(zip_files)
    return zip_folders

def read_csv_in_zip(zip_file_path, csv_file_name, col_names = ['trade_date', 'trade_time', 'ltp', 'volume', 'oi']):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with zip_ref.open(csv_file_name) as csv_file:
            df = pd.read_csv(csv_file, names=col_names)
            df['trade_time'] = pd.to_datetime(df['trade_time'], format='%H:%M:%S').dt.time
    return df

def remove_seconds(t):
    return time(t.hour, t.minute, 0)

def get_polars_datetime(df, date_col='trade_date' , time_col='trade_time', new_date_time_col='trade_date_and_time'):
    '''
    to concatenate date and time column into date_time column
    '''
    df = df.with_columns(
            pl.datetime(df[date_col].dt.year(),
                       df[date_col].dt.month(),
                       df[date_col].dt.day(),
                       df[time_col].dt.hour(),
                       df[time_col].dt.minute(),
                       df[time_col].dt.second()).alias(new_date_time_col)
            )
    return df


def find_all_opt_tick_zip_folders(root_folder):
    zip_folders = []
    for folder_path, _, _ in os.walk(root_folder):
        # zip_files = glob.glob(os.path.join(folder_path, '*.zip'))
        zip_files = glob.glob(os.path.join(folder_path, 'NSE_OPT_TICK*.zip'))
        zip_folders.extend(zip_files)
    return zip_folders

def read_csv_in_zip(zip_file_path, csv_file_name, col_names = ['trade_date', 'trade_time', 'ltp', 'volume', 'oi']):
    '''
    read csv file from a zip folder using polars
    '''
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with zip_ref.open(csv_file_name) as csv_file:
            df = pl.read_csv(io.BytesIO(csv_file.read()), new_columns=col_names)
            df = df.with_columns(pl.col('trade_date').cast(pl.Utf8).str.strptime(pl.Date, "%Y%m%d"))
    return df

# def read_csv_in_zip(zip_file_path, csv_file_name, col_names = ['trade_date', 'trade_time', 'ltp', 'volume', 'oi']):
#     '''
#     read csv file from a zip folder using pandas
#     '''
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         with zip_ref.open(csv_file_name) as csv_file:
#             df = pd.read_csv(csv_file, names=col_names)
#             df['trade_time'] = pd.to_datetime(df['trade_time'], format='%H:%M:%S').dt.time
#     return df

















