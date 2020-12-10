<img style="float: right;" src="examples/logo_big.png"  width='100%'>

# tseuler
A library for Time Series exploration, analysis & modelling. This includes -


As of now, this libray is in pre-alpha phase, i.e there is a lot of work still left before its first stable release.

### TSMAD - Time Series Mini Analysis DashBoard.
Functionalities Include

    - A mini Dashboard for Time Series Analysis, with multiple variations to each kind of analysis
    - Inbuilt Freqency Variation analysis
    - Intervention Analysis (In Future) 
    

### TSSTATS - Time Series Statistical & Modelling Functions
Functionalities Include:

    - Rolling Origin Framework (Currently Supports - statsmodels, sklearn, sklearn) for both multi-variate and uni-variate
    - Residual Diagnostics
    - Statistical Tests
    - Entropy Calculations
    - Intervention Analysis (In Future)

## Example
****
<img style="float: right;" src="examples/example_gif.gif"  width='100%'>

## Installation
****
Installation 
```py
pip install tseuler
```
## Usage
****
- ### Instantiating a DashBoard
    
    ```py
    import pandas as pd
    import tseuler as tse
    # Read the Time Series DataFrame
    dataDF = pd.read_csv('Raw Data/stocks_data.csv', index_col=0)
    tsmadObj = tse.TSMAD(tsdata = dataDF, data_desc = 'Stocks Data',
                     target_columns = ['close'], categorical_columns = ['Name'],
                     dt_format = '%Y-%m-%d', dt_freq = 'B',
                     how_aggregate = {'open':'first', 'high':'max', 'low':'min', 'close':'last'},
                     force_interactive = True)
    tsmadObj.get_board()
    ```

`tseuler` has been built upon:-
****
- pandas
- numpy
- panel
- altair
- matplotlib
- statsmodels



## History
****
<u>v0.0.4dev0 : Development Package</u>
- Added TSMAD
- Added TSSTATS
