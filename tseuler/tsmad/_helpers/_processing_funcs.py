from ..._utils import get_valhexrg, get_valhex11rg
from ...tsstats import ApproximateEntropry, SampleEntropy

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
import pandas as pd
import numpy as np

from warnings import filterwarnings
filterwarnings('ignore')

#FIXME : Need to handle the Frequency Aggregations slots - UV-Seasonal
def get_transformed_data(data, transformation, lag, dtfreq, anfreq):
    dt_idxname = data.index.name
    afreq_dates = data.index.to_frame()
    transformed_data = data.shift(lag)
    err = None
    print('freq', anfreq)
    print(data.asfreq('2'+anfreq))

    try:
        if transformation == 'AS':
            transformed_data = seasonal_decompose(transformed_data.dropna(), freq=12, model = 'additive', extrapolate_trend=0).seasonal        
        elif transformation == 'AT':
            transformed_data = seasonal_decompose(transformed_data.dropna(), freq=12, model = 'additive', extrapolate_trend=0).trend
        elif transformation == 'MS':
            transformed_data = seasonal_decompose(transformed_data.dropna(), freq=12, model = 'multiplicative', extrapolate_trend=0).seasonal
        elif transformation == 'MT':
            transformed_data = seasonal_decompose(transformed_data.dropna(), freq=12, model = 'multiplicative', extrapolate_trend=0).trend
    except Exception as e:
        err = e


#  [r'S', r'T', r'H',
# r'\d+S$', r'\d+T$', r'\d+H$',

# r'D', r'B',
# r'\d+D$', r'\d+B$',

# r'MS', r'M',
# r'\d+MS$', r'\d+M$',

# r'W-MON',r'W-TUE',r'W-WED',r'W-THU',r'W-FRI',r'W-SAT',r'W-SUN',
# r'\d+W-MON$',r'\d+W-TUE$',r'\d+W-WED$',r'\d+W-THU$',r'\d+W-FRI$',r'\d+W-SAT$',r'\d+W-SUN$',

# r'QS-JAN', r'QS-FEB', r'QS-MAR', r'QS-APR', r'QS-MAY', r'QS-JUN', r'QS-JUL', r'QS-AUG', r'QS-SEP', r'QS-OCT', r'QS-NOV', r'QS-DEC',
# r'\d+QS-JAN$', r'\d+QS-FEB$', r'\d+QS-MAR$', r'\d+QS-APR$', r'\d+QS-MAY$', r'\d+QS-JUN$', r'\d+QS-JUL$', r'\d+QS-AUG$', r'\d+QS-SEP$', r'\d+QS-OCT$', r'\d+QS-NOV$', r'\d+QS-DEC$',

# r'Q-JAN', r'Q-FEB', r'Q-MAR', r'Q-APR', r'Q-MAY', r'Q-JUN', r'Q-JUL', r'Q-AUG', r'Q-SEP', r'Q-OCT', r'Q-NOV', r'Q-DEC',
# r'\d+Q-JAN$', r'\d+Q-FEB$', r'\d+Q-MAR$', r'\d+Q-APR$', r'\d+Q-MAY$', r'\d+Q-JUN$', r'\d+Q-JUL$', r'\d+Q-AUG$', r'\d+Q-SEP$', r'\d+Q-OCT$', r'\d+Q-NOV$', r'\d+Q-DEC$',

# r'AS-JAN', r'AS-FEB', r'AS-MAR', r'AS-APR', r'AS-MAY', r'AS-JUN', r'AS-JUL', r'AS-AUG', r'AS-SEP', r'AS-OCT', r'AS-NOV', r'AS-DEC',
# r'\d+AS-JAN$', r'\d+AS-FEB$', r'\d+AS-MAR$', r'\d+AS-APR$', r'\d+AS-MAY$', r'\d+AS-JUN$', r'\d+AS-JUL$', r'\d+AS-AUG$', r'\d+AS-SEP$', r'\d+AS-OCT$', r'\d+AS-NOV$', r'\d+AS-DEC$',

