import csv
import pandas as pd
from Cointraption.objs.feature_vectors import FeatureVectors
"""
The goal is to provide a set of pandas dataframes that include:
raw data, percent change transformation, moving average transformation, 
the final feature vector set, and the set of outcomes.
"""


def formatdata(filename, moving_avg_days, decision_range):

    feature_data = []

    try:
        raw_data = pd.read_csv(filename)  # raw_data pandas dataframe

        perc_data = raw_data.copy()  # percent change day to day, today's percent change since yesterdays close
        for idx, row in raw_data.iterrows():
            for col in raw_data.columns:
                if idx == 0:
                    perc_data.iloc[idx][col] = 0
                elif idx >= 1:
                    ratio = raw_data.iloc[idx][col] / (raw_data.iloc[idx][col] - raw_data.iloc[idx - 1][col])
                    perc = ratio * 100
                    perc_data.iloc[idx][col] = perc

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

        avg_data = []  # moving avg
        # turn the raw data list into a feature list
        # features defined by a moving average of each days variables
        for vidx in range(len(raw_data)):
            # start avgs after we have enough history
            if vidx >= moving_avg_days-1:
                f1, f2, f3, f4, f5 = 0, 0, 0, 0, 0
                f0 = raw_data[vidx][0]
                # avg the 5 items
                for idx in range(vidx-(moving_avg_days - 1), vidx + 1):
                    f1 += raw_data[idx][1]
                    f2 += raw_data[idx][2]
                    f3 += raw_data[idx][3]
                    f4 += raw_data[idx][4]
                    f5 += raw_data[idx][5]
                # append the avgs to the feature list
                avg_data.append((f0, f1 / moving_avg_days, f2 / moving_avg_days, f3 / moving_avg_days, f4 / moving_avg_days, f5 / moving_avg_days))

        for aidx in range(len(avg_data)):
            # start features after we have enough history to get a percent change
            if aidx >= 1:
                # get the percent change
                f0 = avg_data[aidx][0]
                f1 = round((100 * avg_data[aidx][1] / avg_data[aidx-1][1]) - 100)
                f2 = round((100 * avg_data[aidx][2] / avg_data[aidx-1][2]) - 100)
                f3 = round((100 * avg_data[aidx][3] / avg_data[aidx-1][3]) - 100)
                f4 = round((100 * avg_data[aidx][4] / avg_data[aidx-1][4]) - 100)
                f5 = round((100 * avg_data[aidx][5] / avg_data[aidx-1][5]) - 100)
                # append the avgs to the feature list
                feature_data.append((f0, f1, f2, f3, f4, f5))

        # outcomes
        for vidx in range(len(raw_data)):
            # start features after we have enough history to get a percent change
            if vidx >= 1:
                # get the percent change
                f0 = raw_data[vidx][0]
                f1 = round((100 * raw_data[vidx][1] / raw_data[vidx - 1][1]) - 100)
                f2 = round((100 * raw_data[vidx][2] / raw_data[vidx - 1][2]) - 100)
                f3 = round((100 * raw_data[vidx][3] / raw_data[vidx - 1][3]) - 100)
                f4 = round((100 * raw_data[vidx][4] / raw_data[vidx - 1][4]) - 100)
                f5 = round((100 * raw_data[vidx][5] / raw_data[vidx - 1][5]) - 100)
                # append the avgs to the feature list
                perc_data.append((f0, f1, f2, f3, f4, f5))

        # decisions based on close price of the next day, the outcome range is defined by the outcomebasis tuple
        # if the next day close is more than +x% then it was a buy
        # if it's between +x% and -y% it was a hold
        # if it's less than -y% then it was a sell
        for idx in range(len(perc_data)-1):
            if perc_data[idx+1][4] >= decision_range[1]:
                outcomes.append((perc_data[idx][0], 'b'))
            elif perc_data[idx+1][4] <= decision_range[0]:
                outcomes.append((perc_data[idx][0], 's'))
            else:
                outcomes.append((perc_data[idx][0], 'h'))

    except FileNotFoundError as e:
        print("Failed to open file")
        print(str(e))

    except Exception as e:
        print("Failed to read features from file")
        print(str(e))

    # return the arrays and trim so indexes match based on the moving average days
    rlst = moving_avg_days
    plst = moving_avg_days - 1
    olst = plst

    # feature_data will always have an additional item at the end which is used to make the final prediction
    return FeatureVectors(raw_data[rlst:-1], perc_data[plst:-1], avg_data[1:-1], feature_data, outcomes[olst:])

