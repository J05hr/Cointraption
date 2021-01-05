import pandas as pd
from Cointraption.objs.feature_vectors import FeatureVectors

"""
The goal is to provide a set of pandas dataframes that include:
raw data, percent change transformation, moving average transformation, 
the final feature vector set, and the set of actions/decisions.
"""


def formatdata(filename, moving_avg_days, decision_range):
    raw_data = None
    perc_data = None
    actions = None
    avg_data = None
    feature_data = None

    try:
        raw_data = pd.read_csv(filename)  # raw_data pandas dataframe

        perc_data = raw_data.copy()  # percent change day to day, today's percent change since yesterdays close
        for idx, row in raw_data.iterrows():
            for col in raw_data.columns[3:11]:
                if idx == 0:
                    perc_data.loc[idx, col] = 0
                elif idx >= 1:
                    change = raw_data.loc[idx, col] - raw_data.loc[idx - 1, col]
                    current = raw_data.loc[idx, col]
                    if change != 0 and current != 0:
                        ratio = change / current
                        perc = ratio * 100
                    else:
                        perc = 0
                    perc_data.loc[idx, col] = perc

        # actions based on close to close delta, the decision range is defined by the setting decision_range
        # if the next day close is more than +x% then today was a buy
        # if it's between +x% and -y% it was a hold
        # if it's less than -y% then it was a sell
        actions = pd.DataFrame(columns=['action'])  # buy, sell, or hold
        for idx, row in perc_data.iterrows():
            if idx == 0:
                actions.loc[idx] = 'h'
            elif idx >= 1:
                if perc_data.iloc[idx]['close'] >= decision_range[1]:
                    actions.loc[idx] = 'b'
                elif perc_data.iloc[idx]['close'] <= decision_range[0]:
                    actions.loc[idx] = 's'
                else:
                    actions.loc[idx] = 'h'

        avg_data = raw_data.copy()  # percent change day to day, today's percent change since yesterdays close
        for idx, row in raw_data.iterrows():
            if idx >= moving_avg_days - 1:
                f3, f4, f5, f6, f7, f8, f9, f10 = 0, 0, 0, 0, 0, 0, 0, 0
                for pidx in range(idx - (moving_avg_days - 1), idx + 1):
                    f3 += raw_data.iloc[idx][3]
                    f4 += raw_data.iloc[idx][4]
                    f5 += raw_data.iloc[idx][5]
                    f6 += raw_data.iloc[idx][6]
                    f7 += raw_data.iloc[idx][7]
                    f8 += raw_data.iloc[idx][8]
                    f9 += raw_data.iloc[idx][9]
                    f10 += raw_data.iloc[idx][10]
                avrs = [f3/moving_avg_days, f4/moving_avg_days, f5/moving_avg_days, f6/moving_avg_days,
                        f7/moving_avg_days, f8/moving_avg_days, f9/moving_avg_days, f10/moving_avg_days]
                avg_data.iloc[idx][3:11] = avrs

        feature_data = avg_data.copy()
        for idx, row in avg_data.iterrows():
            for col in avg_data.columns[3:11]:
                if idx == 0:
                    feature_data.iloc[idx][col] = 0
                elif idx >= 1:
                    ratio = avg_data.iloc[idx][col] / (avg_data.iloc[idx][col] - avg_data.iloc[idx - 1][col])
                    perc = ratio * 100
                    feature_data.iloc[idx][col] = perc

    except FileNotFoundError as e:
        print("Failed to open file")
        print(str(e))

    except Exception as e:
        print("Failed to read features from file")
        print(str(e))

    return FeatureVectors(raw_data, perc_data, avg_data, feature_data, actions)

