TSEULER_PANEL_DESCRIPTORS = {'logo_description':'''<b>T</b>ime <b>S</b>eries : <b>M</b>ini <b>A</b>nalysis <b>D</b>ashboard.
<br></br>A mini-dashboard for Time Series Analysis ->
Uni-Variate, Bi-Variate & Multi-Variate on just click of a button!'''}


TS_UV_PLOTS = ['Line Plot : Overtime Analysis',
                'Area Chart : Overtime Analysis',
                'Box Plot : Variation Analysis',
                'Ridge Plot : Distribution Analysis',
                'Seasonal Plot : Variation Analysis',
                'Histogram : Distribution Analysis',
                'ACF Plot : Relation Analysis',
                'PACF Plot : Relation Analysis',
                'Q-Q Plot : Distribution Analysis',
                'Moving Average : Series Smoothing',
                'Simple Exponential : Series Smoothing',
                'Fourier : Series Smoothing']
    
TS_BV_PLOTS = ['Line Plot : Overtime Analysis',
               'Area Plot : Overtime Analysis',
               'Violin Plot : Distribution Analysis',
               'Scatter Plot : Relation Analysis',
               'Reg Plot : Relation Analysis',
               'KDE Plot : Relation Analysis',
               'Joint Plot : Relation Analysis']

TS_TV_PLOTS = ['Linked Scatter Plot : Relation Analysis']

TSEULER_CONFIGS = {'plotting.default_engine' : 'Interactive',
                 'plotting.uv.ma_window' : 0.01,
                 'plotting.uv.exp_span' : 0.01,
                 'plotting.uv.fcomp_factor' : 0.01,}


TS_FREQUENCIES = ['S', 'T', 'H', 
                  'D', 'B',
                  'W',
                  'MS', 'M',
                  'QS', 'Q',
                  'AS', 'A']

TS_FREQUENCIES_DESC = {'S': 'Seconds',
                        'T': 'Minutely',
                        'H': 'Hourly',
                        'D': 'Daily',
                        'B': 'Buisness Days',
                        'W': 'Weeks',
                        'MS': 'Month Start',
                        'M': 'Month End',
                        'QS': 'Quarter Start',
                        'Q': 'Quarter End',
                        'AS': 'Year Start',
                        'A': 'Year End'}

TS_FORMATS = ['%Y-%m-%d', '%Y-%m-%d HH:MM:SS']

TS_FREQ_MAP =  {'S' : ['T', 'H', 'D', 'B', 'W', 'MS', 'M', 'QS', 'Q', 'AS', 'A'],
                'T' : ['H', 'D', 'B', 'W', 'MS', 'M', 'QS', 'Q', 'AS', 'A'],
                'H' : ['D', 'B', 'W', 'MS', 'M', 'QS', 'Q', 'AS', 'A'],

                'D' : ['W', 'MS', 'M', 'QS', 'Q', 'AS', 'A'],
                'B' : ['W', 'MS', 'M', 'QS', 'Q', 'AS', 'A'],
                'W' : ['MS', 'M', 'QS', 'Q', 'AS', 'A'],
                'MS' : ['QS', 'Q', 'AS', 'A'],
                'M' : ['QS', 'Q', 'AS', 'A'],
                'QS' : ['AS', 'A'],
                'Q' : ['AS', 'A'],
                'AS' : [],
                'A' : []}

AVAILABLE_AGG_FUNC = ['sum', 'mean', 'median',  'std', 'var',
                      'last', 'first', 'min', 'max']


