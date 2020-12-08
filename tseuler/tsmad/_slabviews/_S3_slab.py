#TODO : Update the marequee as and when the plot
#       is ready and buttons are being updated


from .._helpers import TS_UV_PLOTS, TS_BV_PLOTS, TS_TV_PLOTS, TS_FREQUENCIES_DESC, TS_FREQ_MAP
from .._helpers import TSMAD_CONFIGS
from .._helpers import stats_css, corr_css, table_html_1, table_html_2
from .._helpers import get_transformed_data, prep_statmetric

from .._plottting import get_plot

import param
import panel as pn
pn.extension('vega', raw_css=[stats_css, corr_css])
import pandas as pd


class PlottingPanel(param.Parameterized):
    # Variates Selections
    analysis_variant = param.ObjectSelector(default='UV', objects=['UV', 'BV', 'TV'])
    # Y Pane
    y_Select = param.Selector(objects=['--'])
    y_Lags = param.Integer(default=0, bounds=(0,12))
    y_Transformation = param.ObjectSelector(default='Actual',objects=['Actual', 'AS', 'AT', 'MS', 'MT'])
    # X1 Pane
    x1_Select = param.Selector(objects=['--'])
    x1_Lags = param.Integer(default=0, bounds=(0,12))
    x1_Transformation = param.ObjectSelector(default='Actual',objects=['Actual', 'AS', 'AT', 'MS', 'MT'])
    # X2 Pane
    x2_Select = param.Selector(objects=['--'])
    x2_Lags = param.Integer(default=0, bounds=(0,12))
    x2_Transformation = param.ObjectSelector(default='Actual',objects=['Actual', 'AS', 'AT', 'MS', 'MT'])
    # Plot Selector
    plot_variant = param.Selector(objects=['--'])
    # Frequency Slector
    freq_variant = param.String()
    # Plotting Data
    plotting_data = param.DataFrame()
    plotting_data_metrics = param.DataFrame()



    def __init__(self, filterObj, cat_cols, target_cols, data_freq, how_aggregate, force_interactive, **kwargs):
        super(PlottingPanel, self).__init__(**kwargs)
        self.filter_obj = filterObj
        self.filtered_data = self.filter_obj.get_filtereddata()

        # Data - Plotting
        self.cat_cols = cat_cols
        self.target_cols = target_cols
        self.selectable_cols = [k for k in self.filtered_data.columns if k not in self.cat_cols]
        self.TS_UV_PLOTS = TS_UV_PLOTS
        self.TS_BV_PLOTS = TS_BV_PLOTS
        self.TS_TV_PLOTS = TS_TV_PLOTS
        self.data_freq = data_freq
        self.how_aggregate = how_aggregate
        self.force_interactive = force_interactive

        self.vt_flag = False  # Variant Transition Flag   


    def get_view(self):
        # Prep View and Attach the handlers
        # Row - 1
        self.analysis_variantPanel = pn.panel(self.param.analysis_variant,
                                         widgets = {'analysis_variant' : {'widget_type' : pn.widgets.RadioButtonGroup,
                                                                          'button_type' : 'success',
                                                                          'width' : 660}})
        # Row - 2
        self.y_selectPanel = pn.panel(self.param.y_Select,
                                      widgets = {'y_Select' : {'widget_type' : pn.widgets.Select,
                                                               'width' : 180, 
                                                               'margin' : (-5,5,5,15)}})
        self.y_lagPanel = pn.panel(self.param.y_Lags,
                                   widgets = {'y_Lags' : {'widget_type' : pn.widgets.IntInput,
                                                          'width' : 80, 
                                                          'margin' : (-5,5,5,5)}})
        self.y_trnsrmPanel = pn.panel(self.param.y_Transformation,
                                      widgets = {'y_Transformation' : {'widget_type' : pn.widgets.RadioButtonGroup,
                                                                       'width' : 330,
                                                                       'button_type' : 'primary',
                                                                       'margin' : (12,5,5,5)}})
        y_row = pn.Row('####(Y) :', self.y_selectPanel, self.y_lagPanel, self.y_trnsrmPanel)
        
        # Row - 3
        self.x1_selectPanel = pn.panel(self.param.x1_Select,
                                       widgets = {'x1_Select' : {'widget_type' : pn.widgets.Select,
                                                                  'width' : 180, 
                                                                  'margin' : (-5,5,5,5)}})
        self.x1_lagPanel = pn.panel(self.param.x1_Lags,
                                    widgets = {'x1_Lags' : {'widget_type' : pn.widgets.IntInput,
                                                     'width' : 80, 
                                                     'margin' : (-5,5,5,5)}})
        self.x1_trnsrmPanel = pn.panel(self.param.x1_Transformation,
                                        widgets = {'x1_Transformation' : {'widget_type' : pn.widgets.RadioButtonGroup,
                                                                        'width' : 330,
                                                                        'button_type' : 'primary',
                                                                        'margin' : (12,5,5,5)}})
        x1_row = pn.Row('####(X1) :', self.x1_selectPanel, self.x1_lagPanel, self.x1_trnsrmPanel)
        
        # Row - 2
        self.x2_selectPanel = pn.panel(self.param.x2_Select,
                                        widgets = {'x2_Select' : {'widget_type' : pn.widgets.Select,
                                                                    'width' : 180,
                                                                    'margin' : (-5,5,5,5)}})
        self.x2_lagPanel = pn.panel(self.param.x2_Lags,
                                    widgets = {'x2_Lags' : {'widget_type' : pn.widgets.IntInput,
                                                            'width' : 80, 
                                                            'margin' : (-5,5,5,5)}})
        self.x2_trnsrmPanel = pn.panel(self.param.x2_Transformation,
                                        widgets = {'x2_Transformation' : {'widget_type' : pn.widgets.RadioButtonGroup,
                                                                  'width' : 330,
                                                                  'button_type' : 'primary',
                                                                  'margin' : (12,5,5,5)}})

        self.err_dispPanel = pn.panel('<marquee style="color:white; background-color:#660404;">Plotting...</marquee>', width = 660)
        x2_row = pn.Row('####(X2) :', self.x2_selectPanel, self.x2_lagPanel, self.x2_trnsrmPanel)
        
        # Plot Selector
        self.plot_variantPanel = pn.panel(self.param.plot_variant,
                                            widgets = {'plot_variant' : {'widget_type' : pn.widgets.Select,
                                                                        'width' : 290,
                                                                        'margin' : (-14, 5,5,5)}})
        
        self.slab_descPane = pn.pane.HTML('<p>Usual flow of Variable section involves selecting the\
                                            varible for ex : from <mark>Y Select</mark>, then selecting the Lag\
                                            from <mark>Y Lags</mark>, then selecting the transformation\
                                            <b>Actual, AS, AT, MS, MT</b></p>')
        
        
        # Initialise the plotting_data_metrics to -- for the call hit
        S3L1 = pn.Column('### Variable Slectors & Transformations:',
                         self.analysis_variantPanel, y_row, x1_row, x2_row, self.err_dispPanel)
        S3L2 = pn.Column('### Plot Variant :',
                         self.plot_variantPanel,
                         self.slab_descPane, 
                         self._update_metric_table, width=300)
                         
        # Init View & Data
        self._uv_view()

        # S3L3 - Plot and Metric Table
        dtfreq_html = pn.pane.HTML('<p style="font-size:1.2em;">Data Frequency : <b style="color:red;">{0}</b><br>\
            <i style="font-size:.6em; color:#8a8a8a">({1})</i></p> '.format(self.data_freq, TS_FREQUENCIES_DESC[self.data_freq]),
             margin=(-5,5,5,-300))
        self.freq_variantPanel = pn.panel(self.param.freq_variant,
                                          widgets = {'freq_variant' : {'widget_type' : pn.widgets.TextInput,
                                                                        'placeholder':'Frequency Variant',
                                                                        'width' : 100,
                                                                        'margin' : (-5,5,5,-100)}})
        
        S3L3 = pn.Row(self._update_plot_slab, dtfreq_html, self.freq_variantPanel, margin=(-490, 5,5, 5))
        
        S3 = pn.Column(pn.Row(S3L1, S3L2), S3L3, margin=(5,5,-20,5))

        return S3
    
    def _uv_view(self):
        
        self.selectable_cols = [k for k in self.filtered_data.columns if k not in self.cat_cols]

        self.param.y_Select.objects = self.target_cols
        self.y_Select = self.target_cols[0]
        
        self.param.x1_Select.objects = self.selectable_cols
        self.x1_Select = self.selectable_cols[0]

        self.param.x2_Select.objects = self.selectable_cols
        self.x2_Select = self.selectable_cols[0]

        self.freq_variantPanel = self.data_freq

        self.y_selectPanel.disabled = True
        self.y_lagPanel.disabled = True
        self.y_trnsrmPanel.disabled = True
        self.y_Lags = 0
        self.y_Transformation = 'Actual'

        self.x1_selectPanel.disabled = False
        self.x1_lagPanel.disabled = False
        self.x1_trnsrmPanel.disabled = False
        self.x1_Lags = 0
        self.x1_Transformation = 'Actual'
        
        self.x2_selectPanel.disabled = True
        self.x2_lagPanel.disabled = True
        self.x2_trnsrmPanel.disabled = True
        self.x2_Lags = 0
        self.x2_Transformation = 'Actual'

        # Add ohlc plot if data has open, close, high, low and volume
        if all(k in self.filter_obj.get_filtereddata().columns for k in ['open', 'high', 'low', 'close', 'volume']):
            self.TS_UV_PLOTS += ['CandleStick Chart : Financial Analysis']
        self.param.plot_variant.objects = self.TS_UV_PLOTS
        self.plot_variant = self.TS_UV_PLOTS[0]
        
        self.vt_flag = True
        self._update_plotting_data()

    def _bv_view(self):
        
        self.selectable_cols = [k for k in self.filtered_data.columns if k not in self.cat_cols+self.target_cols]

        self.param.x1_Select.objects = self.selectable_cols
        self.x1_Select = self.selectable_cols[0]

        self.param.x2_Select.objects = self.selectable_cols
        self.x2_Select = self.selectable_cols[0]
        
        self.y_selectPanel.disabled = False
        self.y_lagPanel.disabled = False
        self.y_trnsrmPanel.disabled = False
        self.y_Lags = 0
        self.y_Transformation = 'Actual'
        
        self.x1_selectPanel.disabled = False
        self.x1_lagPanel.disabled = False
        self.x1_trnsrmPanel.disabled = False
        self.x1_Lags = 0
        self.x1_Transformation = 'Actual'
        
        self.x2_selectPanel.disabled = True
        self.x2_lagPanel.disabled = True
        self.x2_trnsrmPanel.disabled = True
        self.x2_Lags = 0
        self.x2_Transformation = 'Actual'

        self._update_plotting_data()
        self.param.plot_variant.objects = self.TS_BV_PLOTS
        self.plot_variant = self.TS_BV_PLOTS[0]
        self.vt_flag = True
        self._update_plotting_data()

    def _tv_view(self):

        self.selectable_cols = [k for k in self.filtered_data.columns if k not in self.cat_cols+self.target_cols]

        if self.selectable_cols==[]:
            self.analysis_variantPanel.value = 'UV'
            self.analysis_variant = 'UV'

        self.param.y_Select.objects = self.target_cols
        self.y_Select = self.target_cols[0]

        self.param.x1_Select.objects = self.selectable_cols
        self.x1_Select = self.selectable_cols[0]

        self.param.x2_Select.objects = self.selectable_cols
        self.x2_Select = self.selectable_cols[0]
    
        self.y_selectPanel.disabled = False
        self.y_lagPanel.disabled = False
        self.y_trnsrmPanel.disabled = False
        self.y_Lags = 0
        self.y_Transformation = 'Actual'
        
        self.x1_selectPanel.disabled = False
        self.x1_lagPanel.disabled = False
        self.x1_trnsrmPanel.disabled = False
        self.x1_Lags = 0
        self.x1_Transformation = 'Actual'
        
        self.x2_selectPanel.disabled = False
        self.x2_lagPanel.disabled = False
        self.x2_trnsrmPanel.disabled = False
        self.x2_Lags = 0
        self.x2_Transformation = 'Actual'
        
        self._update_plotting_data()
        self.param.plot_variant.objects = self.TS_TV_PLOTS
        self.plot_variant = self.TS_TV_PLOTS[0]

        self.vt_flag = True
        self._update_plotting_data()



    @param.depends('analysis_variant', watch=True)
    def _update_view(self):
        self.vt_flag = False
        if self.analysis_variant == 'UV':
            self._uv_view()
        elif self.analysis_variant == 'BV':
            self._bv_view()
        elif self.analysis_variant == 'TV':
            self._tv_view()


    @param.depends('y_Select','y_Lags','y_Transformation',
                   'x1_Select','x1_Lags','x1_Transformation',
                   'x2_Select','x2_Lags','x2_Transformation','freq_variant', watch=True)
    def _update_plotting_data(self):
        # Filter the plotting data
        self.filtered_data = self.filter_obj.get_filtereddata()
        # Prepare Plotting Data
        if all(k != '--' for k in [self.y_Select, self.x1_Select, self.x2_Select]) and self.analysis_variant == 'UV' and self.vt_flag and self.freq_variantPanel!=None:
            tempDF= pd.DataFrame(index=self.filtered_data.index)
            tempDF['X1'] = self.filtered_data[self.x1_Select].copy()
            print(self.freq_variantPanel, '+', self.freq_variant)
            respacket = get_transformed_data(tempDF.X1,
                                            self.x1_Transformation,
                                            self.x1_Lags,
                                            self.data_freq,
                                            self.freq_variantPanel)
            tempDF['plotX1'],  tempDF['anfreq'], tempDF['anfreq_label'], tempDF['anfreq_label1'], tempDF['hue_col'], tarnsformERR = respacket
            if tarnsformERR: self.y_trnsrmPanel.value = 'Actual'
            self.plotting_data = tempDF.copy()
            
        elif all(k != '--' for k in [self.y_Select, self.x1_Select, self.x2_Select]) and self.analysis_variant == 'BV' and self.vt_flag and self.freq_variantPanel!=None:
            # If the x1_selection and x2_selection is same, then remove that option from x2_selction
            if len(set([self.y_Select, self.x1_Select])) != 2:
                _tempobjects = [k for k in self.selectable_cols if k not in [self.y_Select, self.x1_Select]]
                if _tempobjects == []:
                    self.analysis_variantPanel.value = 'UV'
                    self.analysis_variant = 'UV'
                else:
                    self.param.x2_Select.objects = _tempobjects
                    self.x2_Select = _tempobjects[0]
            else:
                tempDF = pd.DataFrame(index=self.filtered_data.index)
                tempDF['Y'] = self.filtered_data[self.y_Select].copy()
                tempDF['X1'] = self.filtered_data[self.x1_Select].copy()
                
                respacket = get_transformed_data(tempDF.Y,
                                                self.y_Transformation,
                                                self.y_Lags,
                                                self.data_freq,
                                                self.freq_variantPanel)
                tempDF['plotY'],  tempDF['anfreq'], tempDF['anfreq_label'], tempDF['anfreq_label1'], tempDF['hue_col'], tarnsformERR = respacket
                if tarnsformERR: 
                    self.y_trnsrmPanel.value = 'Actual'
                    # self.err_dispPanel = pn.panel('<marquee style="color:white; background-color:#660404;">{0}</marquee>'.format(tarnsformERR), width = 660)

                respacket = get_transformed_data(tempDF.X1,
                                                self.x1_Transformation,
                                                self.x1_Lags,
                                                self.data_freq,
                                                self.freq_variantPanel)
                tempDF['plotX1'],  tempDF['anfreq'], tempDF['anfreq_label'], tempDF['anfreq_label1'], tempDF['hue_col'], tarnsformERR = respacket
                if tarnsformERR:
                    self.x1_trnsrmPanel.value = 'Actual'

                self.plotting_data = tempDF.copy()

        elif all(k != '--' for k in [self.y_Select, self.x1_Select, self.x2_Select]) and self.analysis_variant == 'TV' and self.vt_flag and self.freq_variantPanel!=None:
            # If the x1_selection and x2_selection is same, then remove that option from x2_selction
            if len(set([self.y_Select, self.x1_Select, self.x2_Select])) != 3:
                _tempobjects = [k for k in self.selectable_cols if k not in [self.y_Select, self.x1_Select, self.x2_Select]]
                if _tempobjects == []:
                    self.analysis_variantPanel.value = 'UV'
                    self.analysis_variant = 'UV'
                else:
                    self.param.x2_Select.objects = _tempobjects
                    self.x2_Select = _tempobjects[0]
            else:
                tempDF = pd.DataFrame(index=self.filtered_data.index)

                tempDF['Y'] = self.filtered_data[self.y_Select].copy()
                tempDF['X1'] = self.filtered_data[self.x1_Select].copy()
                tempDF['X2'] = self.filtered_data[self.x2_Select].copy()
                
                respacket = get_transformed_data(tempDF.Y,
                                                 self.y_Transformation,
                                                 self.y_Lags,
                                                 self.data_freq,
                                                 self.freq_variant)
                tempDF['plotY'],  tempDF['anfreq'], tempDF['anfreq_label'], tempDF['anfreq_label1'], tempDF['hue_col'], tarnsformERR = respacket
                if tarnsformERR: 
                    self.y_trnsrmPanel.value = 'Actual'

                respacket = get_transformed_data(tempDF.X1,
                                                 self.x1_Transformation,
                                                 self.x1_Lags,
                                                 self.data_freq,
                                                 self.freq_variant)
                tempDF['plotX1'],  tempDF['anfreq'], tempDF['anfreq_label'], tempDF['anfreq_label1'], tempDF['hue_col'], tarnsformERR = respacket
                if tarnsformERR: 
                    self.x1_trnsrmPanel.value = 'Actual'

                respacket = get_transformed_data(tempDF.X2,
                                                 self.x2_Transformation,
                                                 self.x2_Lags,
                                                 self.data_freq,
                                                 self.freq_variant)
                tempDF['plotX2'],  tempDF['anfreq'], tempDF['anfreq_label'], tempDF['anfreq_label1'], tempDF['hue_col'], tarnsformERR = respacket
                if tarnsformERR: 
                    self.x2_trnsrmPanel.value = 'Actual'

                self.plotting_data = tempDF.copy()


    @param.depends('plotting_data', 'plot_variant', watch=False)
    def _update_plot_slab(self):
        if not hasattr(self.plotting_data, 'empty'):
            return None
        # Get Plot based on the plotting data
        if (not self.plotting_data.empty):
            # Only Update 'plotting_data_metrics' if columns is in concurrence with the analysis variant
            check1 = self.analysis_variant == 'UV' and all(k in self.plotting_data.columns for k in ['plotX1'])
            check2 = self.analysis_variant == 'BV' and all(k in self.plotting_data.columns for k in ['plotX1', 'plotY'])
            check3 = self.analysis_variant == 'TV' and all(k in self.plotting_data.columns for k in ['plotX1', 'plotY', 'plotX2'])
            if check1 or check2 or check3:
                self.plotting_data_metrics = pd.DataFrame(prep_statmetric(self.plotting_data, self.analysis_variant))
                # Return the Plot
                self.plot_namePane = pn.pane.HTML(f'''<p style="font-size:2.4em; color:#8a8a8a">{self.analysis_variant} : {self.plot_variant.split(':')[0].strip()}</p>
                                                    <p style="font-size:.6em; color:#8a8a8a"><i>*NOTE:By Default plots are interactive, but
                                                    if the datapoints exceed 2500 plot switch to static</i></p>''', margin= (-5,5,5,5))
                self.plot_filterPanel = pn.pane.HTML(f'''<p style="font-size:0.9em; color:#4a4a4a">{self.filter_obj.get_current_filter_depth()}</p>''', margin= (-5,5,5,5))
                if self.plot_variant == 'CandleStick Chart : Financial Analysis':
                    _plt = get_plot(plot_data = self.filtered_data,
                                    variate_type = self.analysis_variant,
                                    plot_name = self.plot_variant,
                                    freq_variant = self.freq_variant,
                                    how_aggregate = self.how_aggregate,
                                    force_interactive = self.force_interactive)
                else:                    
                    _plt = get_plot(plot_data = self.plotting_data,
                                    variate_type = self.analysis_variant,
                                    plot_name = self.plot_variant,
                                    freq_variant = self.freq_variant,
                                    how_aggregate = self.how_aggregate,
                                    y_label = self.y_Select, x1_label = self.x1_Select, x2_label = self.x2_Select,
                                    force_interactive = self.force_interactive)
                    
                _pane = pn.Column(self.plot_namePane, self.plot_filterPanel, _plt, width=660)
                return _pane
    

    @param.depends('plotting_data_metrics', watch=False)
    def _update_metric_table(self):
        
        if not hasattr(self.plotting_data_metrics, 'empty'):
            return None
        if not self.plotting_data_metrics.empty:
            if self.analysis_variant == 'UV':
                _fillers = list(self.plotting_data_metrics.values.ravel())
                _stat_fillers = _fillers[:26]
                _corr_fillers = _fillers[26:]
                stat_summaryPane = pn.Tabs(('Stat:X1', pn.pane.HTML(table_html_1.format(*_stat_fillers), width=300)),
                                           margin=(5, 5, 5, 5), width=300)
            elif self.analysis_variant == 'BV':
                _fillers = list(self.plotting_data_metrics.values.ravel())
                _x1stat_fillers = _fillers[:26]
                _ystat_fillers = _fillers[26:52]
                _corr_fillers = _fillers[52:]
                stat_summaryPane = pn.Tabs(('Corr:X1-Y', pn.pane.HTML(table_html_2.format(*_corr_fillers), width=300)),
                                           ('Stat:X1', pn.pane.HTML(table_html_1.format(*_x1stat_fillers), width=300)),
                                           ('Stat:Y', pn.pane.HTML(table_html_1.format(*_ystat_fillers), width=300)),
                                            margin=(5, 5, 5, 5), width=300)
            elif self.analysis_variant == 'TV' and all(k in self.plotting_data.columns for k in ['plotX1', 'plotY', 'plotX2']):
                _fillers = list(self.plotting_data_metrics.values.ravel())
                _x1stat_fillers = _fillers[:26]
                _x2stat_fillers = _fillers[26:52]
                _ystat_fillers = _fillers[52:78]
                _corryx1_fillers = _fillers[78:129]
                _corryx2_fillers = _fillers[129:]
                stat_summaryPane = pn.Tabs(('Corr:X1-Y', pn.pane.HTML(table_html_2.format(*_corryx1_fillers), width=300)),
                                           ('Corr:X2-Y', pn.pane.HTML(table_html_2.format(*_corryx2_fillers), width=300)),
                                           ('Stat:X1', pn.pane.HTML(table_html_1.format(*_x1stat_fillers), width=300)),
                                           ('Stat:X2', pn.pane.HTML(table_html_1.format(*_x2stat_fillers), width=300)),
                                           ('Stat:Y', pn.pane.HTML(table_html_1.format(*_ystat_fillers), width=300)),
                                            margin=(5, 5, 5, 5), width=300)
            return stat_summaryPane


