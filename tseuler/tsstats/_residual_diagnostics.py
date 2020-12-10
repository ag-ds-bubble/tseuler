import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
from statsmodels.graphics.tsaplots import plot_acf

def residual_diagnostic(respack, training_target):

    tsdata = training_target.copy().to_frame()
    cvdf, testdf, odf, _ = respack
    cvdf, testdf, odf = cvdf.copy(), testdf.copy(), odf.copy()

    cvdf['Residuals'] = cvdf['Actual']-cvdf['Forecast']
    testdf['Residuals'] = testdf['Actual']-testdf['Forecast']
    
    fig = plt.figure(figsize=(15,15))
    _rows = 6
    if testdf.empty:
        _rows = 4
    grid = plt.GridSpec(_rows, 3, figure=fig, wspace=0.2, hspace=0.5)
    plt.grid()
    
    # Time Series Plot
    ts_axes = plt.subplot(grid[:2,:])
    ts_axes.plot(tsdata, label='Actual')
    ts_axes.plot(cvdf.Forecast, color='#aa8ede', label='CV Preidictions')

    if not testdf.empty:
        ts_axes.plot(testdf.Actual, color='#314d2c', label='Test Actual', linestyle=':')
        ts_axes.plot(testdf.Forecast, color='#fab09b', label='Test Forecast', linewidth=3)
        _err = testdf.Forecast.expanding().std()*1.96
        ts_axes.fill_between(testdf.index,
                            testdf.Forecast+_err,
                            testdf.Forecast-_err, alpha=0.3,
                            color='lightgray', label='Prediction Interval')
    ts_axes.legend()
    ts_axes.set_title('Actual Series + CV Predictions + Test Forecasts', loc='left')
    
    # Cross Validation Diagnostics
    cvtse_axes = plt.subplot(grid[2,:])
    cvdis_axes = plt.subplot(grid[3,0])
    cvqqp_axes = plt.subplot(grid[3,1])
    cvacf_axes = plt.subplot(grid[3,2])
    
    cvtse_axes.plot(cvdf.Residuals)
    sns.distplot(cvdf['Residuals'], ax=cvdis_axes, rug=True, rug_kws={'color':'r'})
    qqplot(cvdf['Residuals'], ax=cvqqp_axes, color='w')
    plot_acf(cvdf['Residuals'], ax=cvacf_axes, title='')

    cvtse_axes.set_title('Cross Validation - {0} - {1}'.format(odf.columns[0], round(odf.loc['CV', odf.columns[0]]),3), loc='left')
    cvtse_axes.set_ylabel('Residuals')
    cvdis_axes.set_title('Cross Validation - Distribution', loc='left')
    cvqqp_axes.set_title('Cross Validation - QQ', loc='left')
    cvacf_axes.set_title('Cross Validation - ACF', loc='left')
    
    
    # Test Diagnostics
    if not testdf.empty:
        tetse_axes = plt.subplot(grid[4,:])
        tedis_axes = plt.subplot(grid[5,0])
        teqqp_axes = plt.subplot(grid[5,1])
        teacf_axes = plt.subplot(grid[5,2])
        
        tetse_axes.plot(testdf.Residuals)
        sns.distplot(testdf['Residuals'], ax=tedis_axes, rug=True, rug_kws={'color':'r'})
        qqplot(testdf['Residuals'], ax=teqqp_axes, color='w')
        plot_acf(testdf['Residuals'], ax=teacf_axes, title='')

        tetse_axes.set_title('Test - {0} - {1}'.format(odf.columns[0], round(odf.loc['Test', odf.columns[0]]),3), loc='left')
        tetse_axes.set_ylabel('Residuals')
        tedis_axes.set_title('Test - Distribution', loc='left')
        teqqp_axes.set_title('Test - QQ', loc='left')
        teacf_axes.set_title('Test - ACF', loc='left')
    
    
    fig.suptitle('Model \nDiagnostic', fontsize=25)
    return fig



