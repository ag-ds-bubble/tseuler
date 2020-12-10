import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
from IPython.display import display
from warnings import filterwarnings

filterwarnings('ignore')

# https://github.com/facebook/prophet/issues/223#issuecomment-326455744
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)



def ro_framework(data, model, 
                 target_col, feature_cols,
                 test_start, cv_window, ahead_offest,
                 test_predict=False, test_roll=False,
                 model_params=None,
                 metric='MAPE', debug=True, ahead_offest_freq='days',back_transform_func=None):


    # Checks
    _tfreq = ['years', 'months', 'weeks', 'days', 'hours', 'minutes',
              'seconds', 'microseconds', 'nanoseconds']
    if not (hasattr(model, 'fit') & hasattr(model, 'predict')):
        raise ValueError("Model Passed should be having '.fit' & '.predict' methods, i.e foloowing the sklearn API")
    if data.shape[0]<10:
        raise ValueError("Data used for modelling should be greater than 10 datapoints")
    if type(data) != pd.core.frame.DataFrame:
        raise ValueError("Data should be a pandas dataframe of type 'pd.DataFrame'")
    if type(data.index) != pd.core.indexes.datetimes.DatetimeIndex:
        raise ValueError("Data should be having index of type 'pd.DatetimeIndex'")
    if not (type(test_start) == str or type(test_start) == pd._libs.tslibs.timestamps.Timestamp):
        raise ValueError("'test_start' should be a 'pd.Timestamp' or 'str'")
    if not (pd.to_datetime(test_start)>data.index[0] and pd.to_datetime(test_start)<data.index[-1]):
        raise ValueError("'test_start' should be in between {0} and {1}".format(data.index.min(),
                                                                                data.index.max()))
    if not type(ahead_offest) == pd._libs.tslibs.offsets.DateOffset:
        raise ValueError("'ahead_offest' should be a 'pd.DateOffset'")
    if type(cv_window) != int:
        raise ValueError("'cv_window' should be an `int`")
    if not any([ahead_offest_freq==k for k in _tfreq]):
        raise ValueError(f"'ahead_offest_freq' should be one of {_tfreq}")
    if getattr(ahead_offest, ahead_offest_freq) <= 0:
        raise ValueError(f"'ahead_offest' should be greater than `0 {ahead_offest_freq}`")
    if target_col not in data.columns:
        raise ValueError(f"{target_col} not found in `data`")
    if feature_cols:
        missing_feats = [k for k in feature_cols if k not in data.columns]
        if missing_feats:
            raise ValueError(f"{missing_feats} columns not present in the dataset")
    if data.index.freq == None:
        raise ValueError(f"data.index.freq should not be `None`")

    # Initialisations
    cvDF = pd.DataFrame(columns = ['Actual', 'Forecast', metric])
    testDF = pd.DataFrame(columns=['Actual', 'Forecast', metric])
    
    model = copy.deepcopy(model)
    
    modelling_data = data.copy()
    modelling_data.sort_index(inplace=True)

    training_data = data[data.index<test_start].copy()
    testing_data = data[data.index>=test_start].copy()

    train_start = training_data.index[0]
    
    test_start = pd.to_datetime(test_start)
    test_end = modelling_data.index[-1]
    
    if cv_window > training_data.shape[0]*0.5:
        raise ValueError("`cv_window` should be less than {}".format(int(training_data.shape[0]*0.5)))
    
    # Fore debugging purpose
    if debug:
        debugDF = pd.DataFrame(columns=['Train Start', 'Train End', 'CV Point', 'Diff'])
        for cv_date in training_data.index[-cv_window:]:
            train_end = cv_date-ahead_offest
            _packet = {'Train Start': train_start, 'Train End': train_end,
                       'CV Point': cv_date, 'Diff': str(getattr(ahead_offest, ahead_offest_freq))+' '+ahead_offest_freq}
            debugDF = debugDF.append(_packet, ignore_index=True)
        display(debugDF)
        return None
    
    
    # Picking the Metrics
    if metric == 'MAPE':
        metric_func = lambda y,yhat: np.round(abs((np.array(y)-np.array(yhat))/np.array(y))*100,2)
    elif metric == 'MSE':
        metric_func = lambda y,yhat: np.round((np.array(y)-np.array(yhat))**2,2)
    
    
    # Cross Validation Loop
    cvDF, fitted_model = _roll_loop_modelling(pred_indices = training_data.index[-cv_window:], data = training_data.copy(),
                                             train_start = train_start, feature_cols = feature_cols,
                                             target_col = target_col, ahead_offest = ahead_offest,
                                             metric_func = metric_func, modedf = cvDF, metric = metric,
                                             model = model, model_params = model_params, back_transform_func = back_transform_func)
    
    # Testing - Using the last fitted_model
    if test_predict:
        if test_roll:
            testDF, _ = _roll_loop_modelling(pred_indices = testing_data.index, data = modelling_data.copy(),
                                                        train_start = train_start, feature_cols = feature_cols,
                                                        target_col = target_col, ahead_offest = ahead_offest,
                                                        metric_func = metric_func, modedf = testDF, metric = metric,
                                                        model = model, model_params = model_params, _desc = 'Running Test Roll', back_transform_func = back_transform_func)
        else:
            testDF = _simple_modelling(data = testing_data, fitted_model=fitted_model,
                                      feature_cols=feature_cols, target_col=target_col,
                                      metric_func=metric_func, modedf=testDF, metric=metric,
                                      back_transform_func=back_transform_func, test_start=test_start, test_end=test_end)
    
    # Prepare Overall Metric
    overallDF = pd.DataFrame([cvDF[metric].mean(), testDF[metric].mean()],
                             columns=['Overall '+metric],
                             index=['CV', 'Test'])
    
    cvDF = cvDF.replace({np.inf:np.nan})
    testDF = testDF.replace({np.inf:np.nan})
    return cvDF, testDF, overallDF, fitted_model



