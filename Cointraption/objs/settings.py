
class Settings:
    def __init__(self, filename, moving_avg_days, decision_range, train_percent, classification_algo):
        # classification parameters set to defaults
        self.classification_parameters = {
            "filename": filename,   # filename for the classification data
            "classification_algo": classification_algo,  # the classification algo to run the data on
            "moving_avg_days": moving_avg_days,   # number of days to smooth the data by
            "decision_range": decision_range,  # (x,y) range for hold, above x is buy, below y is sell
            "train_percent": train_percent   # percentage of data to train on
        }











