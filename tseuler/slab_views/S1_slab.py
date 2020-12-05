from ..utils import get_datasummary, get_valhexrg
from ..static import LOGOPATH, TSEULER_PANEL_DESCRIPTORS
from ..static.htmls import dtype_summary_table, nan_summary_table

import os
import panel as pn
from collections import Counter
from math import pi
import pandas as pd
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from operator import itemgetter

class DataSummaryPanel:
    def __init__(self, data, data_desc, dt_freq):
        self.data = data.copy()
        self.data_desc = data_desc
        self.dt_freq = dt_freq
        self.dtype_dict, self.nan_dict, self.total_cols, self.total_rows = get_datasummary(self.data)
        self.nan_summary_table = nan_summary_table
        self.dtype_summary_table = dtype_summary_table


    def get_view(self):
        logo_pane = pn.Column(pn.pane.PNG(os.path.relpath(LOGOPATH), width=300), pn.pane.HTML(TSEULER_PANEL_DESCRIPTORS['logo_description']))
        # Data Summary
        data_summary = pn.pane.HTML(f'''<p><b>Data Description</b> : {self.data_desc}</p>''')
        # Prepare DType Pane
        self.dtype_summary_table = self.dtype_summary_table.format('#8a8a8a',# Light Background 
                                                         get_valhexrg(self.dtype_dict['category']/self.total_cols),
                                                         round(100*self.dtype_dict['category']/self.total_cols, 3),
                                                         get_valhexrg(self.dtype_dict['int']/self.total_cols),
                                                         round(100*self.dtype_dict['int']/self.total_cols, 3),
                                                         get_valhexrg(self.dtype_dict['float']/self.total_cols),
                                                         round(100*self.dtype_dict['float']/self.total_cols, 3))
        dtype_donutplot = self.get_donutplot(self.dtype_dict, 'DType')
        dtype_table = pn.pane.HTML(self.dtype_summary_table, margin=(100, 5, 5, -30))
        dtype_pane = pn.Row(dtype_donutplot, dtype_table)
        dtype_pane = pn.Column(data_summary, pn.layout.Divider(), dtype_pane)

        # Prepare DType Pane
        nan_summary = pn.pane.HTML(f'''<p><b>Data Shape</b> : {self.data.shape}</p>''')
        nan_pane = self.get_donutplot(self.nan_dict, 'Missing')
        tnan = sum(self.nan_dict.values())
        html_phfillers = []
        
        for col, colval in sorted(self.nan_dict.items(), key=itemgetter(1), reverse=True)[:3]:
            if len(col)>10: col = col[:8]+'..'
            html_phfillers.append(col)
            try:
                _val = get_valhexrg(colval/tnan) 
                _pct = str(round(100*colval/tnan, 3))
                html_phfillers.append(_val)
                html_phfillers.append(_pct)
            except:
                _val = '#000000'
                _pct = 0.0
                html_phfillers += [_val, _pct]
        
        if len(html_phfillers)!=10:
            html_phfillers += ['--', '#000000', 0.0]*(3-(len(html_phfillers)-1)//3)

        self.nan_summary_table = self.nan_summary_table.format('#8a8a8a',*html_phfillers)
        nan_donutplot = self.get_donutplot(self.nan_dict, 'Missing')
        nan_table = pn.pane.HTML(self.nan_summary_table, margin=(100, 5, 5, -30))
        nan_pane = pn.Row(nan_donutplot, nan_table)
        nan_pane = pn.Column(nan_summary, pn.layout.Divider(), nan_pane)

        top_slab = pn.Row(logo_pane, dtype_pane, nan_pane, margin=(5,5,5,5))
        return top_slab

    def get_donutplot(self, datadict, _type = 'dtype'):
        
        # Data
        x = Counter(datadict)
        data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index()
        data = data.rename(index=str, columns={0:'value', 'index':_type})
        data['angle'] = data['value']/sum(x.values()) * 2*pi

        if len(x)>=3:
            data['color'] = Category20c[len(x)] 
        else:
            data['color'] = Category20c[3][:len(x)]
        data.fillna(0.0, inplace=True)

        # Plotting code
        p = figure(plot_height=200, plot_width=200, title=f"{_type} - Distribution",
                   toolbar_location=None, tools="hover",tooltips=[(f"{_type}", f"@{_type}"),("Value", "@value")])
        p.annular_wedge(x=0, y=1,inner_radius=0.4,outer_radius=0.8,
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="black", fill_color='color', legend_field = _type, source=data)
        p.axis.axis_label=None
        p.outline_line_color = None
        p.axis.visible=False
        p.grid.grid_line_color = None
        p.legend.visible=False
        return pn.pane.Bokeh(p)
    