def _roll_loop_modelling(pred_indices, data,
                        train_start, feature_cols,
                        target_col, ahead_offest,
                        metric_func, modedf, metric,
                        model, model_params, _desc = 'Running CV Roll', back_transform_func=None):
    
    for pred_date in tqdm(pred_indices, desc=_desc, leave=True):
        train_end = pred_date-ahead_offest
        # Filter the data
        _train_data = data.truncate(before=train_start, after=train_end)
        _pred_data = data.loc[pred_date].to_frame().T
        
        if feature_cols:
            # Multivariate
            if 'Prophet' in str(model):
                _prophet_model = model.get_pmodelinstance()
                _traindf =  _train_data.copy()
                _traindf = _traindf[[target_col]+feature_cols]
                _traindf.index.name = 'ds'
                _traindf.reset_index(inplace=True)
                _traindf.rename(columns={target_col:'y'}, inplace=True)

                # Make the forecasting dataframe
                _forecastdf =  _pred_data.copy()
                _forecastdf = _forecastdf[feature_cols]
                _forecastdf.index.name = 'ds'
                _forecastdf.reset_index(inplace=True)
                _forecastdf.rename(columns={target_col:'y'}, inplace=True)
                
                with suppress_stdout_stderr():
                    _fitted_model = _prophet_model.fit(_traindf)
                    _forecast = _prophet_model.predict(_forecastdf).yhat.values[0]
                _actual = _pred_data[target_col].values[0]
        else:
            # Univariate
            if 'statsmodels' in str(model):
                # Update Model Params Based on library
                model_params['endog'] = _train_data[target_col]
                modeldef = model(**model_params)
                
                _fitted_model = modeldef.fit()
                _forecast = _fitted_model.predict(start=pred_date, end=pred_date).values[0]
                _actual = _pred_data[target_col].values[0]
            elif 'Prophet' in str(model):
                # Make the training dataframe
                _prophet_model = model.get_pmodelinstance()
                _traindf =  _train_data.copy()
                _traindf.index.name = 'ds'
                _traindf.reset_index(inplace=True)
                _traindf.rename(columns={target_col:'y'}, inplace=True)
                
                # Make the forecasting dataframe
                _forecastdf = pd.DataFrame(columns=['ds'])
                _forecastdf['ds'] = [pred_date]
                with suppress_stdout_stderr():
                    _fitted_model = _prophet_model.fit(_traindf)
                    _forecast = _prophet_model.predict(_forecastdf).yhat.values[0]
                _actual = _pred_data[target_col].values[0]

        # Update Metric Sheets
        if back_transform_func:
            _actual = back_transform_func(_actual)
            _forecast = back_transform_func(_forecast)
            
        modedf.loc[pred_date, 'Actual'] = _actual
        modedf.loc[pred_date, 'Forecast'] = _forecast
        modedf.loc[pred_date,  metric] = metric_func(_actual, _forecast)

    return modedf, _fitted_model


def _simple_modelling(data, fitted_model, feature_cols,
                        target_col, metric_func, modedf, metric,
                        back_transform_func, test_start=None, test_end=None):
        
    if feature_cols:
        # Multivariate
        if 'Prophet' in str(fitted_model):
            # Make the forecasting dataframe
            _forecastdf =  data.copy()
            modedf['Actual'] = _forecastdf[target_col]
            _forecastdf = _forecastdf[feature_cols]
            _forecastdf.index.name = 'ds'
            _forecastdf.reset_index(inplace=True)
            with suppress_stdout_stderr():
                modedf['Forecast'] = fitted_model.predict(_forecastdf).yhat.values
    else:
        # Univariate
        if 'statsmodels' in str(fitted_model):
            modedf['Actual'] = data[target_col]
            modedf['Forecast'] = fitted_model.predict(start=test_start, end=test_end)
            modedf[metric] = modedf.apply(lambda x : metric_func(x.Actual, x.Forecast), axis=1)
        elif 'Prophet' in str(fitted_model):
            # Make the training dataframe
            _forecastdf =  data.copy()
            modedf['Actual'] = _forecastdf[target_col]
            _forecastdf.index.name = 'ds'
            _forecastdf.reset_index(inplace=True)
            _forecastdf = _forecastdf[['ds']].copy()
            modedf['Forecast'] = fitted_model.predict(_forecastdf).yhat.values

    # Update Metric Sheets
    if back_transform_func:
        modedf['Actual'] = back_transform_func(modedf['Actual'])
        modedf['Forecast'] = back_transform_func(modedf['Forecast'])
    modedf[metric] = modedf.apply(lambda x : metric_func(x.Actual, x.Forecast), axis=1)

    return modedf

