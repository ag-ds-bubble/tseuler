from ..._utils import get_valhexrg, get_valhex11rg
from ...tsstats import ApproximateEntropry, SampleEntropy
from .._helpers import TS_FREQ_MAP, TS_FREQUENCIES, TSMAD_CONFIGS
from ..._utils import format_with_suffix

import re
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
import pandas as pd
import numpy as np
from warnings import filterwarnings
filterwarnings('ignore')


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
    _corr_method = TSMAD_CONFIGS['stat.corr_type']
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
        dataDF = dataDF.corr(method=_corr_method)
        dataDF = dataDF[['Y', 'Y-AS', 'Y-AT', 'Y-MS', 'Y-MT']]
        dataDF = dataDF.loc[['X1', 'X1-AS', 'X1-AT', 'X1-MS', 'X1-MT'], :]
    elif any('X2' in k for k in dataDF.columns):
        dataDF = dataDF.corr(method=_corr_method)
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
    format_fillers+=[format_with_suffix(_count), format_with_suffix(_mean), format_with_suffix(_std), format_with_suffix(_min),
                     format_with_suffix(_pct25), format_with_suffix(_pct50), format_with_suffix(_pct75), format_with_suffix(_max)]
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


# S3_Slab Functions
# ==========================
# TODO : Based on freq, decide freq of the decompose
def get_transformed_data(data, transformation, lag):
    transformed_data = data.shift(lag)
    err = None
    # Handle Transformations
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

    return transformed_data, err

# TODO : Fix for those frequencies at/after which the dataframe becomes empty...
def get_available_frequencies(data, datafreq, freq_group, how_aggregate):

    available_freqs = []
    available_max = []
    err = None

    _mult = re.search(r'\d+', datafreq)
    if _mult:
        available_max.append(int(_mult.group()))
        available_freqs.append(datafreq.replace(_mult.group(), ''))
    else:
        available_max.append(1)
        available_freqs.append(datafreq)
    for econvfreq in TS_FREQ_MAP[freq_group]:
        _tempresample = data.resample(econvfreq, label='right').agg(how_aggregate).dropna()
        if not _tempresample.empty:
            available_freqs.append(econvfreq)
            available_max.append(5)

    return np.array(available_freqs), np.array(available_max)

def get_aggregated_data(data, anfreq, howagg):
    # As the frequency is changed, the data needs to be aggregated
    data = data.copy()
    data = data.resample(anfreq, label='right').agg(howagg)
    return data

#TODO:Fix `anfreq_label1` is purely for the benefit of UV-Seasonal Plot
def add_anfreq(plot_data, afreq_group):
    dt_idxname = plot_data.index.name
    data_dates = plot_data.index.to_frame().copy()
    err = None
    # Analysis Frequency Generation
    if afreq_group == 'W':
        # 'W'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("W").dt.start_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = data_dates[dt_idxname].apply(lambda x:'W'+str(x.week).zfill(2))
        plot_data['anfreq_label1'] = data_dates[dt_idxname].dt.day_name()
    elif afreq_group == 'MS':
        # 'MS'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("M").dt.start_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = plot_data['anfreq'].dt.month_name()
        plot_data['anfreq_label1'] = data_dates[dt_idxname].dt.day
    elif afreq_group == 'M':
        # 'M'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("M").dt.end_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = plot_data['anfreq'].dt.month_name()
        plot_data['anfreq_label1'] = data_dates[dt_idxname].dt.day
    elif afreq_group == 'QS':
        # 'QS'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("Q").dt.start_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = data_dates[dt_idxname].dt.to_period('Q').astype(str).str[4:]
        plot_data['anfreq_label1'] = (plot_data.index - pd.PeriodIndex(plot_data.index,freq='Q').start_time).days + 1
    elif afreq_group == 'Q':
        # 'Q'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("Q").dt.end_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = data_dates[dt_idxname].dt.to_period('Q').astype(str).str[4:]
        plot_data['anfreq_label1'] = (plot_data.index - pd.PeriodIndex(plot_data.index,freq='Q').start_time).days + 1
    elif afreq_group == 'AS':
        # 'AS'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("A").dt.start_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = data_dates[dt_idxname].dt.year
        plot_data['anfreq_label1'] = data_dates[dt_idxname].dt.dayofyear
    elif afreq_group == 'A':
        # 'A'
        plot_data['anfreq'] = data_dates[dt_idxname].dt.to_period("A").dt.end_time.astype('datetime64[D]')
        plot_data['anfreq_label'] = data_dates[dt_idxname].dt.year
        plot_data['anfreq_label1'] = data_dates[dt_idxname].dt.month_name()

    plot_data['hue_col'] = data_dates[dt_idxname].dt.to_period("A").dt.start_time.astype('datetime64[D]').dt.year

def get_freqgroup(_freqlabel):
    freq_group = _freqlabel
    for eftype in TS_FREQUENCIES:
        _match = re.compile(eftype).fullmatch(_freqlabel)
        if _match:
            # If it has multiplier
            _mult = re.search('\d+', _freqlabel)
            if _mult:
                freq_group = freq_group.replace(_mult.group(), '')
            # Split from -
            freq_group = freq_group.split('-')[0]
    return freq_group
