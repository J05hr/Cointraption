from Cointraption.objs.results import Results
import Cointraption.core.feature_extractor as featex
import Cointraption.core.bayes_classifier as nbayes
import math


def run(settings):
    filename = settings.classification_parameters["filename"]
    moving_avg_days = settings.classification_parameters["moving_avg_days"]
    decision_range = settings.classification_parameters["decision_range"]
    train_percent = settings.classification_parameters["train_percent"]

    classification_list = []
    final_prediction = []
    out_dict = {'h': 'hold', 's': 'sell', 'b': 'buy'}

    # get feature and outcomes data as a FeatureVectors object
    fvs = featex.formatdata(filename, moving_avg_days, decision_range)

    # get the total number of data points
    d_count = len(fvs.featurelist)

    split_idx = math.ceil(d_count * (train_percent/100))  # calc the split index
    # split the data
    train_fvs = fvs.featurelist[:split_idx]
    test_fvs = fvs.featurelist[split_idx:]
    test_outcomes = fvs.actions[split_idx:]

    # figure out some basic training variables
    traindcnt = len(train_fvs.feature_data)  # num of features
    bcount = 0
    scount = 0
    hcount = 0
    for outcome in train_fvs.outcomes:
        if outcome[1] == 'b':
            bcount += 1
        elif outcome[1] == 's':
            scount += 1
        else:
            hcount += 1
    bprior = bcount / traindcnt
    sprior = scount / traindcnt
    hprior = hcount / traindcnt

    # train model to get a data set for P(data|results) and other probabilities needed for naive bayes
    td = nbayes.train(train_fvs.featurelist, train_fvs.outcomes, bcount, scount, hcount)

    # record the accuracy of the classification
    correctcnt = 0
    monin = 0
    monout = 0
    buyin = 0
    control = 0

    # loop through the testing data and do classification
    for fvidx in range(len(test_fvs.featurelist)-2):
        cresults = []
        featurevector = test_fvs.featurelist[fvidx]
        # get evidence probability for this vector
        ev = nbayes.getevidence(featurevector, train_fvs.featurelist, traindcnt)
        res = nbayes.classify(featurevector, td, ev, bprior, sprior, hprior)
        # print the results
        print(featurevector[0])
        print("    p(buy|data)       |     p(sell|data)    |    p(hold|data)")
        print(res)
        cresults.append(featurevector[0])
        cresults.extend(res)

        # figure out the predicted outcome
        if res.index(max(res)) == 0:
            pout = 'buy'
            monin += 100
            buyin += 100
        elif res.index(max(res)) == 1:
            pout = 'sell'
            if monin > 100:
                monin -= 100
                monout += 100
        else:
            pout = 'hold'
        # check if the test prediction was accurate and print
        testString = ""
        if out_dict[test_fvs.outcomes[fvidx][1]] == pout:
            correctcnt += 1
            testString = "Correct | Outcome: " + out_dict[test_fvs.outcomes[fvidx][1]] + " | Prediction: " + pout
        else:
            testString = "Incorrect | Outcome: " + out_dict[test_fvs.outcomes[fvidx][1]] + " | Prediction: " + pout
        print(testString)
        cresults.append(testString)
        percnextdayclose = test_fvs.perclist[fvidx+1][4]
        nextdayprofit = monin * (percnextdayclose/100)
        monin += nextdayprofit
        classification_list.append(cresults)

    # print the accuracy of the classification at the end of testing
    accur = (correctcnt / (len(test_fvs.featurelist)-1)) * 100
    profit = monin + monout - buyin
    print("total prediction accuracy is: " + str(accur) + "%")
    print("money in: $" + str(monin) + ", money out: $" + str(monout))
    print("total buy in: $" + str(buyin) + ", profit: $" + str(profit))

    # take the most recent feature and run the model to predict the unknown decision
    lastvector = test_fvs.featurelist[-1]
    ev = nbayes.getevidence(lastvector, train_fvs.featurelist, traindcnt)
    final_prediction = nbayes.classify(lastvector, td, ev, bprior, sprior, hprior)
    print("\nfinal prediction for the unknown (last day)")
    print("    p(buy|data)       |     p(sell|data)    |    p(hold|data)")
    print(str(final_prediction) + "\n")

    # control is holding the full buy-in for the entire training range.
    first = test_fvs.rawlist[0][4]
    last = test_fvs.rawlist[-3][4]
    control = buyin * (last / first)
    profitOverControl = profit - control

    return Results(decision_range, train_percent, moving_avg_days, accur, profit, buyin, profitOverControl,
                   classification_list, final_prediction)
