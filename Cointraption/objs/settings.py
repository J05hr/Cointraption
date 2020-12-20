
class Settings:
    def __init__(self):

        # classification parameters set to defaults
        self.classification_parameters = {
            "filename": "",   # filename for the classification data
            "moving_avg_days": 0,   # number of days to smooth the data by
            "decision_range": (3, -3),  # (x,y) range for hold, above x is buy, below y is sell
            "train_percent": 90   # percentage of data to train on
        }











