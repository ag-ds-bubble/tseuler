# TODO : Fix for analysis frequency mangement
# TODO : Add methodology for imputation

# Relative Imports
from ._helpers import TS_FREQUENCIES, AVAILABLE_AGG_FUNC, TS_FORMATS
from ._panelview import PanelView

import re
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime

class TSMAD:
    def __init__(self, tsdata, data_desc : str = '',
                 target_columns : list = [],
                 categorical_columns : list = [],
                 dt_format : str = '%Y-%m-%d',
                 dt_freq : str = 'MS',
                 how_aggregate : str = 'mean',
                 force_interactive : bool = False):

        # Attributes
        self.usable_cols = []
        self.dropped_cols = []
        self.data_desc = data_desc

        # Sanity Checks
        sanity_packet = self._check_n_prep(tsdata.copy(), target_columns, categorical_columns,
                                           dt_format, dt_freq, how_aggregate, force_interactive)

        self.dt_freq = dt_freq
        self.dt_format = dt_format
        self.tsdata = sanity_packet[0]
        self.target_columns = sanity_packet[1]
        self.categorical_columns = sanity_packet[2]
        self.how_aggregate = sanity_packet[3]
        self.force_interactive = force_interactive

    def __add__(self, new_board):
        return NotImplemented

    def _check_n_prep(self, tsdata, target_columns, categorical_columns, dt_format,
                      dt_freq, how_aggregate, force_interactive):

        # Type Checks
        # Check for tsdata
        if not isinstance(tsdata, pd.core.frame.DataFrame):
            raise TypeError("`tsdata` should be a pandas dataframe, i.e of type `pd.core.frame.DataFrame`")
        # Check for target_columns
        if not isinstance(target_columns, list):
            raise TypeError(f"`target_columns` should be of type `list` even if there is one target column, target_columns={target_columns} does not conform to this.")
        # Check for categorical_columns
        if not isinstance(categorical_columns, list):
            raise TypeError(f"`categorical_columns` should be of type `list` even if there is one categorical column, categorical_columns={categorical_columns} does not conform to this.")
        # Check for dt_format
        if not isinstance(dt_format, str):
            raise TypeError(f"`dt_format` should be of type `str`, dt_format={dt_format} does not conform to this.")
        # Chcek for dt_freq
        if not isinstance(dt_freq, str):
            raise TypeError(f"`dt_freq` should be of type `str`, dt_freq={dt_freq} does not conform to this.")
        # Check for how_aggregate <- string or dictionary mapping the values for plotting columns
        if not any([isinstance(how_aggregate, str), isinstance(how_aggregate, dict)]):
            raise TypeError(f"`how_aggregate` should be of type `str` or `dict`, how_aggregate={how_aggregate} does not conform to this.")
        # Check for force_interactive
        if not isinstance(force_interactive, bool):
            raise TypeError(f"`force_interactive` should be of type `bool`, force_interactive={force_interactive} does not conform to this.")
        
        # Value Checks
        # Check for dt_format
        if not (dt_format in TS_FORMATS):
            raise ValueError(f"`dt_format` should be of one of {TS_FORMATS}, dt_format={TS_FORMATS} does not conform to this.")
        # Check for dt_freq & get frequency group
        _dtfreq_regex_compile = [re.compile(eftype).fullmatch(dt_freq)!=None for eftype in TS_FREQUENCIES]
        if sum(_dtfreq_regex_compile)!=1:
            raise ValueError(f"`dt_freq` should match one of {TS_FREQUENCIES} regex, dt_freq={dt_freq} does not conform to this.")
        if sum(_dtfreq_regex_compile[:6])==1:
            if dt_format != '%Y-%m-%d HH:MM:SS':
                raise ValueError(f"For dt_freq={dt_freq}, 'dt_format' should be '%Y-%m-%d HH:MM:SS'")
        elif sum(_dtfreq_regex_compile[6:])==1:
            if dt_format != '%Y-%m-%d':
                raise ValueError(f"For dt_freq={dt_freq}, 'dt_format' should be '%Y-%m-%d'")
        
        # Check for Data Description
        if not isinstance(self.data_desc, str):
            raise ValueError(f"'data_desc' should be of type 'str'")
        # Checks for tsdata
        if tsdata.empty:
            raise ValueError(f"'tsdata' should not be an empty DataFrame")
        
        if type(tsdata.index)==pd.core.indexes.datetimes.DatetimeIndex:
            pass
        elif type(tsdata.index)==pd.core.indexes.base.Index:
            for edt in np.random.choice(tsdata.index, int(tsdata.shape[0]*0.01)):
                try:
                    _ = datetime.strptime(edt, dt_format)
                except:
                    raise ValueError(f"{edt} is not parsable in the {dt_format}.")
                tsdata.index = pd.to_datetime(tsdata.index, format=dt_format)
        else:
            raise ValueError(f"`tsdata` index should be eitherof type pandas.DatetimeIndex or Index.")

        if not set(target_columns).issubset(set(tsdata.columns.tolist())):
            raise ValueError(f"{target_columns} not present in the 'tsdata'")
        # Sanity check for categorical columns
        if not set(categorical_columns).issubset(set(tsdata.columns.tolist())):
            raise ValueError(f"{categorical_columns} not present in the 'tsdata'")
        elif categorical_columns != []:
            for eachCatCol in categorical_columns:
                tsdata[eachCatCol] = tsdata[eachCatCol].astype('category')
            
        # Usable and Unusable columns
        self.usable_cols = [e for e in tsdata.columns if any(a in tsdata[e].dtype.__str__() for a in  ['int', 'float', 'category'])]
        self.plot_cols = [e for e in tsdata.columns if any(a in tsdata[e].dtype.__str__() for a in  ['int', 'float'])]
        self.dropped_cols = [e for e in tsdata.columns if e not in self.usable_cols]
        tsdata = tsdata[self.usable_cols]

        # If there is no 'int' or 'float' category column left, raise error
        _intcols = 0
        _floatcols = 0
        for ecol in tsdata.columns:
            if 'int' in tsdata[ecol].dtype.__str__():
                _intcols += 1
            elif 'float' in tsdata[ecol].dtype.__str__():
                _floatcols += 1
        if not any([_floatcols>0, _intcols>0]):
            raise ValueError(f"`tsdata` has no `int` or `float` cloumns left to plot")

        # Sanity check for how_aggregate
        if isinstance(how_aggregate, str):
            if how_aggregate not in AVAILABLE_AGG_FUNC:
                raise ValueError(f"For type(how_aggregate)==str , `how_aggregate` parameter should be one of {AVAILABLE_AGG_FUNC}")
        elif isinstance(how_aggregate, dict):
            _keys = list(how_aggregate.keys())
            _vals = list(how_aggregate.values())
            if not set(_keys).issubset(set(tsdata.columns.tolist())):
                raise ValueError(f"For type(how_aggregate)==dict , `how_aggregate` parameter's keys should be be one of {_keys}")
            if not any(_eval in AVAILABLE_AGG_FUNC for _eval in _vals):
                raise ValueError(f"For type(how_aggregate)==dict , `how_aggregate` parameter's values should be one of {AVAILABLE_AGG_FUNC}")
            _missed_plot_cols = list(set(self.plot_cols).difference(set(_keys)))
            for _mpc in _missed_plot_cols:
                how_aggregate[_mpc] = 'mean'
        
        # Check if the data conforms to the following dt_freq
        if categorical_columns:
            for egid, eg in tsdata.groupby(categorical_columns):
                if pd.infer_freq(eg.index) != dt_freq:
                    _resp = ''
                    for eccol in categorical_columns:
                        if len(eg[eccol].unique()) > 1 : raise ValueError("Wrong Grouping, Check!")
                        _resp+=eccol+'('+str(eg[eccol].unique()[0])+')'+'→'
                    raise ValueError(f"Dataframe with filter of '{_resp[:-1]}' does not have datetime index conforming to freq={dt_freq}")
        else:
            if pd.infer_freq(tsdata.index) != dt_freq:
                raise ValueError(f"DateTime index for does not have datetime index conforming to freq={dt_freq}")
        
        return tsdata, target_columns, categorical_columns, how_aggregate

    def get_board(self):
        # Sends the board whose elements have been pre-attached
        self.dash_panel =  PanelView(data = self.tsdata, datadesc = self.data_desc, dt_freq = self.dt_freq,
                                     dt_format = self.dt_format, how_aggregate = self.how_aggregate,
                                     catcols = self.categorical_columns, targetcols = self.target_columns,
                                     force_interactive = self.force_interactive)
        return self.dash_panel.view.servable()