# r'A-JAN', r'A-FEB', r'A-MAR', r'A-APR', r'A-MAY', r'A-JUN', r'A-JUL', r'A-AUG', r'A-SEP', r'A-OCT', r'A-NOV', r'A-DEC',
# r'\d+A-JAN$', r'\d+A-FEB$', r'\d+A-MAR$', r'\d+A-APR$', r'\d+A-MAY$', r'\d+A-JUN$', r'\d+A-JUL$', r'\d+A-AUG$', r'\d+A-SEP$', r'\d+A-OCT$', r'\d+A-NOV$', r'\d+A-DEC$']


    # Analysis Frequency Generation
    if anfreq == 'Weeks':
        # 'W'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("W").dt.start_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = afreq_dates[dt_idxname].apply(lambda x:'W'+str(x.week).zfill(2))
        afreq_dates['anfreq_label1'] = afreq_dates[dt_idxname].dt.day_name()
    elif anfreq == 'Month Start':
        # 'MS'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("M").dt.start_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = afreq_dates['anfreq'].dt.month_name()
        afreq_dates['anfreq_label1'] = afreq_dates[dt_idxname].dt.day
    elif anfreq == 'Month End':
        # 'M'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("M").dt.end_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = afreq_dates['anfreq'].dt.month_name()
        afreq_dates['anfreq_label1'] = afreq_dates[dt_idxname].dt.day
    elif anfreq == 'Quarter Start':
        # 'QS'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("Q").dt.start_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = pd.to_datetime(afreq_dates[dt_idxname]).dt.to_period('Q-MAR').astype(str).str[4:]
        afreq_dates['anfreq_label1'] = (afreq_dates[dt_idxname] - pd.PeriodIndex(afreq_dates[dt_idxname],freq='Q').start_time).dt.days + 1
    elif anfreq == 'Quarter End':
        # 'Q'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("Q").dt.end_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = pd.to_datetime(afreq_dates[dt_idxname]).dt.to_period('Q-MAR').astype(str).str[4:]
        afreq_dates['anfreq_label1'] = (afreq_dates[dt_idxname] - pd.PeriodIndex(afreq_dates[dt_idxname],freq='Q').start_time).dt.days + 1
    elif anfreq == 'Year Start':
        # 'AS'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("A").dt.start_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = afreq_dates[dt_idxname].dt.year
        afreq_dates['anfreq_label1'] = afreq_dates[dt_idxname].dt.dayofyear
    elif anfreq == 'Year End':
        # 'A'
        afreq_dates['anfreq'] = afreq_dates[dt_idxname].dt.to_period("A").dt.end_time.astype('datetime64[D]')
        afreq_dates['anfreq_label'] = afreq_dates[dt_idxname].dt.year
        afreq_dates['anfreq_label1'] = afreq_dates[dt_idxname].dt.month_name()

    afreq_dates['hue_col'] = afreq_dates[dt_idxname].dt.to_period("A").dt.start_time.astype('datetime64[D]').dt.year

    return transformed_data, afreq_dates['anfreq'], afreq_dates['anfreq_label'], afreq_dates['anfreq_label1'], afreq_dates['hue_col'], err

def prep_statmetric(data, variate):
    
    if variate == 'UV':
        dataDF = data[['plotX1']].copy()
        return get_unifillers(dataDF)+['X1']+['--.--']*50
    elif variate == 'BV':
        dataDF = data[['plotY', 'plotX1']].copy()
        return get_unifillers(dataDF[['plotX1']])+get_unifillers(dataDF[['plotY']])+['X1']+get_corrfillers(dataDF[['plotY', 'plotX1']].copy(), variate)
    elif variate == 'TV':
        dataDF = data[['plotY', 'plotX1', 'plotX2']].copy()
        _fillers = get_unifillers(dataDF[['plotX1']])+get_unifillers(dataDF[['plotX2']])+get_unifillers(dataDF[['plotY']])
        _fillers += ['X1']+get_corrfillers(dataDF[['plotY', 'plotX1']].copy(), variate)
        _fillers += ['X2']+get_corrfillers(dataDF[['plotY', 'plotX2']].copy(), variate)
        return _fillers

