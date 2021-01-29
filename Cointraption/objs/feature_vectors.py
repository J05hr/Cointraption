

class FeatureVectors:

    def __init__(self, raw, perc_data, avg_data, feature_data, actions):
        self.raw_data = raw  # raw data in a pandas data frame
        self.perc_data = perc_data  # raw is transformed to percent change feature over feature
        self.avg_data = avg_data  # raw is transformed to be a predefined moving average feature over feature
        self.feature_data = feature_data  # the final feature vectors
        self.actions = actions  # list of predefined outcomes buy, sell, or hold
