
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.stattools import adfuller


def get_ts_strength(tt, st, rt):
    
    trend_strength = np.var(rt)/np.var(tt+rt)
    trend_strength = max([0, 1-trend_strength])

    seasonal_strength = np.var(rt)/np.var(st+rt)
    seasonal_strength = max([0, 1-seasonal_strength])
    
    sdf = pd.DataFrame([trend_strength, seasonal_strength],
                         columns=['Strength'], index=['Trend', 'Seasonal'])
    
    return sdf

def adf_test(timeseries, autolag='AIC',**kwargs):
    dftest = adfuller(timeseries, autolag=autolag, **kwargs)
    df = pd.Series(dftest[0:4],
                   index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        df['Critical Value (%s)'%key] = value
    return df.to_frame()

def kpss_test(timeseries, regression='c', nlags="auto", **kwargs):
    kpsstest = kpss(timeseries, regression=regression, nlags=nlags, **kwargs)
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    return kpss_output.to_frame()

