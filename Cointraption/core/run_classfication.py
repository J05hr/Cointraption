from Cointraption.objs.results import Results
import Cointraption.core.feature_extractor as featex
import Cointraption.core.bayes_classifier as nbayes
import Cointraption.core.perceptron_classifier as perceptron
from Cointraption.objs.feature_vectors import FeatureVectors
import math


def run(settings):
    filename = settings.classification_parameters["filename"]
    moving_avg_days = settings.classification_parameters["moving_avg_days"]
    decision_range = settings.classification_parameters["decision_range"]
    train_percent = settings.classification_parameters["train_percent"]
    classification_algo = settings.classification_parameters["classification_algo"]

    classification_list = []
    out_dict = {'h': 'hold', 's': 'sell', 'b': 'buy'}

    # get feature and outcomes data as a FeatureVectors object
    fvs = featex.formatdata(filename, moving_avg_days, decision_range)
    d_count = len(fvs.feature_data)  # get the total number of data points
    split_idx = math.ceil(d_count * (train_percent/100))  # calc the split index
    # split the data
    train_fvs = FeatureVectors(fvs.raw_data[:split_idx], fvs.perc_data[:split_idx], fvs.avg_data[:split_idx], fvs.feature_data[:split_idx], fvs.actions[:split_idx])
    test_fvs = FeatureVectors(fvs.raw_data[split_idx:], fvs.perc_data[split_idx:], fvs.avg_data[split_idx:], fvs.feature_data[split_idx:], fvs.actions[split_idx:])

    # figure out some basic training variables
    train_count = len(train_fvs.feature_data)  # num of features
    buy_count = 0
    sell_count = 0
    hold_count = 0
    for action in train_fvs.actions:
        if action[2] == 'b':
            buy_count += 1
        elif action[2] == 's':
            sell_count += 1
        else:
            hold_count += 1
    buy_prior = buy_count / train_count
    sell_prior = sell_count / train_count
    hold_prior = hold_count / train_count

    # classification training cases
    if classification_algo == 'Naive Bayes':
        # train model to get a data set for P(data|results) and other probabilities needed for naive bayes
        td = nbayes.train(train_fvs.feature_data, train_fvs.actions, buy_count, sell_count, hold_count)
    elif classification_algo == 'Perceptron':
        # train perceptron model
        td = perceptron.train(train_fvs.feature_data, train_fvs.actions)
    else:
        # default to perceptron if not sure of the algo
        td = perceptron.train(train_fvs.feature_data, train_fvs.actions)

    # record the accuracy of the classification
    correct_count = 0
    money_in = 0
    money_out = 0
    buy_in = 0

    # loop through the testing data and do classification
    for fvidx in range(len(test_fvs.feature_data) - 2):
        cresults = []
        featurevector = test_fvs.feature_data[fvidx]
        # classify cases
        if classification_algo == 'Naive Bayes':
            res = nbayes.classify(featurevector, td, buy_prior, sell_prior, hold_prior)
        elif classification_algo == 'Perceptron':
            res = perceptron.classify(featurevector, td)
        else:
            res = perceptron.classify(featurevector, td)

        # print the results
        print(featurevector[0])
        print("    p(buy|data)       |     p(sell|data)    |    p(hold|data)")
        print(res)
        cresults.append(featurevector[0])
        cresults.extend(res)

        # figure out the predicted outcome
        if res.index(max(res)) == 0:
            pout = 'buy'
            money_in += 100
            buy_in += 100
        elif res.index(max(res)) == 1:
            pout = 'sell'
            if money_in > 100:
                money_in -= 100
                money_out += 100
        else:
            pout = 'hold'
        # check if the test prediction was accurate and print
        testString = ""
        if out_dict[test_fvs.actions[fvidx][2]] == pout:
            correct_count += 1
            testString = "Correct | Outcome: " + out_dict[test_fvs.actions[fvidx][2]] + " | Prediction: " + pout
        else:
            testString = "Incorrect | Outcome: " + out_dict[test_fvs.actions[fvidx][2]] + " | Prediction: " + pout
        print(testString)
        cresults.append(testString)
        percnextdayclose = test_fvs.perc_data[fvidx + 1][6]
        nextdayprofit = money_in * (percnextdayclose / 100)
        money_in += nextdayprofit
        classification_list.append(cresults)

    # print the accuracy of the classification at the end of testing
    accur = (correct_count / (len(test_fvs.feature_data) - 1)) * 100
    profit = money_in + money_out - buy_in
    print("total prediction accuracy is: " + str(accur) + "%")
    print("money in: $" + str(money_in) + ", money out: $" + str(money_out))
    print("total buy in: $" + str(buy_in) + ", profit: $" + str(profit))

    # take the most recent feature and run the model to predict the unknown decision
    lastvector = test_fvs.feature_data[-1]
    # classify cases
    if classification_algo == 'Naive Bayes':
        final_prediction = nbayes.classify(lastvector, td, buy_prior, sell_prior, hold_prior)
    elif classification_algo == 'Perceptron':
        final_prediction = perceptron.classify(lastvector, td)
    else:
        final_prediction = perceptron.classify(lastvector, td)

    print("\nfinal prediction for the unknown (last day)")
    print("    p(buy|data)       |     p(sell|data)    |    p(hold|data)")
    print(str(final_prediction) + "\n")

    # control is holding the full buy-in for the entire training range.
    first = test_fvs.raw_data[0][6]
    last = test_fvs.raw_data[-3][6]
    control = buy_in * (last / first)
    profitOverControl = profit - control

    return Results(decision_range, train_percent, moving_avg_days, accur, profit, buy_in, profitOverControl,
                   classification_list, final_prediction)
