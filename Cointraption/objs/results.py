
class Results:
    def __init__(self, outcome_range, train_percent, moving_avg, p_accuracy, profit, buy_in, profit_over_control,
                 classification_list, final_prediction):
        self.outcome_range = outcome_range
        self.train_percent = train_percent
        self.moving_avg = moving_avg
        self.p_accuracy = p_accuracy
        self.profit = profit
        self.buy_in = buy_in
        self.profit_over_control = profit_over_control
        self.classification_list = classification_list
        self.final_prediction = final_prediction

