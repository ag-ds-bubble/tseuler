<img style="float: right;" src="tseuler/static/logo.png"  width='100%'>

# ts-mad
Time Series - Mini Analysis Dashboard

<installation>
<usage>
<gif : workflow>
<different charts>

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
    from tseuler import TsBoard
    # Read the Time Series DataFrame
    df = pd.read_csv('TimeSeriesdata3.csv', index_col=0)
    # Create a DashBoard!
    tb = TsBoard(tsdata=df, data_desc='Temperature Data',
                 target_column = ['AverageTemperature'],
                 categorical_columns = ['Country', 'City'])

    ```
    <image example>
    ****


## Versions
****
<u>v1.0.0 : Original Package</u>
- Add UV, BV and TV plots

