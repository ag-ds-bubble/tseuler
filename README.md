<img style="float: right;" src="examples/logo_big.png"  width='100%'>

# tseuler
A library for Time Series exploration, analysis & modelling. This includes -


As of now, this libray is in pre-alpha phase, i.e there is a lot of work still left before its first stable release. Current functionalties include :-

- A mini Dashboard for Time Series Analysis, with multiple variations to each kind of analysis
- Inherent Frequency adjustment & calculations

On later releases this library will include modelling approaches and analysis for:-

- In-Depth Automatic Analysis
- Intervention analysis
- Simple Modelling


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

`tseuler` has been built upon:-

- pandas
- numpy
- panel
- altair
- matplotlib
- statsmodels

<u>v0.0.1 : Original Package</u>
- Added TseulerBoard

