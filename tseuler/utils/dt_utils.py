from datetime import datetime, timedelta
from calendar import monthrange

import pandas as pd
import numpy as np

def get_datasummary(data):
    data = data.copy()
    # Get the DTypes
    total_cols = data.shape[1]
    total_rows = data.shape[0]
    dtype_dict = {'category':0, 'int': 0, 'float' : 0}
    for k,v in data.dtypes.to_dict().items():
        if 'float' in v.__str__():
            dtype_dict['float'] += 1
        if 'category' in v.__str__():
            dtype_dict['category'] += 1
        if 'int' in v.__str__():
            dtype_dict['int'] += 1

    # Get NaN dict
    nan_dict = data.isna().sum().to_dict()    
    
    return dtype_dict, nan_dict, total_cols, total_rows


#TODO @ Future: Add in-house frequency inference with ['S', 'nS', 'M', 'nM', 'H', 'nH', 'D', 'nD', 'BD', 'W', 'nW','MS', 'ME', 'QS', 'QE', 'nMS', 'nME','YS', 'YE',]
# which will also take care of the missing dates, and give the best possible frequency
def infer_dtindex(tsdata, catcols):
    pass