TSMAD.__doc__ = """
    TSMAD - Time Series Mini Analysis Dashboard
    -----------------------------------
    A Dashboard for Univariate, Bivariate and Trivariate analysis
    for the Time Series Datasets. 

    Parameters
    ----------
    tsdata : pandas.dataframe
        Pandas DataFrame with DateTime index, in Long(Narrow) 
        Format - https://en.wikipedia.org/wiki/Wide_and_narrow_data
        or string index parsable to dates, via calling pd.to_datetime()
        function on the `tsdata` index. Make sure that the frequency of 
        the datetime index conforms to the index time frequency as 
        specified in the `dt_freq` parameter.

        As of v0.0.1 only float, categorical, object columns are allowed to be 
        in the dataframe, if there are more those columns will be dropped.

    data_desc : str, optional
        Description of the dataset.

    target_columns : list, optional
        A list of target columns, can be one can be more than one.
        A target column is required to do Bivariate analysis and above.

    categorical_columns : list, optional
        A list of categorical columns to filter from, these must be in,
        'DEPTH ORDER'. DEPTH ORDER - here refers to those multiple categorical
        columns which are required for filtering of the dataset in a sequiential
        manner, for ex : for a dataset like this:
        
        INDEX           TEMPERATURE      COUNTRY       CITY
        ------------------------------------------------------
        2000-01-01   |      40        |  India     | New Delhi
        2000-01-02   |      42        |  India     | New Delhi
        2000-01-03   |      41        |  India     | New Delhi
        2000-01-04   |      43        |  India     | New Delhi
        ...
        ...
        2000-05-03   |      41        |  China     | Beijing
        2000-05-04   |      43        |  China     | Beijing

        categorical_columns parameter should be = ['COUNTRY', 'CITY'],
        which implies that 'COUNTRY' & 'CITY' columns are categorical filters
        for the dataset and ALSO, they have been ordered in depth 
        i.e Country -> City.

    dt_format : str, optional
        Format of the DatetimeIndex of the `tsdata` dataframe, should be one of,
            - %Y-%m-%d
            - %Y-%m-%d HH:MM:SS

    dt_freq : str, optional
        Frequency of the `tsdata` DatetimeIndex, it should be one of the pandas
        acceptable offset aliases - 
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

    how_aggregate : str or dict, optional
        While changing the freqeuncy of the dataset to analyse say Monthly, Quarterly,
        Yearly etc.., a aggregation function need to be performed.

        This parameter can be a `str` or a `dict`.
        If this parameter is passed as a `str` and is one of 
            - ['sum', 'mean', 'median', 'std', 'var', 'last', 'first', 'min', 'max']
        then that particular aggregation is applied to all the available columns.

        If the parameter passed is of type `dict` then the keys should columns names
        and the value against each should be the aggregation that needs to be applied.
        If aggregate functions for some of he plotting columns are not give, then `mean`
        is assumed for them by default.

        For example, for a stock datasets which have the columns of Open, High, Low & Close
        `how_aggregate` parameter can look something like this.
            - {'Open' : 'first', 'High':'max', 'Low':'min', 'Close':'last'}

    force_interactive : bool, optional
        Wether to force the plots to be interactive i.e `altair` based or not.

    Methods
    -------
    get_board
    
    Notes
    -----
    To create a new tseuler Dashboard :
    import pandas as pd
    import tseuler import as tmd

    df = pd.read_csv('TimeSeriesdata-MS.csv', index_col=0)
    tb = tmd.TSMAD(tsdata=df, data_desc='Temperature Data',
                target_columns = ['AverageTemperature'],
                categorical_columns = ['Country', 'City'],
                dt_format='%Y-%m-%d', dt_freq='MS')
    """
