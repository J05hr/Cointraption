from Cointraption.objs.perceptron_data import PerceptronData


def train(training_fvs, outcomes):
    buy_weights = dict()
    sell_weights = dict()
    hold_weights = dict()
    # initialize weight dictionaries
    for col_idx in range(3, 11):
        buy_weights.setdefault(col_idx, 0)
        sell_weights.setdefault(col_idx, 0)
        hold_weights.setdefault(col_idx, 0)
    # loop through the feature vectors and train
    for row_idx in range(len(training_fvs)):
        bx = 0
        sx = 0
        hx = 0
        for col_idx in range(3, 11):
            bx += training_fvs[row_idx][col_idx] * buy_weights[col_idx]
            sx += training_fvs[row_idx][col_idx] * sell_weights[col_idx]
            hx += training_fvs[row_idx][col_idx] * hold_weights[col_idx]

        # check if we need to update buys
        if bx >= 0 and outcomes[row_idx][2] != 'b':
            # punish weights
            for col_idx in range(3, 11):
                buy_weights[col_idx] = buy_weights[col_idx] - training_fvs[row_idx][col_idx]
        elif bx < 0 and outcomes[row_idx][2] == 'b':
            # increase weights
            for col_idx in range(3, 11):
                buy_weights[col_idx] = buy_weights[col_idx] + training_fvs[row_idx][col_idx]

        # check if we need to update sells
        if sx >= 0 and outcomes[row_idx][2] != 's':
            # punish weights
            for col_idx in range(3, 11):
                sell_weights[col_idx] = sell_weights[col_idx] - training_fvs[row_idx][col_idx]
        elif sx < 0 and outcomes[row_idx][2] == 's':
            # increase weights
            for col_idx in range(3, 11):
                sell_weights[col_idx] = sell_weights[col_idx] + training_fvs[row_idx][col_idx]

        # check if we need to update holds
        if hx >= 0 and outcomes[row_idx][2] != 'h':
            # punish weights
            for col_idx in range(3, 11):
                hold_weights[col_idx] = hold_weights[col_idx] - training_fvs[row_idx][col_idx]
        elif hx < 0 and outcomes[row_idx][2] == 'h':
            # increase weights
            for col_idx in range(3, 11):
                hold_weights[col_idx] = hold_weights[col_idx] + training_fvs[row_idx][col_idx]

    return PerceptronData(buy_weights, sell_weights, hold_weights)


def classify(fv, pd):
    buy_res = 0
    sell_res = 0
    hold_res = 0
    for col_idx in range(3, 11):
        buy_res += fv[col_idx] * pd.buy_weights[col_idx]
        sell_res += fv[col_idx] * pd.sell_weights[col_idx]
        hold_res += fv[col_idx] * pd.hold_weights[col_idx]

    return buy_res, sell_res, hold_res


