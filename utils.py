import pandas as pd
import os
import json

def sort_dfs_by_most_profitable_hype(dfs, number_of_mounths):
    sorted_dfs_list = list()
    for stock_name in dfs.keys():
        d = dict()
        d['name'] = stock_name
        d['df'] = dfs[stock_name][str(number_of_mounths)]
        d['best_hype'] = d['df'].idxmax()
        d['price_at_best_hype'] = d['df'][d['best_hype']]
        sorted_dfs_list.append(d)
    sorted_dfs_list = sorted(sorted_dfs_list, key=lambda x: (x['best_hype'], -x['price_at_best_hype']))
    return sorted_dfs_list

def read_jsons_from_dir(path_to_jsons):
    jsons = list()
    for filename in os.listdir(path_to_jsons):
        if os.path.splitext(filename)[1] != ".json":
            continue
        filename = os.path.join(path_to_jsons, filename)
        with open(filename) as f:
            jsons.append(json.load(f))
    return jsons


def create_stocks_dfs_from_jsons(jsons):
    dfs = dict()
    for stock_json in jsons:
        df = pd.DataFrame(stock_json['data']).astype({'price': 'float', 'hype': 'int'}).dropna()
        df_name = stock_json['asset']['symbol']
        df.name = df_name
        dfs[df_name] = df
    return dfs


def get_df_by_datatime(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = clean_data(df)
    return df
        

def clean_data(df):
    return df.asfreq('W-MON', fill_value=df.mean())


def get_df_with_period_diff(df, period):
        df['{}'.format(int(period/4))] = df['price'].diff(periods=period)
        return df
        

