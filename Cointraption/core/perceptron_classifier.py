from Cointraption.objs.perceptron_data import PerceptronData


def train(trainingfvs, outcomes):
    buy_weights = dict()
    sell_weights = dict()
    hold_weights = dict()
    for col in trainingfvs.columns[3:11]:
        buy_weights.setdefault(col, 0)
        sell_weights.setdefault(col, 0)
        hold_weights.setdefault(col, 0)
    for idx, row in trainingfvs.iterrows():
        bx = 0
        sx = 0
        hx = 0
        for col in trainingfvs.columns[3:11]:
            bx += trainingfvs.loc[idx, col] * buy_weights[col]
            sx += trainingfvs.loc[idx, col] * sell_weights[col]
            hx += trainingfvs.loc[idx, col] * hold_weights[col]
        # check if we need to update buys
        if bx >= 0 and outcomes.loc[idx, 'action'] != 'buy':
            # punish weights
            for col in trainingfvs.columns[3:11]:
                buy_weights[col] = buy_weights[col] - trainingfvs.loc[idx, col]
        elif bx < 0 and outcomes.loc[idx, 'action'] == 'buy':
            # increase weights
            for col in trainingfvs.columns[3:11]:
                buy_weights[col] = buy_weights[col] + trainingfvs.loc[idx, col]
        # check if we need to update sells
        if sx >= 0 and outcomes.loc[idx, 'action'] != 'sell':
            # punish weights
            for col in trainingfvs.columns[3:11]:
                sell_weights[col] = sell_weights[col] - trainingfvs.loc[idx, col]
        elif sx < 0 and outcomes.loc[idx, 'action'] == 'sell':
            # increase weights
            for col in trainingfvs.columns[3:11]:
                sell_weights[col] = sell_weights[col] + trainingfvs.loc[idx, col]
        # check if we need to update holds
        if hx >= 0 and outcomes.loc[idx, 'action'] != 'hold':
            # punish weights
            for col in trainingfvs.columns[3:11]:
                hold_weights[col] = hold_weights[col] - trainingfvs.loc[idx, col]
        elif hx < 0 and outcomes.loc[idx, 'action'] == 'hold':
            # increase weights
            for col in trainingfvs.columns[3:11]:
                hold_weights[col] = hold_weights[col] + trainingfvs.loc[idx, col]

    return PerceptronData(buy_weights, sell_weights, hold_weights)


def classify(fv, pd):
    buy_res = 0
    sell_res = 0
    hold_res = 0
    for key in fv:
        buy_res += fv[key] * pd.buy_weights[key]
        sell_res += fv[key] * pd.sell_weights[key]
        hold_res += fv[key] * pd.hold_weights[key]

    return buy_res, sell_res, hold_res


