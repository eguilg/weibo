import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift
import math

def ppkr_features_t(features_t, repo, k):

    arrive_tt = repo.arrive_tt[repo['w_id'] == features_t.name].values[:k]
    interval_tt = arrive_tt - shift(arrive_tt, 1, cval=0)
    features_t[:k] = arrive_tt
    features_t['max_interval_tt'] = interval_tt.max()
    features_t['mean_interval_tt'] = interval_tt.mean()
    features_t['mean_interval_fhk_tt'] = interval_tt[:math.ceil(k/2)].mean() # mean of first half k interval
    features_t['mean_interval_lhk_tt'] = interval_tt[math.ceil(k/2):].mean() # mean of last half k interval

    return features_t

