import altair as alt

def tv_linkedScatterPlot(data, engine, xlabel, ylabel1, ylabel2):

    data = data.copy()
    data['year'] = data.apply(lambda x : x.name.year, axis=1)
    data.rename(columns={'plotY':xlabel, 'plotX1':ylabel1, 'plotX2':ylabel2}, inplace=True)
    interval = alt.selection(type='interval', encodings=['x', 'y'])

    base = alt.Chart(data)
    base = base.mark_point()

    lplot = base.encode(x=ylabel1,
                        y=alt.Y('{0}:Q'.format(xlabel), axis=alt.Axis(format='~s')),
                        color = alt.condition(interval, 'year',
                                            alt.value('lightgray')))
    lplot = lplot.properties(selection=interval, width = 260, height = 300)

    rplot = base.encode(x=ylabel2,
                        y=alt.Y('{0}:Q'.format(xlabel),title='', axis=alt.Axis(labels=False)),
                        color = alt.condition(interval, 'year',
                                            alt.value('lightgray')))
    rplot = rplot.properties(selection=interval, width = 260, height = 300)

    p = alt.hconcat(lplot, rplot, spacing = 0)

    return p



