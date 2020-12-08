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

TSMAD_CONFIGS = {'plotting.default_engine' : 'Interactive',
                 'plotting.uv.ma_window' : 0.01,
                 'plotting.uv.exp_span' : 0.01,
                 'plotting.uv.fcomp_factor' : 0.01,}


TS_FREQUENCIES = [r'S', r'T', r'H',
                  r'\d+S$', r'\d+T$', r'\d+H$',
                  
                  r'D', r'B',
                  r'\d+D$', r'\d+B$',
                  
                  r'MS', r'M',
                  r'\d+MS$', r'\d+M$',
                  
                  r'W-MON',r'W-TUE',r'W-WED',r'W-THU',r'W-FRI',r'W-SAT',r'W-SUN',
                  r'\d+W-MON$',r'\d+W-TUE$',r'\d+W-WED$',r'\d+W-THU$',r'\d+W-FRI$',r'\d+W-SAT$',r'\d+W-SUN$',

                  r'QS-JAN', r'QS-FEB', r'QS-MAR', r'QS-APR', r'QS-MAY', r'QS-JUN', r'QS-JUL', r'QS-AUG', r'QS-SEP', r'QS-OCT', r'QS-NOV', r'QS-DEC',
                  r'\d+QS-JAN$', r'\d+QS-FEB$', r'\d+QS-MAR$', r'\d+QS-APR$', r'\d+QS-MAY$', r'\d+QS-JUN$', r'\d+QS-JUL$', r'\d+QS-AUG$', r'\d+QS-SEP$', r'\d+QS-OCT$', r'\d+QS-NOV$', r'\d+QS-DEC$',
                  
                  r'Q-JAN', r'Q-FEB', r'Q-MAR', r'Q-APR', r'Q-MAY', r'Q-JUN', r'Q-JUL', r'Q-AUG', r'Q-SEP', r'Q-OCT', r'Q-NOV', r'Q-DEC',
                  r'\d+Q-JAN$', r'\d+Q-FEB$', r'\d+Q-MAR$', r'\d+Q-APR$', r'\d+Q-MAY$', r'\d+Q-JUN$', r'\d+Q-JUL$', r'\d+Q-AUG$', r'\d+Q-SEP$', r'\d+Q-OCT$', r'\d+Q-NOV$', r'\d+Q-DEC$',
                  
                  r'AS-JAN', r'AS-FEB', r'AS-MAR', r'AS-APR', r'AS-MAY', r'AS-JUN', r'AS-JUL', r'AS-AUG', r'AS-SEP', r'AS-OCT', r'AS-NOV', r'AS-DEC',
                  r'\d+AS-JAN$', r'\d+AS-FEB$', r'\d+AS-MAR$', r'\d+AS-APR$', r'\d+AS-MAY$', r'\d+AS-JUN$', r'\d+AS-JUL$', r'\d+AS-AUG$', r'\d+AS-SEP$', r'\d+AS-OCT$', r'\d+AS-NOV$', r'\d+AS-DEC$',
                  
                  r'A-JAN', r'A-FEB', r'A-MAR', r'A-APR', r'A-MAY', r'A-JUN', r'A-JUL', r'A-AUG', r'A-SEP', r'A-OCT', r'A-NOV', r'A-DEC',
                  r'\d+A-JAN$', r'\d+A-FEB$', r'\d+A-MAR$', r'\d+A-APR$', r'\d+A-MAY$', r'\d+A-JUN$', r'\d+A-JUL$', r'\d+A-AUG$', r'\d+A-SEP$', r'\d+A-OCT$', r'\d+A-NOV$', r'\d+A-DEC$']

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