def get_corrfillers(dataDF, variate):
    dataDF = dataDF.dropna().copy()
    corrlist = []
    dataDF.rename(columns = {'plotY':'Y', 'plotX1':'X1', 'plotX2' : 'X2'}, inplace=True)
    for ecol in dataDF.columns:
        try:
            dataDF[ecol+'-AS'] = seasonal_decompose(dataDF[ecol], freq=12, model = 'additive', extrapolate_trend=0).seasonal
        except:
            dataDF[ecol+'-AS'] = np.nan
        try:
            dataDF[ecol+'-AT'] = seasonal_decompose(dataDF[ecol], freq=12, model = 'additive', extrapolate_trend=0).trend
        except:
            dataDF[ecol+'-AT'] = np.nan
        try:
            dataDF[ecol+'-MS'] = seasonal_decompose(dataDF[ecol], freq=12, model = 'multiplicative', extrapolate_trend=0).seasonal
        except:
            dataDF[ecol+'-MS'] = np.nan
        try:
            dataDF[ecol+'-MT'] = seasonal_decompose(dataDF[ecol], freq=12, model = 'multiplicative', extrapolate_trend=0).trend
        except:
            dataDF[ecol+'-MT'] = np.nan

    if any('X1' in k for k in dataDF.columns):
        dataDF = dataDF.corr()
        dataDF = dataDF[['Y', 'Y-AS', 'Y-AT', 'Y-MS', 'Y-MT']]
        dataDF = dataDF.loc[['X1', 'X1-AS', 'X1-AT', 'X1-MS', 'X1-MT'], :]
    elif any('X2' in k for k in dataDF.columns):
        dataDF = dataDF.corr()
        dataDF = dataDF[['Y', 'Y-AS', 'Y-AT', 'Y-MS', 'Y-MT']]
        dataDF = dataDF.loc[['X2', 'X2-AS', 'X2-AT', 'X2-MS', 'X2-MT'], :]
    corrlist = []

    for k in list(dataDF.values.ravel()):
        if not pd.isna(k):
            corrlist.append(get_valhex11rg(k))
            corrlist.append(round(k,2))
        else:
            corrlist.append(get_valhex11rg(1))
            corrlist.append('--')
    return corrlist

def get_unifillers(dataDF):
    format_fillers = []
    statReport = dataDF.dropna().describe()
    _count, _mean, _std, _min, _pct25, _pct50, _pct75, _max = np.ravel(statReport.values)
    # Nan
    _nancounts = pd.isna(dataDF).sum().values[0]
    _nanpct = _nancounts/_count
    _nancolor = get_valhexrg(_nanpct)
    format_fillers+=[_nancolor, _nancounts, round(_nanpct*100, 2)]
    # 0s
    _zerocounts = (dataDF.dropna() == 0.0).sum().values[0]
    _zeropct = _zerocounts/_count
    _zerocolor = get_valhexrg(_zeropct)
    format_fillers+=[_zerocolor, _zerocounts, round(_zeropct*100, 2)]
    # +ive's
    _poscounts = (dataDF.dropna() >= 0.0).sum().values[0]
    _pospct = _poscounts/_count
    _poscolor = get_valhexrg(_pospct)
    format_fillers+=[_poscolor, _poscounts, round(_pospct*100, 2)]
    # -ive's
    _negcounts = (dataDF.dropna() < 0.0).sum().values[0]
    _negpct = _negcounts/_count
    _negcolor = get_valhexrg(_negpct)
    format_fillers+=[_negcolor, _negcounts, round(_negpct*100, 2)]
    format_fillers+=[round(_count, 3), round(_mean, 3), round(_std, 3), round(_min, 3),
                     round(_pct25, 3), round(_pct50, 3), round(_pct75, 3), round(_max, 3)]
    # ADF
    adfStationarity, adfStationarityPVal = adf_test(dataDF)
    # KPSS
    kpssStationarity, kpssStationarityPVal = kpss_test(dataDF)
    # Entropy
    format_fillers+=[adfStationarity, round(adfStationarityPVal, 3), kpssStationarity, round(kpssStationarityPVal, 3)]
    format_fillers.append(ApproximateEntropry([e[0] for e in dataDF.values.tolist()], 2, 0.2*np.std([e[0] for e in dataDF.values.tolist()])))
    format_fillers.append(SampleEntropy([e[0] for e in dataDF.values.tolist()], 2, 0.2*np.std([e[0] for e in dataDF.values.tolist()])))

    return format_fillers

## Statistical Tests
def adf_test(_df, signif_val = 0.05):
    if _df.shape[0] < 5000:
        
        _series= pd.Series(_df.values.flatten(), index=_df.index).dropna()
        result = adfuller(_series, autolag='AIC')
        p = result[1]
        if p < signif_val :
            return True, p
        else :
            return False, p
    else:
        return '', '--'
    
def kpss_test(_df):
    
    _series= pd.Series(_df.values.flatten(), index=_df.index).dropna()
    result = kpss(_series, regression='c', nlags='auto')
    
    if (result[0] > [e for e in result[-1].values()]).sum() == 4:
        return False, result[1]
    else:
        return True, result[1]


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