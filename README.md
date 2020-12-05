<img style="float: right;" src="tseuler/static/logo.png"  width='100%'>

# tseuler
A library for Time Series exploration, analysis & modelling. This includes -

- A mini Dashboard for Time Series Analysis, with multiple variations to each kind of analysis
- Inherent Frequency adjustment & calculations

## Example
****

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
    from tseuler import TseulerBoard
    # Read the Time Series DataFrame
    df = pd.read_csv('TimeSeriesdata3.csv', index_col=0)
    # Create a DashBoard!
    tb = TseulerBoard(tsdata=df, data_desc='Temperature Data',
                      target_column = ['AverageTemperature'],
                      categorical_columns = ['Country', 'City'])

    ```


## Versions
****
<u>v0.0.1 : Original Package</u>
- Added TseulerBoard

