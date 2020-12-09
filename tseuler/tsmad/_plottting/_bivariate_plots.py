import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import panel as pn
import pandas as pd
import numpy as np

plt.style.use('ggplot')
alt.data_transformers.disable_max_rows()


def bv_linePlot(data, engine, xlabel, ylabel1, ylabel2):
    data = data.copy() 
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)

    if engine == 'Static':
        fig, axes = plt.subplots(figsize=(9,6))

        axes.plot(data[ylabel1], marker='o', markersize=1.5)
        axes.legend([ylabel1])
        axes_r = axes.twinx()
        axes_r.plot(data[ylabel2], marker='o', markersize=1.5, color='orange')
        axes_r.legend([ylabel2], loc=1)

        axes.set_xlabel(xlabel, fontsize = 15)
        axes.set_ylabel(ylabel1, fontsize = 15)
        axes_r.set_ylabel(ylabel2, fontsize = 15)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
        
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        data=data.dropna()
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'], name='isel')
        # Base Plot
        base = alt.Chart(data.reset_index())
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                        tooltip = ylabel1)
        base = base.properties(width = 580, height = 275)
        # Upper Plot
        upper1 = base.mark_line(color='#3d84ba')
        upper1 = upper1.encode(x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title=''),
                            y = alt.Y('{0}:Q'.format(ylabel1), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        upper2 = base.mark_line(color='#f57542')
        upper2 = upper2.encode(x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title=''),
                            y = alt.Y('{0}:Q'.format(ylabel2), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        # Lower Plot
        lower = base.mark_area(line={'color':'darkgray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgray', offset=1)],
                x1=1, x2=1,
                y1=1, y2=0
            ))
        lower = lower.encode(y=alt.Y('{0}:Q'.format(ylabel1), title='', axis=None))
        lower = lower.properties(height=20)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'
        # Base Statistics1
        base_stat1 = upper1.transform_filter(brush)
        base_stat1 = base_stat1.transform_aggregate(Mean1='mean({0})'.format(ylabel1),
                                                    StdDev1='stdev({0})'.format(ylabel1),
                                                    Var1='variance({0})'.format(ylabel1))
        label_stat1 = base_stat1.transform_calculate(stat_label1="'Mean = ' + format(datum.Mean1, '~s') + \
                                                    '; Standard Deviation = ' + format(datum.StdDev1, '~s') +\
                                                    '; Variance = ' + format(datum.Var1, '~s')")
        label_stat1 = label_stat1.mark_text(align='left', baseline='bottom', color='#3d84ba')
        label_stat1 = label_stat1.encode(x=alt.value(0.0), y=alt.value(12.0), text=alt.Text('stat_label1:N'))
        # Base Statistics2
        base_stat2 = upper2.transform_filter(brush)
        base_stat2 = base_stat2.transform_aggregate(Mean2='mean({0})'.format(ylabel2),
                                                    StdDev2='stdev({0})'.format(ylabel2),
                                                    Var2='variance({0})'.format(ylabel2))
        label_stat2 = base_stat2.transform_calculate(stat_label1="'Mean = ' + format(datum.Mean2, '~s') + \
                                                    '; Standard Deviation = ' + format(datum.StdDev2, '~s') +\
                                                    '; Variance = ' + format(datum.Var2, '~s')")
        label_stat2 = label_stat2.mark_text(align='left', baseline='bottom', color='#f57542')
        label_stat2 = label_stat2.encode(x=alt.value(0.0), y=alt.value(25.0), text=alt.Text('stat_label1:N'))
        upper1 = upper1 + label_stat1
        upper2 = upper2 + label_stat2
        upper = (upper1+upper2).resolve_scale(y='independent')
        ## Y LABEL 1
        # Values
        _ymean_uu1 = data[ylabel1].max()
        _ymean1 = data[ylabel1].mean()
        # Inspired from :- https://stats.stackexchange.com/a/350278
        _maxvar_in_slice1 = ((data[ylabel1].max()-data[ylabel1].min())/2)**2
        _ystd_uu1 = np.sqrt(_maxvar_in_slice1)
        _ystd1 = data[ylabel1].std()
        _yvar_uu1 = _maxvar_in_slice1
        _yvar1 = data[ylabel1].var()

        # Stat Bar Base
        stats_barbase1 = base_stat1.mark_bar(color='#3d84ba')
        stats_barbase1 = stats_barbase1.properties(width = 188, height = 20)
        # Mean Bar
        mean_bar1 = stats_barbase1.encode(x=alt.X('Mean1:Q', title='',
                                                scale=alt.Scale(domain=[-_ymean_uu1,_ymean_uu1]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totmean_line1 = alt.Chart(pd.DataFrame({'x': [_ymean1]}))
        totmean_line1 = totmean_line1.mark_rule(color='red', size=5)
        totmean_line1 = totmean_line1.encode(x='x')
        mean_bar1 += totmean_line1
        # Standard Deviation Bar
        std_bar1 = stats_barbase1.encode(x=alt.X('StdDev1:Q', title='',
                                                scale=alt.Scale(domain=[-_ystd_uu1,_ystd_uu1]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totstd_line1 = alt.Chart(pd.DataFrame({'x': [_ystd1]}))
        totstd_line1 = totstd_line1.mark_rule(color='red', size=5)
        totstd_line1 = totstd_line1.encode(x='x')
        std_bar1 += totstd_line1
        # Variance Bar
        var_bar1 = stats_barbase1.encode(x=alt.X('Var1:Q', title='',
                                                scale=alt.Scale(domain=[-_yvar_uu1,_yvar_uu1]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totvar_line1 = alt.Chart(pd.DataFrame({'x': [_yvar1]}))
        totvar_line1 = totvar_line1.mark_rule(color='red', size=5)
        totvar_line1 = totvar_line1.encode(x='x')
        var_bar1 += totvar_line1
        ## Y LABEL 2
        # Values
        _ymean_uu2 = data[ylabel2].max()
        _ymean2 = data[ylabel2].mean()
        # Inspired from :- https://stats.stackexchange.com/a/350278
        _maxvar_in_slice2 = ((data[ylabel2].max()-data[ylabel2].min())/2)**2
        _ystd_uu2 = np.sqrt(_maxvar_in_slice2)
        _ystd2 = data[ylabel2].std()
        _yvar_uu2 = _maxvar_in_slice2
        _yvar2 = data[ylabel2].var()

        # Stat Bar Base
        stats_barbase2 = base_stat2.mark_bar(color='#f57542')
        stats_barbase2 = stats_barbase2.properties(width = 188, height = 20)
        # Mean Bar
        mean_bar2 = stats_barbase2.encode(x=alt.X('Mean2:Q', title='Mean',
                                                scale=alt.Scale(domain=[-_ymean_uu2,_ymean_uu2]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totmean_line2 = alt.Chart(pd.DataFrame({'x': [_ymean2]}))
        totmean_line2 = totmean_line2.mark_rule(color='red', size=5)
        totmean_line2 = totmean_line2.encode(x='x')
        mean_bar2 += totmean_line2
        # Standard Deviation Bar
        std_bar2 = stats_barbase2.encode(x=alt.X('StdDev2:Q', title='Std',
                                                scale=alt.Scale(domain=[-_ystd_uu2,_ystd_uu2]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totstd_line2 = alt.Chart(pd.DataFrame({'x': [_ystd2]}))
        totstd_line2 = totstd_line2.mark_rule(color='red', size=5)
        totstd_line2 = totstd_line2.encode(x='x')
        std_bar2 += totstd_line2
        # Variance Bar
        var_bar2 = stats_barbase2.encode(x=alt.X('Var2:Q', title='Var',
                                                scale=alt.Scale(domain=[-_yvar_uu2,_yvar_uu2]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totvar_line2 = alt.Chart(pd.DataFrame({'x': [_yvar2]}))
        totvar_line2 = totvar_line2.mark_rule(color='red', size=5)
        totvar_line2 = totvar_line2.encode(x='x')
        var_bar2 += totvar_line2
        # Concatenated
        p = alt.vconcat(upper, mean_bar1|std_bar1|var_bar1, mean_bar2|std_bar2|var_bar2, lower).configure_concat(spacing=2)
        p = p.configure_axisLeft(labelColor = '#3d84ba', titleColor = '#3d84ba')
        p = p.configure_axisRight(labelColor = '#f57542', titleColor = '#f57542')

        return p


def bv_areaPlot(data, engine, xlabel, ylabel1, ylabel2):
    data = data.copy() 
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)

    if engine == 'Static':
        fig, axes = plt.subplots(figsize=(9,6))

        _index = data.index.tolist()

        axes.fill_between(_index, data[ylabel1].values)
        axes.legend([ylabel1], loc=0)
        axes_r = axes.twinx()
        axes_r.fill_between(_index, data[ylabel2].values, color='orange')
        axes_r.legend([ylabel2], loc=0)

        axes.set_xlabel(xlabel, fontsize = 15)
        axes.set_ylabel(ylabel1, fontsize = 15)
        axes_r.set_ylabel(ylabel2, fontsize = 15)
        axes.grid(b=True, which='major', color='k', linewidth=0.25)
                
        plt.close()
        return pn.pane.Matplotlib(fig, tight=True)
    
    elif engine == 'Interactive':
        data=data.dropna()
        # Selection Brush
        brush = alt.selection(type='interval', encodings=['x'], name='isel')
        # Base Plot
        base = alt.Chart(data.reset_index())
        base = base.encode(x = alt.X('{0}:T'.format(data.index.name), title=''),
                        tooltip = ylabel1)
        base = base.properties(width = 580, height = 275)
        # Upper Plot
        upper1 = base.mark_area(line={'color':'#3d84ba'},
                                    color=alt.Gradient(
                                        gradient='linear',
                                        stops=[alt.GradientStop(color='white', offset=0),
                                            alt.GradientStop(color='#3d84ba', offset=1)],
                                        x1=1, x2=1,
                                        y1=1, y2=0
                                    ))
        upper1 = upper1.encode(x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title=''),
                               y = alt.Y('{0}:Q'.format(ylabel1), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        upper2 = base.mark_area(line={'color':'#f57542'},
                                    color=alt.Gradient(
                                        gradient='linear',
                                        stops=[alt.GradientStop(color='white', offset=0),
                                            alt.GradientStop(color='#f57542', offset=1)],
                                        x1=1, x2=1,
                                        y1=1, y2=0
                                    ))
        upper2 = upper2.encode(x = alt.X('{0}:T'.format(data.index.name), scale=alt.Scale(domain=brush), title=''),
                            y = alt.Y('{0}:Q'.format(ylabel2), scale=alt.Scale(zero=False), axis=alt.Axis(format='~s')))
        # Lower Plot
        lower = base.mark_area(line={'color':'darkgray'},
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgray', offset=1)],
                x1=1, x2=1,
                y1=1, y2=0
            ))

        lower = lower.encode(y=alt.Y('{0}:Q'.format(ylabel1), title='', axis=None))
        lower = lower.properties(height=20)
        lower = lower.add_selection(brush)
        lower.encoding.x.title = 'Interval Selection'

        # Base Statistics1
        base_stat1 = upper1.transform_filter(brush)
        base_stat1 = base_stat1.transform_aggregate(Mean1='mean({0})'.format(ylabel1),
                                                    StdDev1='stdev({0})'.format(ylabel1),
                                                    Var1='variance({0})'.format(ylabel1))
        label_stat1 = base_stat1.transform_calculate(stat_label1="'Mean = ' + format(datum.Mean1, '~s') + \
                                                    '; Standard Deviation = ' + format(datum.StdDev1, '~s') +\
                                                    '; Variance = ' + format(datum.Var1, '~s')")
        label_stat1 = label_stat1.mark_text(align='left', baseline='bottom', color='#3d84ba')
        label_stat1 = label_stat1.encode(x=alt.value(0.0), y=alt.value(12.0), text=alt.Text('stat_label1:N'))
        # Base Statistics2
        base_stat2 = upper2.transform_filter(brush)
        base_stat2 = base_stat2.transform_aggregate(Mean2='mean({0})'.format(ylabel2),
                                                    StdDev2='stdev({0})'.format(ylabel2),
                                                    Var2='variance({0})'.format(ylabel2))
        label_stat2 = base_stat2.transform_calculate(stat_label1="'Mean = ' + format(datum.Mean2, '~s') + \
                                                    '; Standard Deviation = ' + format(datum.StdDev2, '~s') +\
                                                    '; Variance = ' + format(datum.Var2, '~s')")
        label_stat2 = label_stat2.mark_text(align='left', baseline='bottom', color='#f57542')
        label_stat2 = label_stat2.encode(x=alt.value(0.0), y=alt.value(25.0), text=alt.Text('stat_label1:N'))

        upper1 = upper1 + label_stat1
        upper2 = upper2 + label_stat2
        upper = (upper1+upper2).resolve_scale(y='independent')

        ## Y LABEL 1
        # Values
        _ymean_uu1 = data[ylabel1].max()
        _ymean1 = data[ylabel1].mean()
        # Inspired from :- https://stats.stackexchange.com/a/350278
        _maxvar_in_slice1 = ((data[ylabel1].max()-data[ylabel1].min())/2)**2
        _ystd_uu1 = np.sqrt(_maxvar_in_slice1)
        _ystd1 = data[ylabel1].std()
        _yvar_uu1 = _maxvar_in_slice1
        _yvar1 = data[ylabel1].var()
        # Stat Bar Base
        stats_barbase1 = base_stat1.mark_bar(color='#3d84ba')
        stats_barbase1 = stats_barbase1.properties(width = 188, height = 20)
        # Mean Bar
        mean_bar1 = stats_barbase1.encode(x=alt.X('Mean1:Q', title='',
                                                scale=alt.Scale(domain=[-_ymean_uu1,_ymean_uu1]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totmean_line1 = alt.Chart(pd.DataFrame({'x': [_ymean1]}))
        totmean_line1 = totmean_line1.mark_rule(color='red', size=5)
        totmean_line1 = totmean_line1.encode(x='x')
        mean_bar1 += totmean_line1
        # Standard Deviation Bar
        std_bar1 = stats_barbase1.encode(x=alt.X('StdDev1:Q', title='',
                                                scale=alt.Scale(domain=[-_ystd_uu1,_ystd_uu1]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totstd_line1 = alt.Chart(pd.DataFrame({'x': [_ystd1]}))
        totstd_line1 = totstd_line1.mark_rule(color='red', size=5)
        totstd_line1 = totstd_line1.encode(x='x')
        std_bar1 += totstd_line1
        # Variance Bar
        var_bar1 = stats_barbase1.encode(x=alt.X('Var1:Q', title='',
                                                scale=alt.Scale(domain=[-_yvar_uu1,_yvar_uu1]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totvar_line1 = alt.Chart(pd.DataFrame({'x': [_yvar1]}))
        totvar_line1 = totvar_line1.mark_rule(color='red', size=5)
        totvar_line1 = totvar_line1.encode(x='x')
        var_bar1 += totvar_line1

        ## Y LABEL 2
        # Values
        _ymean_uu2 = data[ylabel2].max()
        _ymean2 = data[ylabel2].mean()
        # Inspired from :- https://stats.stackexchange.com/a/350278
        _maxvar_in_slice2 = ((data[ylabel2].max()-data[ylabel2].min())/2)**2
        _ystd_uu2 = np.sqrt(_maxvar_in_slice2)
        _ystd2 = data[ylabel2].std()
        _yvar_uu2 = _maxvar_in_slice2
        _yvar2 = data[ylabel2].var()
        # Stat Bar Base
        stats_barbase2 = base_stat2.mark_bar(color='#f57542')
        stats_barbase2 = stats_barbase2.properties(width = 188, height = 20)
        # Mean Bar
        mean_bar2 = stats_barbase2.encode(x=alt.X('Mean2:Q', title='Mean',
                                                scale=alt.Scale(domain=[-_ymean_uu2,_ymean_uu2]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totmean_line2 = alt.Chart(pd.DataFrame({'x': [_ymean2]}))
        totmean_line2 = totmean_line2.mark_rule(color='red', size=5)
        totmean_line2 = totmean_line2.encode(x='x')
        mean_bar2 += totmean_line2
        # Standard Deviation Bar
        std_bar2 = stats_barbase2.encode(x=alt.X('StdDev2:Q', title='Std',
                                                scale=alt.Scale(domain=[-_ystd_uu2,_ystd_uu2]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totstd_line2 = alt.Chart(pd.DataFrame({'x': [_ystd2]}))
        totstd_line2 = totstd_line2.mark_rule(color='red', size=5)
        totstd_line2 = totstd_line2.encode(x='x')
        std_bar2 += totstd_line2
        # Variance Bar
        var_bar2 = stats_barbase2.encode(x=alt.X('Var2:Q', title='Var',
                                                scale=alt.Scale(domain=[-_yvar_uu2,_yvar_uu2]),
                                                axis=alt.Axis(format='~s')), y=alt.value(10.5))
        totvar_line2 = alt.Chart(pd.DataFrame({'x': [_yvar2]}))
        totvar_line2 = totvar_line2.mark_rule(color='red', size=5)
        totvar_line2 = totvar_line2.encode(x='x')
        var_bar2 += totvar_line2

        # Concatenated
        # p = alt.vconcat(upper+label_stat, mean_bar|std_bar|var_bar, lower).configure_concat(spacing=2)
        p = alt.vconcat(upper, mean_bar1|std_bar1|var_bar1, mean_bar2|std_bar2|var_bar2, lower).configure_concat(spacing=2)
        p = p.configure_axisLeft(labelColor = '#3d84ba', titleColor = '#3d84ba')
        p = p.configure_axisRight(labelColor = '#f57542', titleColor = '#f57542')

        return p


def bv_violinPlot(data, engine, xlabel, ylabel1, ylabel2):

    data = data.copy() 
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)
    data = data[[ylabel1, ylabel2]].copy()

    if engine == 'Static':
        plt.rcParams['figure.figsize'] = (9,6)
        fig = sns.violinplot(x = 'variable', y = 'value', data = data.melt())
        fig.grid(b=True, which='major', color='k', linewidth=0.25)
        fig.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig.figure, tight=True)

    elif engine == 'Interactive':
        p = alt.Chart(data.dropna().melt())
        p = p.transform_density('value',
                                as_=['value', 'density'],
                                groupby=['variable'])
        p = p.mark_area(orient='horizontal').encode(
            y=alt.Y('value:Q', axis=alt.Axis(format='~s')),
            color='variable:N',
            x=alt.X('density:Q', stack='center',
                    impute=None, title=None,
                    axis=alt.Axis(labels=False, values=[0],grid=False, ticks=True)),
            column=alt.Column('variable:N', header=alt.Header(titleOrient='bottom',
                                                            labelOrient='bottom',
                                                            labelPadding=0)))
        p = p.properties(width = 200, height = 280)
        p = p.configure_facet(spacing=0)
        p = p.configure_view(stroke=None)
        return p


def bv_scatterPlot(data, engine, xlabel, ylabel1, ylabel2):

    data = data.dropna().copy() 
    # data['year'] = data.apply(lambda x : x.name.year, axis=1)
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)
    if engine == 'Static':
        plt.rcParams['figure.figsize'] = (9,6)
        fig = sns.scatterplot(x=ylabel1, y=ylabel2, data=data)
        fig.grid(b=True, which='major', color='k', linewidth=0.25)
        fig.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig.figure, tight=True)

    elif engine == 'Interactive':
        p = alt.Chart(data.dropna())
        p = p.mark_point(size=30)
        p = p.encode(x=alt.X('{0}:Q'.format(ylabel1), axis=alt.Axis(format='~s'), scale = alt.Scale(zero=False)),
                     y=alt.Y('{0}:Q'.format(ylabel2), axis=alt.Axis(format='~s'), scale = alt.Scale(zero=False)),
                     color=alt.Color('anfreq_label'), tooltip=[ylabel1,ylabel2])
        p = p.properties(width = 520, height = 320)
        p = p.interactive()
        return p


def bv_regPlot(data, engine, xlabel, ylabel1, ylabel2):

    data = data.dropna().copy()
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)

    if engine == 'Static':
        plt.rcParams['figure.figsize'] = (9,6)
        fig = sns.regplot(x = ylabel1, y = ylabel2, data = data, 
                            line_kws={'color':'maroon'},
                            scatter_kws={'edgecolor' : 'k'})
        fig.grid(b=True, which='major', color='k', linewidth=0.25)
        fig.grid(b=True, which='minor', color='k', linewidth=0.125)
        plt.close()
        return pn.pane.Matplotlib(fig.figure, tight=True)

    elif engine == 'Interactive':
        p = alt.Chart(data.dropna())
        p = p.mark_point(size=30)
        p = p.encode(x=alt.X('{0}:Q'.format(ylabel1), axis=alt.Axis(format='~s'), scale = alt.Scale(zero=False)),
                     y=alt.Y('{0}:Q'.format(ylabel2), axis=alt.Axis(format='~s'), scale = alt.Scale(zero=False)),
                     color=alt.Color('anfreq_label'), tooltip=[ylabel1,ylabel2])
        p = p + p.transform_regression(ylabel1, ylabel2).mark_line(color='maroon')
        p = p.properties(width = 520, height = 320)
        return p


def bv_kdePlot(data, engine, xlabel, ylabel1, ylabel2):

    data = data.copy() 
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)

    plt.rcParams['figure.figsize'] = (9,6)
    fig = sns.kdeplot(x=ylabel1, y=ylabel2, data=data.dropna(),
                        cmap = 'Blues', shade = True, rug = True)
    fig.grid(b=True, which='major', color='k', linewidth=0.25)
    fig.grid(b=True, which='minor', color='k', linewidth=0.125)
    plt.close()
    return pn.pane.Matplotlib(fig.figure, tight=True)


def bv_jointPlot(data, engine, xlabel, ylabel1, ylabel2):
    data = data.dropna().copy()
    data.rename(columns={'plotY':ylabel1, 'plotX1':ylabel2}, inplace=True)

    if engine == 'Static':
        plt.rcParams['figure.figsize'] = (9,6)
        jp = sns.jointplot(x=ylabel1, y=ylabel2, data=data, hue='anfreq_label')
        plt.close()
        return pn.pane.Matplotlib(jp.fig, tight=True)

    elif engine == 'Interactive':
        brush = alt.selection(type='interval')
        base = alt.Chart(data)
        base = base.encode(x=alt.X('{0}:Q'.format(ylabel1), axis=alt.Axis(format='~s'), scale = alt.Scale(zero=False)),
                        y=alt.Y('{0}:Q'.format(ylabel2), axis=alt.Axis(format='~s'), scale = alt.Scale(zero=False)),
                        color=alt.condition(brush, 'anfreq_label:O', alt.value('grey'), scale=alt.Scale(scheme='set1')),
                        )
        base = base.properties(width = 420, height = 300)
        base = base.add_selection(brush)

        points = base.mark_point(size=10)

        density_x = base.transform_filter(brush)
        density_x = density_x.transform_density(density=ylabel1,groupby=['anfreq_label'],
                                                steps=20,as_=[ylabel1, 'Density1'])
        density_x = density_x.mark_area(orient='vertical', opacity=0.5)
        density_x = density_x.encode(x = alt.X('{0}:Q'.format(ylabel1), title='', axis=alt.Axis(format='~s')),
                                     y = alt.Y('Density1:Q', title='Density', axis=alt.Axis(format='~s')),
                                     color=alt.Color('anfreq_label:O', scale=alt.Scale(scheme='set1')))
        density_x = density_x.properties(height=50)

        density_y = base.transform_filter(brush)
        density_y = density_y.transform_density(density=ylabel2,groupby=['anfreq_label'],
                                                steps=20, as_=[ylabel2, 'Density2'])
        density_y = density_y.mark_area(orient='horizontal', opacity=0.5)
        density_y = density_y.encode(x=alt.X('Density2:Q', title='Density', axis=alt.Axis(labelAngle=90, format='~s')),
                                     y=alt.Y('{0}:Q'.format(ylabel2), title='', axis=alt.Axis(format='~s')),
                                     color=alt.Color('anfreq_label:O', scale=alt.Scale(scheme='set1')))
        density_y = density_y.properties(width=50)

        p = density_x & (points | density_y)
        return p

