# TODO : Fix for analysis frequency mangement

# Relative Imports
from ._helpers import TS_FREQUENCIES, AVAILABLE_AGG_FUNC
from ._panelview import PanelView

import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm

class TSMAD:
    """
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
        
        INDEX            TEMPERATURE     COUNTRY     CITY
        ------------------------------------------------------
        2000-01-01   |      40        |  India     | New Delhi
        2000-01-02   |      42        |  India     | New Delhi
        2000-01-03   |      41        |  India     | New Delhi
        2000-01-04   |      43        |  India     | New Delhi
        ...
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
            - '%Y-%m-%d'
            - %Y-%m-%d HH:MM:SS'

    dt_freq : str, optional
        Frequency of the `tsdata` DatetimeIndex, it should be one of the pandas
        acceptable offset aliases - 
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

    freq_conv_agg : str, optional
        While analysing various frequencies of the dataset, say Monthly, Quarterly, Yearly etc..
        One or the other of these operations need to be performed to transform the
        dataframe, this parameter effectively translates to :-
            - 'sum' : tsdata.groupby(categorical_columns).agg('sum')
            - 'mean' : tsdata.groupby(categorical_columns).agg('mean')
            - 'median' : tsdata.groupby(categorical_columns).agg('median')
            - 'std' : tsdata.groupby(categorical_columns).agg('std')
            - 'var' : tsdata.groupby(categorical_columns).agg('var')
            - 'last' : tsdata.groupby(categorical_columns).agg('last')
            - 'first' : tsdata.groupby(categorical_columns).agg('first')
            - 'min' : tsdata.groupby(categorical_columns).agg('min')
            - 'max' : tsdata.groupby(categorical_columns).agg('max')

    force_interactive : bool, optional
        Wether to force the plots to be interactive

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
    def __init__(self, tsdata, data_desc : str = '',
                 target_columns : list = [],
                 categorical_columns : list = [],
                 dt_format : str = '%Y-%m-%d',
                 dt_freq : str = 'MS',
                 freq_conv_agg : str = 'mean',
                 force_interactive : bool = False):

        # Attributes
        self.usable_cols = []
        self.dropped_cols = []
        self.data_desc = data_desc

        # Sanity Checks
        sanity_packet = self._check_n_prep(tsdata.copy(), target_columns, categorical_columns,
                                           dt_format, dt_freq, freq_conv_agg, force_interactive)

        self.tsdata = sanity_packet[0]
        self.target_columns = sanity_packet[1]
        self.categorical_columns = sanity_packet[2]
        self.freq_conv_agg = sanity_packet[3]
        self.dt_freq = dt_freq
        self.dt_format = dt_format
        self.force_interactive = force_interactive

    def __add__(self, new_board):
        return NotImplemented

    def _check_n_prep(self, tsdata, target_columns, categorical_columns, dt_format,
                      dt_freq, freq_conv_agg, force_interactive):

        # Check if the dataframe sent is empty
        assert not tsdata.empty, "'tsdata' DataFrame can not be an empty pandas dataframe"
        if not isinstance(force_interactive, bool):
            raise ValueError("'force_interactive' parameter should be of type `bool`")
        # Check if the dt_format is date parsable
        # Frequency and Available Analysis Freqency
        if dt_freq not in TS_FREQUENCIES:
            raise ValueError(f"'dt_freq' should be one of {TS_FREQUENCIES}, if not convert the data to one of these pandas offset aliases")
        if dt_freq in TS_FREQUENCIES[:3]:
            if dt_format != '%Y-%m-%d HH:MM:SS':
                raise ValueError(f"For {dt_freq}, 'dt_format' should be '%Y-%m-%d HH:MM:SS'")
        else:
            if dt_format != '%Y-%m-%d':
                raise ValueError(f"For {dt_freq}, 'dt_format' should be '%Y-%m-%d'")
        # - Randomly sample 1% index from the dataframe and check if the format holds
        if type(tsdata.index)==pd.core.indexes.datetimes.DatetimeIndex:
            pass
        elif type(tsdata.index)==pd.core.indexes.base.Index:
            for edt in np.random.choice(tsdata.index, int(tsdata.shape[0]*0.01)):
                try:
                    _ = datetime.strptime(edt, dt_format)
                except:
                    raise ValueError(f"{edt} is not parsable in the {dt_format}.")
        else:
            raise ValueError(f"`tsdata` index should be eitherof type pandas.DatetimeIndex or Index.")

        # Check if the index is not datetime parsable
        try:
            tsdata.index = pd.to_datetime(tsdata.index, format=dt_format)
            tsdata = tsdata.sort_index()
        except:
            raise Exception("Unable to convert the 'tsdata' index to datetime\nCheck if the data has index which is parsable to datetime format")

        # Sanity check for target columns
        if not isinstance(target_columns, list):
            raise ValueError("'target_columns' should be of type 'list'")
        if not set(target_columns).issubset(set(tsdata.columns.tolist())):
            raise ValueError(f"{target_columns} not present in the 'tsdata'")
        # Sanity check for categorical columns
        if not isinstance(categorical_columns, list):
            raise ValueError("'categorical_columns' should be of type 'list'")
        if not set(categorical_columns).issubset(set(tsdata.columns.tolist())):
            raise ValueError(f"{categorical_columns} not present in the 'tsdata'")
        elif categorical_columns != []:
            for eachCatCol in categorical_columns:
                tsdata[eachCatCol] = tsdata[eachCatCol].astype('category')
        
        # Sanity check for freq_conv_agg
        if freq_conv_agg not in AVAILABLE_AGG_FUNC:
            raise ValueError(f"'freq_conv_agg' should be one of {AVAILABLE_AGG_FUNC}")
        
        # Sanity check for freq_conv_agg
        if not isinstance(self.data_desc, str):
            raise ValueError(f"'data_desc' should be of type 'str'")

        # Usable and Unusable columns
        self.usable_cols = [e for e in tsdata.columns if any(a in tsdata[e].dtype.__str__() for a in  ['int', 'float', 'category'])]
        self.dropped_cols = [e for e in tsdata.columns if e not in self.usable_cols]
        tsdata = tsdata[self.usable_cols]

        # Check if the data conforms to the following dt_freq
        if categorical_columns:
            for egid, eg in tsdata.groupby(categorical_columns):
                match1 = pd.infer_freq(eg.index) == dt_freq
                match2 = 'W' in pd.infer_freq(eg.index)
                match3 = 'Q' in pd.infer_freq(eg.index)
                if not any([match1, match2, match3]):
                    _resp = ''
                    for eccol in categorical_columns:
                        if len(eg[eccol].unique()) > 1 : raise ValueError("Wrong Grouping, Check!")
                        _resp+=eccol+'('+str(eg[eccol].unique()[0])+')'+'→'
                    raise ValueError(f"Dataframe with filter of '{_resp[:-1]}' does not have date_range frequency conforming to freq={dt_freq}")
        else:
            match1 = pd.infer_freq(tsdata.index) == dt_freq
            match2 = 'W' in pd.infer_freq(tsdata.index)
            match3 = 'Q' in pd.infer_freq(tsdata.index)
            if not any([match1, match2, match3]):
                raise ValueError(f"DateTime index for does not have date_range frequency conforming to freq={dt_freq}")

        return tsdata, target_columns, categorical_columns, freq_conv_agg

    def get_board(self):
        # Sends the board whose elements have been pre-attached
        self.dash_panel =  PanelView(data = self.tsdata, datadesc = self.data_desc,
                                     dt_freq = self.dt_freq, dt_format = self.dt_format, freq_conv_agg = self.freq_conv_agg,
                                     catcols = self.categorical_columns, targetcols = self.target_columns, force_interactive = self.force_interactive)
        return self.dash_panel.view.servable()

