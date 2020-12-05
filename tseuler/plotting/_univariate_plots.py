
from ..static import TSEULER_CONFIGS
from ..utils import get_rgbtohex

from datetime import datetime
import calendar
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import altair as alt
import seaborn as sns
import panel as pn
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot



def uv_linePlot(data, engine, xlabel, ylabel):

    data = data.copy() 
    data.rename(columns={'plotX1':ylabel}, inplace=True)

    if engine == 'Static':

        fig = data[ylabel].plot(figsize=(9,6), legend=True).figure
        plt.xlabel(xlabel, fontsize = 15)
        plt.ylabel(ylabel, fontsize = 15)
        plt.grid(b=True, which='major', color='k', linewidth=0.25)
        plt.grid(b=True, which='minor', color='k', linewidth=0.125)
        
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'], name='isel')
        # Base Plot
        base = alt.Chart(data.dropna().reset_index()).mark_line()
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                        tooltip = ylabel)
        base = base.properties(width = 612, height = 300)
        # Upper Plot
        upper = base.encode(x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title=''),
                            y = alt.Y('{0}:Q'.format(ylabel), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        # Lower Plot
        lower = base.mark_area(line={'color':'darkgray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgray', offset=1)],
                x1=1, x2=1,
                y1=1, y2=0
            ))
        lower = lower.encode(y=alt.Y('{0}:Q'.format(ylabel), title='', axis=None))
        lower = lower.properties(height=20)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'
        # Base Statistics
        base_stat = upper.transform_filter(brush)
        base_stat = base_stat.transform_aggregate(Mean='mean({0})'.format(ylabel),
                                                  StdDev='stdev({0})'.format(ylabel),
                                                  Var='variance({0})'.format(ylabel))
        # Label Statistics
        label_stat = base_stat.transform_calculate(
            stat_label="'Mean = ' + format(datum.Mean, '.1f') + \
            '; Standard Deviation = ' + format(datum.StdDev, '.1f') +\
            '; Variance = ' + format(datum.Var, '.1f')")
        label_stat = label_stat.mark_text(align='left', baseline='bottom')
        label_stat = label_stat.encode(x=alt.value(0.0), y=alt.value(12.0), text=alt.Text('stat_label:N'))
        # Values
        _ymean_uu = data[ylabel].max()
        _ymean = data[ylabel].mean()
        _ystd_uu = data[ylabel].std()*1.5
        _ystd = data[ylabel].std()
        _yvar_uu = data[ylabel].var()*1.5
        _yvar = data[ylabel].var()
        # Stat Bar Base
        stats_barbase = base_stat.mark_bar()
        stats_barbase = stats_barbase.properties(width = 200, height = 20)
        # Mean Bar
        mean_bar = stats_barbase.encode(x=alt.X('Mean:Q', title='Mean', scale=alt.Scale(domain=[-_ymean_uu,_ymean_uu]), axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totmean_line = alt.Chart(pd.DataFrame({'x': [_ymean]}))
        totmean_line = totmean_line.mark_rule(color='red', size=5)
        totmean_line = totmean_line.encode(x='x')
        mean_bar += totmean_line
        # Standard Deviation Bar
        std_bar = stats_barbase.encode(x=alt.X('StdDev:Q', title='Std', scale=alt.Scale(domain=[-_ystd_uu,_ystd_uu]), axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totstd_line = alt.Chart(pd.DataFrame({'x': [_ystd]}))
        totstd_line = totstd_line.mark_rule(color='red', size=5)
        totstd_line = totstd_line.encode(x='x')
        std_bar += totstd_line
        # Variance Bar
        var_bar = stats_barbase.encode(x=alt.X('Var:Q', title='Var', scale=alt.Scale(domain=[-_yvar_uu,_yvar_uu]), axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totvar_line = alt.Chart(pd.DataFrame({'x': [_yvar]}))
        totvar_line = totvar_line.mark_rule(color='red', size=5)
        totvar_line = totvar_line.encode(x='x')
        var_bar += totvar_line
        # Concatenated
        p = alt.vconcat(upper+label_stat, mean_bar|std_bar|var_bar, lower).configure_concat(spacing=2)
        
        return p


def uv_areaPlot(data, engine, xlabel, ylabel):
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    if engine == 'Static':
        fig, axes = plt.subplots(figsize=(9.4,5))
        
        pdata = data[ylabel].copy()
        pdata[pdata<0] = np.nan
        ndata = data[ylabel].copy()
        ndata[ndata>=0] = np.nan
        axes.fill_between(pdata.index, pdata.values)
        axes.fill_between(ndata.index, ndata.values, color='orange')
        
        axes.set_xlabel(xlabel, fontsize = 15)
        axes.set_ylabel(ylabel, fontsize = 15)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
        axes.grid(b=True, which='minor', color='k', linewidth=0.125)
        
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'], name='isel')
        # Base Plot
        base = alt.Chart(data.dropna().reset_index())
        base = base.mark_area(line={'color':'darkgreen'},
                              color=alt.Gradient(
                                gradient='linear',
                                stops=[alt.GradientStop(color='white', offset=0),
                                    alt.GradientStop(color='darkgreen', offset=1)],
                                x1=1,
                                x2=1,
                                y1=1,
                                y2=0
                            ))
        if any(data[ylabel].dropna()<0):
            base = base.transform_calculate(negative='datum.{0} < 0'.format(ylabel))
            base = base.encode(x = '{0}:T'.format(data.index.name),
                            y = '{0}:Q'.format(ylabel),
                            tooltip = ylabel,
                            color = alt.Color('negative:N', legend=None))
        else:
            base = base.encode(x = '{0}:T'.format(data.index.name),
                                y = '{0}:Q'.format(ylabel),
                                tooltip = ylabel)
        base = base.properties(width = 635, height = 300)
        # Upper Plot
        upper = base.encode(x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title=''),
                            y = alt.Y('{0}:Q'.format(ylabel), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        # Lower Plot
        lower = base.mark_area(line={'color':'darkgray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgray', offset=1)],
                x1=1, x2=1,
                y1=1, y2=0
            ))
        lower = lower.encode(y=alt.Y('{0}:Q'.format(ylabel), title='', axis=None))
        lower = lower.properties(height=20)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'
        # Base Statistics
        base_stat = upper.transform_filter(brush)
        base_stat = base_stat.transform_aggregate(Mean='mean({0})'.format(ylabel),
                                                StdDev='stdev({0})'.format(ylabel),
                                                Var='variance({0})'.format(ylabel))
        # Label Statistics
        label_stat = base_stat.transform_calculate(
            stat_label="'Mean = ' + format(datum.Mean, '.1f') + \
            '; Standard Deviation = ' + format(datum.StdDev, '.1f') +\
            '; Variance = ' + format(datum.Var, '.1f')")
        label_stat = label_stat.mark_text(align='left', baseline='bottom')
        label_stat = label_stat.encode(x=alt.value(0.0), y=alt.value(12.0), text=alt.Text('stat_label:N'))
        # Values
        _ymean_uu = data[ylabel].max()
        _ymean = data[ylabel].mean()
        _ystd_uu = data[ylabel].std()*1.5
        _ystd = data[ylabel].std()
        _yvar_uu = data[ylabel].var()*1.5
        _yvar = data[ylabel].var()
        # Stat Bar Base
        stats_barbase = base_stat.mark_bar()
        stats_barbase = stats_barbase.properties(width = 200, height = 20)
        # Mean Bar
        mean_bar = stats_barbase.encode(x=alt.X('Mean:Q', title='Mean', scale=alt.Scale(domain=[-_ymean_uu,_ymean_uu]), axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totmean_line = alt.Chart(pd.DataFrame({'x': [_ymean]}))
        totmean_line = totmean_line.mark_rule(color='red', size=5)
        totmean_line = totmean_line.encode(x='x')
        mean_bar += totmean_line
        # Standard Deviation Bar
        std_bar = stats_barbase.encode(x=alt.X('StdDev:Q', title='Std', scale=alt.Scale(domain=[-_ystd_uu,_ystd_uu]), axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totstd_line = alt.Chart(pd.DataFrame({'x': [_ystd]}))
        totstd_line = totstd_line.mark_rule(color='red', size=5)
        totstd_line = totstd_line.encode(x='x')
        std_bar += totstd_line
        # Variance Bar
        var_bar = stats_barbase.encode(x=alt.X('Var:Q', title='Var', scale=alt.Scale(domain=[-_yvar_uu,_yvar_uu]), axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totvar_line = alt.Chart(pd.DataFrame({'x': [_yvar]}))
        totvar_line = totvar_line.mark_rule(color='red', size=5)
        totvar_line = totvar_line.encode(x='x')
        var_bar += totvar_line
        # Concatenated
        p = alt.vconcat(upper+label_stat, mean_bar|std_bar|var_bar, lower).configure_concat(spacing=2)
        return p


def uv_boxPlot(data, engine, xlabel, ylabel, afreq):
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)

    if engine == 'Static':
        fig, axes = plt.subplots(figsize=(9.4,5))
        sns.boxplot(x="anfreq_label", y=ylabel, data=data, ax = axes)

        axes.set_xlabel(afreq, fontsize = 15)
        axes.set_ylabel(ylabel, fontsize = 15)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
        axes.grid(b=True, which='minor', color='k', linewidth=0.125)
        
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        brush = alt.selection(type='interval', encodings=['x'])
        source = data.copy()
        base = alt.Chart(source).mark_boxplot()
        if afreq not in ['Month Start', 'Month End']:
            base = base.encode(x=alt.X('anfreq_label:O',
                                        axis=alt.Axis(labelAngle = 45.0),
                                        title = afreq,
                                        sort=alt.EncodingSortField(field='anfreq_label', order='ascending')),
                                y=alt.Y('{0}:Q'.format(ylabel), axis=alt.Axis(format='~s')))
        else:
            base = base.encode(x=alt.X('anfreq_label:O',
                                        axis=alt.Axis(labelAngle = 45.0),
                                        title = afreq,
                                        sort=['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                                'August', 'September', 'October', 'November', 'December']),
                           y=alt.Y('{0}:Q'.format(ylabel), axis=alt.Axis(format='~s')))

        base = base.properties(width = 625, height = 360)

        return base


def uv_ridgePlot(data, engine, xlabel, ylabel, afreq):
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    if data['anfreq_label'].nunique()>15:
        engine = 'Interactive'

    if engine == 'Static':

        sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
        # Initialize the FacetGrid object
        pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
        g = sns.FacetGrid(data, row="anfreq_label", hue="anfreq_label", aspect=15, height=.5, palette=pal)

        # Draw the densities in a few steps
        g.map(sns.kdeplot, ylabel,
                bw_adjust=.5, clip_on=False,
                fill=True, alpha=1, linewidth=1.5)
        g.map(sns.kdeplot, ylabel, clip_on=False, color="w", lw=2, bw_adjust=.5)
        g.map(plt.axhline, y=0, lw=2, clip_on=False)

        # Define and use a simple function to label the plot in axes coordinates
        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, fontweight="bold", color=color,
                    ha="left", va="center", transform=ax.transAxes)

        g.map(label, ylabel)

        # Set the subplots to overlap
        g.fig.subplots_adjust(hspace=-.25)

        # Remove axes details that don't play well with overlap
        g.set_titles("")
        g.set(yticks=[])
        g.despine(bottom=True, left=True)
        plt.close()
        return pn.pane.Matplotlib(g.fig, tight=True)
    
    elif engine == 'Interactive':
        
        step=30
        overlap = 2
        data = data.dropna()
        min_cval = data[ylabel].min()
        max_cval = data[ylabel].max()
        ridgeline = alt.Chart(data, height=step)
        ridgeline = ridgeline.mark_area(interpolate="monotone",
                                        fillOpacity=0.8,
                                        stroke="lightgray",
                                        strokeWidth=0.5)
        ridgeline = ridgeline.encode(alt.X("{0}:Q".format(ylabel), bin=True, title=ylabel, axis=alt.Axis(format='~s')))
        ridgeline = ridgeline.encode(alt.Y("count({0}):Q".format(ylabel), 
                                        scale=alt.Scale(range=[step, -step * overlap]), impute=alt.ImputeParams(value=0),
                                        axis=None))
        ridgeline = ridgeline.encode(alt.Fill("mean({0}):Q".format(ylabel),
                                            legend=None,
                                            scale=alt.Scale(domain=[max_cval, min_cval], scheme="redyellowblue")))
        if afreq not in ['Month Start', 'Month End']:
            ridgeline = ridgeline.encode(alt.Row("{0}:N".format('anfreq_label'),
                                                 header=alt.Header(labelAngle=0, labelAlign="left")))
        else:
            ridgeline = ridgeline.encode(alt.Row("{0}:N".format('anfreq_label'), title=afreq,
                                                sort=['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                                    'August', 'September', 'October', 'November', 'December'],
                                                header=alt.Header(labelAngle=0, labelAlign="left")))
        ridgeline = ridgeline.properties(bounds="flush", width = 525)
        ridgeline = ridgeline.configure_facet(spacing=0)

        return ridgeline


def uv_seasonalPlot(data, engine, xlabel, ylabel, afreq, aggf):
    
    data = data.dropna().copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    data = data.groupby(['anfreq_label', 'anfreq_label1']).agg({ylabel: aggf}).reset_index()
    
    if engine == 'Static':
        fig , axes = plt.subplots(figsize=(9.4,5))
        _ = sns.lineplot(x = 'anfreq_label1', y = ylabel, data = data,
                        hue = 'anfreq_label', marker = 'o', ax = axes, legend='Week' not in afreq)

        axes.set_xlabel(afreq, fontsize = 15)
        axes.set_ylabel(ylabel, fontsize = 15)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
        axes.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        
        data = data.dropna()
        nearest = alt.selection(type='single', nearest=True,
                                on='mouseover', fields=['anfreq_label1'],
                                empty='none')
        _xshand = 'anfreq_label1:Q'
        _legend = alt.Legend()
        _yencoder = alt.Y('{0}:Q'.format(ylabel), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s'))

        if afreq == 'Year Start':
            _legend = alt.Legend(type='gradient')
        elif afreq=='Weeks':
            _xshand = 'anfreq_label1:N'
            _legend = None
        elif afreq=='Year End':
            _xshand = 'anfreq_label1:N'
            _legend = alt.Legend(type='gradient')

        line = alt.Chart(data)
        line = line.mark_line(interpolate='monotone')
        line = line.encode(x = alt.X(_xshand, axis=alt.Axis(labelAngle = 0.0), title='Day'),
                           y = _yencoder,
                           color=alt.Color('anfreq_label:N',
                                            legend = _legend,
                                            title = afreq))

        selectors = alt.Chart(data).mark_point()
        selectors = selectors.encode(x = alt.X(_xshand, axis=alt.Axis(labelAngle = 0.0)),
                                     opacity = alt.value(0))
        selectors = selectors.add_selection(nearest)

        points = line.mark_point()
        points = points.encode(opacity=alt.condition(nearest,alt.value(1),alt.value(0)))

        text = line.mark_text(align='left', dx=5, dy=-5)
        text = text.encode(text=alt.condition(nearest, '{0}:Q'.format(ylabel), alt.value(' ')))

        rules = alt.Chart(data).mark_rule(color='gray')
        rules = rules.encode(x = alt.X(_xshand, axis=alt.Axis(labelAngle = 0.0)))
        rules = rules.transform_filter(nearest)

        p = alt.layer(line,  selectors,  points,  rules,  text)
        p = p.configure_legend(gradientLength=280, gradientThickness=10)
        p = p.properties(width = 545, height = 350)
        
        return p


def uv_histPlot(data, engine, xlabel, ylabel):
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    
    if engine == 'Static':
        fig, axes = plt.subplots(figsize=(9.4,5))
        data[ylabel].hist(ax=axes)

        axes.set_xlabel(xlabel, fontsize = 15)
        axes.set_ylabel(ylabel, fontsize = 15)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
        axes.grid(b=True, which='minor', color='k', linewidth=0.125)
        
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        
        brush = alt.selection(type='interval', encodings=['x'])
        source = data[ylabel].reset_index()
        base = alt.Chart(source).mark_bar()
        if any(data[ylabel].dropna()<0):
            base = base.transform_calculate(negative='datum.{0} < 0'.format(ylabel))
            base = base.encode(x = alt.X('{0}:T'.format(data.index.name)),
                               y = alt.Y('{0}:Q'.format(ylabel), axis=alt.Axis(format='~s')),
                               tooltip = ylabel,
                               color = alt.Color('negative:N', legend=None))
        else:
            base = base.encode(x = alt.X('{0}:T'.format(data.index.name)),
                               y = alt.Y('{0}:Q'.format(ylabel), axis=alt.Axis(format='~s')),
                               tooltip = ylabel)
        base = base.properties(width = 600, height = 320)

        upper = base.encode(alt.X('{0}:T'.format(data.index.name), 
                                scale=alt.Scale(domain=brush)))
        upper.configure_title(fontSize=25)
        upper.encoding.x.title = xlabel
        upper.encoding.y.title = ylabel
        upper.configure_axisBottom(labelFontSize = 15)
        upper.configure_axisLeft(labelFontSize = 15)

        lower = base.properties(height=30).add_selection(brush)
        lower.title = ''
        lower.encoding.x.title = 'Interval Selection'
        lower.encoding.y.title = ''
        lower.encoding.y.axis.title = ''
        lower.configure_axisBottom(labelFontSize = 4)
        lower.configure_axisLeft(labelFontSize = 1)
        
        line = alt.Chart()
        line = line.mark_rule(color='firebrick')
        line = line.encode(y='mean({0}):Q'.format(ylabel),
                        size=alt.SizeValue(3))
        line = line.transform_filter(brush)
        upper = alt.layer(upper, line, data=source)

        p = alt.vconcat(upper, lower).configure_concat(spacing=2)
        return p


def uv_acfPlot(data, engine, xlabel, ylabel):
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    fig, axes = plt.subplots(figsize=(9.4,5))
    
    plot_acf(data[ylabel].dropna().values, ax=axes)
    axes.set_xlabel('Lags', fontsize = 15)
    axes.set_ylabel('Correlation', fontsize = 15)
    axes.grid(b=True, which='major', color='k', linewidth=0.25)
    axes.grid(b=True, which='minor', color='k', linewidth=0.125)
    
    plt.close()
    return pn.pane.Matplotlib(fig, tight=True)
    

def uv_pacfPlot(data, engine, xlabel, ylabel):
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)

    fig, axes = plt.subplots(figsize=(9.4,5))
    
    plot_pacf(data[ylabel].dropna().values, ax=axes)
    axes.set_xlabel('Lags', fontsize = 15)
    axes.set_ylabel('Correlation', fontsize = 15)
    axes.grid(b=True, which='major', color='k', linewidth=0.25)
    axes.grid(b=True, which='minor', color='k', linewidth=0.125)
    
    plt.close()
    return pn.pane.Matplotlib(fig, tight=True)


def uv_qqPlot(data, engine, xlabel, ylabel):
    # Add Altair : https://altair-viz.github.io/gallery/scatter_qq.html
    data = data.copy()
    data.rename(columns={'plotX1':ylabel}, inplace=True)

    if engine=='Static':
        fig, axes = plt.subplots(figsize=(9.4,5))
        qqplot(data[ylabel].dropna().values, ax=axes)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
        axes.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)

    elif engine == 'Interactive':
        p = alt.Chart(data)
        p = p.transform_quantile(ylabel, step=0.01, as_ = ['p', 'v'])
        p = p.transform_calculate(normal = 'quantileNormal(datum.p)')
        p = p.mark_point()
        p = p.encode(x=alt.X('normal:Q'),
                     y=alt.Y('v:Q', axis=alt.Axis(format='~s')))
        p = p.properties(width = 600, height = 360).interactive()
        return p


def uv_maSmoothPlot(data, engine, xlabel, ylabel):

    # Data Prep
    data = data.copy() 
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    _config_mawin = TSEULER_CONFIGS['plotting.uv.ma_window']
    if isinstance(_config_mawin, float):
        ma_win = int(_config_mawin*data.shape[0])
    elif isinstance(_config_mawin, int):
        ma_win = _config_mawin

    ma_colname = 'Moving Average ({0})'.format(ma_win)
    data[ma_colname] = data[ylabel].rolling(window=ma_win).mean()

    if engine == 'Static':

        fig = data[[ylabel, ma_colname]].plot(figsize=(9,6), legend=True).figure
        plt.xlabel(xlabel, fontsize = 15)
        plt.ylabel(ylabel, fontsize = 15)
        plt.grid(b=True, which='major', color='k', linewidth=0.25)
        plt.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'], name='isel')
        # Base Plot
        base = alt.Chart(data.reset_index()).mark_line()
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                           tooltip = ylabel)
        base = base.properties(width = 620, height = 360)
        # Upper Plot
        x_ecoder = x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title='')
        upper = base.encode(x = x_ecoder,
                            y = alt.Y('{0}:Q'.format(ylabel), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')),
                            tooltip=[ylabel])
        # Moving Average Line
        ma_line = upper.encode(x = alt.X('{0}:T'.format(data.index.name),
                                 scale=alt.Scale(domain=brush), title=''),
                       color=alt.ColorValue('red'),
                       y = alt.Y('{0}:Q'.format(ma_colname), scale=alt.Scale(zero=False)))

        # Lower Plot
        lower = base.mark_area(line={'color':'darkgray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgray', offset=1)],
                x1=1, x2=1,
                y1=1, y2=0
            ))
        lower = lower.encode(y=alt.Y('{0}:Q'.format(ylabel), title='', axis=None))
        lower = lower.properties(height=20)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'
        # Concatenated
        p = alt.vconcat(upper+ma_line, lower).configure_concat(spacing=2)

        return p


def uv_expSmoothPlot(data, engine, xlabel, ylabel):

    # Data Prep
    data = data.copy() 
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    _config_expspan = TSEULER_CONFIGS['plotting.uv.exp_span']
    if isinstance(_config_expspan, float):
        exp_span = int(_config_expspan*data.shape[0])
    elif isinstance(_config_expspan, int):
        exp_span = _config_expspan

    exp_colname = 'Moving Average ({0})'.format(exp_span)
    data[exp_colname] = data[ylabel].ewm(span=exp_span).mean()

    if engine == 'Static':

        fig = data[[ylabel, exp_colname]].plot(figsize=(9,6), legend=True).figure
        plt.xlabel(xlabel, fontsize = 15)
        plt.ylabel(ylabel, fontsize = 15)
        plt.grid(b=True, which='major', color='k', linewidth=0.25)
        plt.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'], name='isel')
        # Base Plot
        base = alt.Chart(data.reset_index()).mark_line()
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                        tooltip = ylabel)
        base = base.properties(width = 620, height = 360)
        # Upper Plot
        x_ecoder = x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title='')
        upper = base.encode(x = x_ecoder,
                            y = alt.Y('{0}:Q'.format(ylabel), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')),
                        tooltip=[ylabel])
        # Exponential Smoothing Line
        exp_line = upper.encode(x = alt.X('{0}:T'.format(data.index.name),
                                          scale=alt.Scale(domain=brush), title=''),
                                color=alt.ColorValue('red'),
                                y = alt.Y('{0}:Q'.format(exp_colname), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        # Lower Plot
        lower = base.mark_area(line={'color':'darkgray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgray', offset=1)],
                x1=1, x2=1,
                y1=1, y2=0
            ))
        lower = lower.encode(y=alt.Y('{0}:Q'.format(ylabel), title='', axis=None))
        lower = lower.properties(height=20)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'
        # Concatenated
        p = alt.vconcat(upper+exp_line, lower).configure_concat(spacing=2)

        return p


def uv_fourierSmoothPlot(data, engine, xlabel, ylabel):

    # Data Prep
    data = data.dropna().copy() 
    data.rename(columns={'plotX1':ylabel}, inplace=True)
    fcomp_factor = TSEULER_CONFIGS['plotting.uv.fcomp_factor']
    y = data[ylabel].values
    n = len(y)
    x = data[ylabel].index
    comps = np.unique(np.geomspace(1, int(fcomp_factor*data.shape[0]), 50).astype(int))
    colors = np.linspace(start=1, stop=255, num=comps.max()*2)

    for ecomp in comps:
        Y = np.fft.fft(y)
        np.put(Y, range(ecomp+1, n), 0.0)
        ifft = np.fft.ifft(Y)
        data['tseulerF_{0}'.format(ecomp)] = ifft.real

    if engine == 'Static':
        fig, axes  = plt.subplots(figsize=(9,6))
        for eidx, efcol in enumerate([k for k in data.columns if 'tseulerF_' in k]):
            _opacity = (eidx+1)/len(comps) if (eidx+1)/len(comps)>0.4 else 0.4
            _color = plt.cm.Reds(int(colors[int(efcol.split('_')[-1])]))
            axes.plot(x, data[efcol],
                      color = _color,
                      alpha = _opacity)

        _=axes.plot(x,y, label="Original dataset", linestyle='--')
        _=axes.grid(linestyle='dashed')
        _=axes.legend()
        plt.xlabel(xlabel, fontsize = 15)
        plt.ylabel(ylabel, fontsize = 15)
        plt.grid(b=True, which='major', color='k', linewidth=0.25)
        plt.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        # Base Plot
        base = alt.Chart(data.reset_index()).mark_line()
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                           tooltip = ylabel)
        base = base.properties(width = 612, height = 360)
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                           y = alt.Y('{0}:Q'.format(ylabel), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')),
                           tooltip=[ylabel])
        _flayers = [base]
        for cidx, col in enumerate([k for k in data.columns if 'tseulerF_' in k]):
            _t = int(col.split('_')[-1]) 
            _color = get_rgbtohex(*plt.cm.Reds(int(colors[_t]))[:-1])
            _opacity = (cidx+1)/len(comps) if (cidx+1)/len(comps)>0.4 else 0.4
            _tf = base.encode(y=alt.Y('{0}:Q'.format(col), title='',
                                      scale=alt.Scale(zero=False)),
                            color=alt.ColorValue(_color),
                            opacity=alt.OpacityValue(_opacity))
            _flayers.append(_tf)

        p = alt.layer(*_flayers).interactive()
        return p


def uv_candlestickPlot(data, engine, xlabel, ylabel):
    data = data.copy()
    if engine == 'Static':
        fig,_=mpf.plot(data, type='candlestick', figsize=(9,6),
                    volume=True, style='charles', returnfig=True)
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        data.columns = [k.lower() for k in data.columns]
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'])
        open_close_color = alt.condition("datum.open <= datum.close",
                                        alt.value("#06982d"),
                                        alt.value("#ae1325"))
        base = alt.Chart(data.reset_index())
        base = base.encode(alt.X('{0}:T'.format(data.index.name),
                                title='', axis=None, 
                                scale=alt.Scale(domain=brush)),
                            color = open_close_color,
                            tooltip = ['open', 'high', 'low', 'close'])
        # Rule
        rule = base.mark_rule()
        rule = rule.encode(alt.Y('low:Q', title='Price', scale=alt.Scale(zero=False)),
                        alt.Y2('high:Q'))
        # Bars
        bar = base.mark_bar()
        bar = bar.encode(alt.Y('open:Q'),alt.Y2('close:Q'))
        # Candlestick Chart
        candlestick_chart = rule + bar
        candlestick_chart = candlestick_chart.properties(width = 600, height = 280)
        candlestick_chart = candlestick_chart.transform_filter(brush)
        # Volume Chart
        volume_chart = alt.Chart(data.reset_index())
        volume_chart = volume_chart.mark_bar()
        volume_chart = volume_chart.encode(alt.X('{0}:T'.format(data.index.name), title='',
                                                scale=alt.Scale(domain=brush)),
                                        alt.Y('volume:Q', axis=alt.Axis(format='~s')),
                                        color=open_close_color)
        volume_chart = volume_chart.transform_filter(brush)
        volume_chart = volume_chart.properties(width = 600, height = 60)
        # Selection Chart
        lower = alt.Chart(data.reset_index())
        lower = lower.mark_area(line={'color':'darkgray'},
                                color=alt.Gradient(
                                gradient='linear',
                                stops=[alt.GradientStop(color='white', offset=0),
                                        alt.GradientStop(color='darkgray', offset=1)],
                                x1=1, x2=1,
                                y1=1, y2=0)
                            )
        lower = lower.encode(x=alt.X('{0}:T'.format(data.index.name)),
                            y=alt.Y('{0}:Q'.format('close'), title=''))
        lower = lower.properties(height=20, width=600)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'
        # Concatenated Chart
        p = alt.vconcat(candlestick_chart, volume_chart, lower).configure_concat(spacing=0)
        return p
