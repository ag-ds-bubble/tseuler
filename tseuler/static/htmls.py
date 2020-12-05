dtype_summary_table = '''<table>
    <tbody>
        <tr>
            <td style="color:{0}; padding : 0px 10px;"><b>Category</b></td>
            <td style = "color:{1};">{2}%</td>
        </tr>
        <tr>
            <td style="color:{0}; padding : 0px 10px;"><b>Integer</b></td>
            <td style = "color:{3};">{4}%</td>
        </tr>
        <tr>
            <td style="color:{0}; padding : 0px 10px;"><b>Float</b></td>
            <td style = "color:{5};">{6}%</td>
        </tr>
    </tbody>
</table>'''


nan_summary_table = '''<table>
    <tbody>
        <tr>
            <td style="color:{0}; padding : 0px 10px;"><b>{1}</b></td>
            <td style = "color:{2};">{3}%</td>
        </tr>
        <tr>
            <td style="color:{0}; padding : 0px 10px;"><b>{4}</b></td>
            <td style = "color:{5};">{6}%</td>
        </tr>
        <tr>
            <td style="color:{0}; padding : 0px 10px;"><b>{7}</b></td>
            <td style = "color:{8};">{9}%</td>
        </tr>
    </tbody>
</table>
<p style="color:blue;margin-left: 50px;">...more</p>'''


stats_css = '''
.stats_css {
    border-radius: 2px;
    border-collapse: collapse;
    margin: 2px 2px;
    font-size: 0.9em;
    width:90%;
    font-family: sans-serif;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.stats_css thead tr {
    background-color: #009879;
    color: #ffffff;
}

.stats_css th,
.stats_css td {
    padding:15px 15px 0 0;
}

.stats_css tbody tr {
    border-bottom: 1px solid #dddddd;
}

.stats_css tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}

.stats_css tbody tr:last-of-type {
    border-bottom: 1px solid #009879;
}
'''


corr_css = """
.corr_css body {
  font-family: Arial, sans-serif;
  font-weight: 1;
  line-height: .1em;
  color:#A7A1AE;
  background-color:#1F2739;
}

.corr_css h1 {
  font-size:1em; 
  font-weight: 300;
  line-height:1em;
  text-align: center;
  color: #4DC3FA;
}


.corr_css h2 a {
  font-weight: 700;
  text-transform: uppercase;
  color: #FB667A;
  text-decoration: none;
}

.corr_css .blue { color: #185875; }
.corr_css .yellow { color: #FFF842; }

.corr_css th h1 {
      font-weight: bold;
      font-size: 1em;
  text-align: center;
  color: #afb9c9;
}

.corr_css td:first-child { 
        color: #afb9c9; 
        background-color: #1F2739;
        font-weight: bold;}

.corr_css tr:nth-child(odd) {
      background-color: #ccdced;
}

.corr_css tr:nth-child(even) {
      background-color: #8497b5;
}

.corr_css th {
      background-color: #1F2739;
}

.corr_css {width: 90%;}

.corr_css td, .corr_css th {
      padding-bottom: 2%;
      padding-top: 2%;
  padding-left: 2%;  
}

.corr_css tr:hover {
   background-color: #ebeef2;
-webkit-box-shadow: 0 6px 6px -6px #0E1119;
       -moz-box-shadow: 0 6px 6px -6px #0E1119;
            box-shadow: 0 6px 6px -6px #0E1119;
}

.corr_css td:hover {
  background-color: #FFF842;
  color: #403E10;
  font-weight: bold;
  
  box-shadow: #7F7C21 -1px 1px, #7F7C21 -2px 2px, #7F7C21 -3px 3px, #7F7C21 -4px 4px, #7F7C21 -5px 5px, #7F7C21 -6px 6px;
  transform: translate3d(6px, -6px, 0);
  
  transition-delay: 0s;
      transition-duration: 0.4s;
      transition-property: all;
  transition-timing-function: line;
}

@media (max-width: 300) {
.corr_css td:nth-child(4),
.corr_css th:nth-child(4) { display: none; }
}
"""

