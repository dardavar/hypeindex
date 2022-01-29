import pandas as pd
import matplotlib.pyplot as plt

def arrange_data(df):
    df = df.reset_index()
    iloc_dfs = list()
    for row_index in range(0, len(df.index)):
        iloc_series = df.iloc[row_index]
        hype = int(iloc_series['hype'])
        iloc_series = iloc_series.drop('hype')
        iloc_df = pd.DataFrame(iloc_series).reset_index().rename(columns={row_index: 'price', 'index': 'mounths'})
        iloc_df['hype'] = hype
        iloc_dfs.append(iloc_df)
    return pd.concat(iloc_dfs, ignore_index=True)


def plot_single_stock_2d(df, df_name):
    df.plot(subplots=True,
            layout=(3,4),
            title='{} - Price changes as function of the hype'.format(df_name))
    plt.show()
    
def plot_all_stocks_2d(dfs, period, num_of_stocks_to_show=5):
    idx = 1
    for df in dfs:
        df['df'].plot(label=df['name'])
        idx += 1
        if idx > num_of_stocks_to_show:
            break
    plt.title("Stocks prices as function of the hype for a period of {} mounths".format(period))
    plt.legend()
    plt.show()


def plot_3d(df):
    df = arrange_data(df)
    threedee = plt.figure().gca(projection='3d')
    threedee.scatter(df['mounths'], df['hype'], df['price'])
    threedee.set_xlabel('Mounths')
    threedee.set_ylabel('Hype')
    threedee.set_zlabel('Price')
    plt.show()
