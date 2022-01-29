from future.utils import iteritems
import argparse
import utils
import data_visualization

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get best hype for a given period of investment')

    parser.add_argument("-json_path", help="Path to jsons")
    parser.add_argument("-period", help="Investment period", type=int)
    parser.add_argument("-to_show", help="Number of stocks to show", type=int)
    parser.add_argument("-plot_all", help="Plot stats to al stocks.", action="store_true")

    args = parser.parse_args()
    print(args)

    path_to_jsons = args.json_path
    plot_every_stock = args.plot_all
    number_of_mounths = args.period
    num_of_stocks_to_show = args.to_show
    jsons = utils.read_jsons_from_dir(path_to_jsons)

    dfs = utils.create_stocks_dfs_from_jsons(jsons)

    hype_price_relation_dfs = dict()
    for df_name, df in iteritems(dfs):
        for period in range(4, 52, 4):
            df = utils.get_df_with_period_diff(df, period)
        hype_price_relation_df = df.drop(['price', 'volume'], axis=1).groupby('hype').mean().fillna(0)
        hype_price_relation_dfs[df_name] = hype_price_relation_df
        if plot_every_stock:
            data_visualization.plot_single_stock_2d(hype_price_relation_df, df_name)
    sorted_dfs = utils.sort_dfs_by_most_profitable_hype(hype_price_relation_dfs, number_of_mounths)
    data_visualization.plot_all_stocks_2d(sorted_dfs, number_of_mounths, num_of_stocks_to_show)
        