from Cointraption.objs.bayes_data import BayesData


def train(training_fvs, outcomes, b_count, s_count, h_count):
    # initialize
    num_feats = 6
    td = BayesData(num_feats)

    # traverse the training outcomes and the training vectors at the same time and record data into td
    for idx in range(len(training_fvs)):
        # choose the right outcome to record data for
        if outcomes[idx][1] == 'b':  # use td.p_buys
            for dct_idx in range(1, num_feats):
                dct = td.p_buys[dct_idx]
                feat_value = training_fvs[idx][dct_idx]
                try:
                    dct[feat_value] += 1
                except KeyError:
                    dct.setdefault(feat_value, 1)

        elif outcomes[idx][1] == 's':  # use td.p_sells
            for dct_idx in range(1, num_feats):
                dct = td.p_sells[dct_idx]
                feat_value = training_fvs[idx][dct_idx]
                try:
                    dct[feat_value] += 1
                except KeyError:
                    dct.setdefault(feat_value, 1)

        else:  # use td.p_holds
            for dct_idx in range(1, num_feats):
                dct = td.p_holds[dct_idx]
                feat_value = training_fvs[idx][dct_idx]
                try:
                    dct[feat_value] += 1
                except KeyError:
                    dct.setdefault(feat_value, 1)

    # for each array in td, replace counts with probabilities
    o_arr = td.p_buys
    for dict_idx in range(num_feats):
        dct = o_arr[dict_idx]
        for key in dct:
            v_count = dct[key]
            # divide total outcome count by the value count
            dct[key] = v_count / b_count
    o_arr = td.p_sells
    for dict_idx in range(num_feats):
        dct = o_arr[dict_idx]
        for key in dct:
            v_count = dct[key]
            # divide total outcome count by the value count
            dct[key] = v_count / s_count
    o_arr = td.p_holds
    for dict_idx in range(num_feats):
        dct = o_arr[dict_idx]
        for key in dct:
            v_count = dct[key]
            # divide total outcome count by the value count
            dct[key] = v_count / h_count

    return td


def classify(fv, td, b_prior, s_prior, h_prior):
    p_buys = td.p_buys
    p_sells = td.p_sells
    p_holds = td.p_holds

    # smoothing value in case prob is 0
    smoothing = 0.001

    # calc p(data | result) for each outcome
    pdb = p_holds[1].get(fv[1], smoothing) * p_holds[2].get(fv[2], smoothing) * p_buys[3].get(fv[3], smoothing) * p_buys[4].get(fv[4], smoothing) * p_buys[5].get(fv[5], smoothing)
    pds = p_sells[1].get(fv[1], smoothing) * p_sells[2].get(fv[2], smoothing) * p_sells[3].get(fv[3], smoothing) * p_sells[4].get(fv[4], smoothing) * p_sells[5].get(fv[5], smoothing)
    pdh = p_holds[1].get(fv[1], smoothing) * p_holds[2].get(fv[2], smoothing) * p_holds[3].get(fv[3], smoothing) * p_holds[4].get(fv[4], smoothing) * p_holds[5].get(fv[5], smoothing)

    # calc final probabilities
    pbd = pdb * b_prior
    psd = pds * s_prior
    phd = pdh * h_prior

    norm = pdb + psd + phd

    # result is a tuple of ( p(buy|data), p(sell|data), p(hold|data) )
    res = [pbd/norm, psd/norm, phd/norm]

    return res