table_html_1 = """
<b>Summary Table</b>
<br>This table reflects the Statistics of the Time Series being analysed.</br><br>
<p>From Missing values and +ive and -ive values to the key statistics pertaining to
a Time Series, including <i>Augmented-Dickey Fuller</i> Test,  <i>Kwiatkowski–Phillips–Schmidt–Shin</i> Test
and Entropy Values.</p><br>
<table class="stats_css">
    <thead >
        <tr>
            <th>Property</th>
            <th>Value</th>
            <th>Property</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td># Nan</td>
            <td style="color:{0}; font-size:.9em;">{1} ({2}%)</td>
            <td># 0's</td>
            <td style="color:{3}; font-size:.9em;">{4} ({5}%)</td>
        </tr>
        <tr>
            <td># +ive's</td>
            <td style="color:{6}; font-size:.9em;">{7} ({8}%)</td>
            <td># -ive's</td>
            <td style="color:{9}; font-size:.9em;">{10} ({11}%)</td>
        </tr>
        <tr>
            <td>count</td>
            <td>{12}</td>
            <td>mean</td>
            <td>{13}</td>
        </tr>
        <tr>
            <td>std</td>
            <td>{14}</td>
            <td>min</td>
            <td>{15}</td>
        </tr>
        <tr>
            <td>25%</td>
            <td>{16}</td>
            <td>50%</td>
            <td>{17}</td>
        </tr>
        <tr>
            <td>75%</td>
            <td>{18}</td>
            <td>max</td>
            <td>{19}</td>
        </tr>
        <tr>
            <td>ADF Stationarity</td>
            <td>{20}</td>
            <td>ADF p-value</td>
            <td>{21}</td>
        </tr>
        <tr>
            <td>KPSS Stationarity</td>
            <td>{22}</td>
            <td>KPSS p-value</td>
            <td>{23}</td>
        </tr>
        <tr>
            <td>Approximate Entropy</td>
            <td>{24}</td>
            <td>Sample Entropy</td>
            <td>{25}</td>
        </tr>
    </tbody>
</table>"""



table_html_2 = """
<br><b>Correlation Table</b></br><br>
<br>This table reflects the Correlation value of the Time Series target vs a Variable.</br><br>
<p>The correlation values between the two time-series can be either <i>Pearson Correlation</i>,
<i>Spearman Correlation</i> or <i>Kendall Correlation</i>, this is a setting that can be changed
in the configurations.</p><br>
<table class="corr_css">
    <thead>
        <tr>
            <th><h1></h1></th>
            <th><h1>Y</h1></th>
            <th><h1>Y-AS</h1></th>
            <th><h1>Y-AT</h1></th>
            <th><h1>Y-MS</h1></th>
            <th><h1>Y-MT</h1></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{0}</td>
            <td style="color:{1};"><b>{2}</b></td>
            <td style="color:{3};"><b>{4}</b></td>
            <td style="color:{5};"><b>{6}</b></td>
            <td style="color:{7};"><b>{8}</b></td>
            <td style="color:{9};"><b>{10}</b></td>
        </tr>
        <tr>
            <td>{0}-AS</td>
            <td style="color:{11};"><b>{12}</b></td>
            <td style="color:{13};"><b>{14}</b></td>
            <td style="color:{15};"><b>{16}</b></td>
            <td style="color:{17};"><b>{18}</b></td>
            <td style="color:{19};"><b>{20}</b></td>
        </tr>
        <tr>
            <td>{0}-AT</td>
            <td style="color:{21};"><b>{22}</b></td>
            <td style="color:{23};"><b>{24}</b></td>
            <td style="color:{25};"><b>{26}</b></td>
            <td style="color:{27};"><b>{28}</b></td>
            <td style="color:{29};"><b>{30}</b></td>
        </tr>
        <tr>
            <td>{0}-MS</td>
            <td style="color:{31};"><b>{32}</b></td>
            <td style="color:{33};"><b>{34}</b></td>
            <td style="color:{35};"><b>{36}</b></td>
            <td style="color:{37};"><b>{38}</b></td>
            <td style="color:{39};"><b>{40}</b></td>
        </tr>
        <tr>
            <td>{0}-MT</td>
            <td style="color:{41};"><b>{42}</b></td>
            <td style="color:{43};"><b>{44}</b></td>
            <td style="color:{45};"><b>{46}</b></td>
            <td style="color:{47};"><b>{48}</b></td>
            <td style="color:{49};"><b>{50}</b></td>
        </tr>
    </tbody>
</table>"""


