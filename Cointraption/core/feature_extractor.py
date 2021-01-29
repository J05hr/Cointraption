import csv
from Cointraption.objs.feature_vectors import FeatureVectors

"""
The goal is to provide a set of pandas dataframes that include:
raw data, percent change transformation, moving average transformation, 
the final feature vector set, and the set of actions/decisions.

Current Kraken csv data: 
0 unix, 1 date, 2 symbol, 3 open, 4 high, 5 low, 6 close, 7 vwap, 8 Volume BTC, 9 Volume USD, 10 tradecount
"""


def formatdata(filename, moving_avg_days, decision_range):
    raw_data = []  # raw_data
    perc_data = []  # percent change day to day, today's percent change since yesterdays close
    actions = []  # buy, sell, or hold
    avg_data = []  # moving avg
    feature_data = []

    try:
        # try to open the csv and read the raw data into a list of tuples
        with open(filename, "r") as dfile:
            csvr = csv.reader(dfile, delimiter=',')
            # skip the header
            next(csvr)
            for line in csvr:
                # small line length means theres an error
                if len(line) < 11:
                    raise Exception("number of columns in the csv is too small")
                rd = [line[0], line[1], line[2], float(line[3]), float(line[4]), float(line[5]), float(line[6]),
                      float(line[7]), float(line[8]), float(line[9]), float(line[10])]
                raw_data.append(rd)

        # generate the different data sets by looping through the raw data once
        # actions based on close to close delta, the decision range is defined by the setting decision_range
        # if the next day close is more than +x% then today was a buy
        # if it's between +x% and -y% it was a hold
        # if it's less than -y% then it was a sell
        for idx in range(len(raw_data)):
            # start features after we have enough history to get a moving average
            if idx >= moving_avg_days - 1:
                f0 = raw_data[idx][0]
                f1 = raw_data[idx][1]
                f2 = raw_data[idx][2]
                f7 = raw_data[idx][7]
                f8 = raw_data[idx][8]
                f9 = raw_data[idx][9]
                f10 = raw_data[idx][10]
                f3, f4, f5, f6 = 0, 0, 0, 0
                # avg the 5 items
                for idx in range(idx - (moving_avg_days - 1), idx + 1):
                    f3 += raw_data[idx][3]
                    f4 += raw_data[idx][4]
                    f5 += raw_data[idx][5]
                    f6 += raw_data[idx][6]
                avg_data.append([f0, f1, f2, f3 / moving_avg_days, f4 / moving_avg_days, f5 / moving_avg_days,
                                 f6 / moving_avg_days, f7, f8, f9, f10])
            # early features are left alone
            else:
                avg_data.append([raw_data[idx][0], raw_data[idx][1], raw_data[idx][2], raw_data[idx][3],
                                 raw_data[idx][4], raw_data[idx][5], raw_data[idx][6], raw_data[idx][7],
                                 raw_data[idx][8], raw_data[idx][9], raw_data[idx][10]])
                
            # start features after we have enough history to get a percent change
            if idx >= 1:
                # get the percent change
                f0 = raw_data[idx][0]
                f1 = raw_data[idx][1]
                f2 = raw_data[idx][2]
                f3 = round((100 * raw_data[idx][3] / raw_data[idx - 1][3]) - 100)
                f4 = round((100 * raw_data[idx][4] / raw_data[idx - 1][4]) - 100)
                f5 = round((100 * raw_data[idx][5] / raw_data[idx - 1][5]) - 100)
                f6 = round((100 * raw_data[idx][6] / raw_data[idx - 1][6]) - 100)
                f7 = raw_data[idx][7]
                f8 = raw_data[idx][8]
                f9 = raw_data[idx][9]
                f10 = raw_data[idx][10]
                perc_data.append([f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10])
                # using perc_data for now
                feature_data.append([f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10])

                if f6 >= decision_range[1]:
                    actions.append([raw_data[idx][0], raw_data[idx][1], 'b'])
                elif f6 <= decision_range[0]:
                    actions.append([raw_data[idx][0], raw_data[idx][1], 's'])
                else:
                    actions.append([raw_data[idx][0], raw_data[idx][1], 'h'])

            # early features are zeroed out, actions are hold
            else:
                perc_data.append([raw_data[idx][0], raw_data[idx][1], raw_data[idx][2], 0, 0, 0, 0, 0, 0, 0, 0])
                feature_data.append([raw_data[idx][0], raw_data[idx][1], raw_data[idx][2], 0, 0, 0, 0, 0, 0, 0, 0])
                actions.append([raw_data[idx][0], raw_data[idx][1], 'h'])

    except FileNotFoundError as e:
        print("Failed to open file")
        print(str(e))

    except Exception as e:
        print("Failed to read features from file")
        print(str(e))

    return FeatureVectors(raw_data, perc_data, avg_data, feature_data, actions)

