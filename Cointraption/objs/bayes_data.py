

class BayesData:
    def __init__(self, numfeat):
        # each item is an array of feature dictionaries
        # keys correspond to feature values and values correspond to probabilities
        self.p_buys = []  # array for buys
        self.p_sells = []  # array for sells
        self.p_holds = []  # array for holds
        # add the dictionaries for the number of features we have
        for idx in range(numfeat):
            self.p_buys.append(dict())
            self.p_sells.append(dict())
            self.p_holds.append(dict())


