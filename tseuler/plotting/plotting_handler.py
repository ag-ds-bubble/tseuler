# TODO : UV - Add Lag Chart
# TODO : UV - Add https://www.statsmodels.org/stable/graphics.html plots
# TODO : UV - Vegalite doesnt support boxplot selection yet https://github.com/altair-viz/altair/issues/2232
# TODO : UV - Manage frequency conversion for both the engines
# TODO : UV - FIX FOR YEAR END-MONTHS NOT IN ORDER.
# TODO : UV - CANDLESTICK, AREA & LINE Plots -> Currently dropping nan values from the df before plotting
        #        as it is currently making transform_aggregate undefined
        # -------

# TODO : BV - Update the long labels to smaller ones
# TODO : BV - Update y axis as the data is updated to be in the bounds

# TODO : ALL PLOTS WILL HAVE ~s NUMBER FORMATING (EVEN TEXTS IN LINE AND AREA PLOTS - UV & BV)

# TODO : alt.renderers.set_embed_options(theme='dark'), Dark theme


from ._univariate_plots import uv_linePlot, uv_areaPlot, uv_maSmoothPlot, uv_expSmoothPlot, uv_fourierSmoothPlot
from ._univariate_plots import uv_boxPlot, uv_histPlot, uv_ridgePlot, uv_seasonalPlot
from ._univariate_plots import uv_acfPlot, uv_pacfPlot, uv_qqPlot
from ._univariate_plots import uv_candlestickPlot


from ._bivariate_plots import bv_linePlot, bv_areaPlot
from ._bivariate_plots import bv_violinPlot
from ._bivariate_plots import bv_scatterPlot, bv_regPlot, bv_kdePlot, bv_jointPlot

from ._trivariate_plots import tv_linkedScatterPlot

from ..static import TSEULER_CONFIGS,TS_UV_PLOTS,TS_BV_PLOTS,TS_TV_PLOTS


def get_plot(plot_data, variate_type, plot_name, freq_variant, freq_agg, force_interactive,
             y_label = None, x1_label = None, x2_label = None):
            
    datapoints = plot_data.shape[0]
    plotting_engine = TSEULER_CONFIGS['plotting.default_engine']

    if plotting_engine == 'Interactive':
        plotting_engine = 'Interactive' if datapoints < 2500 else 'Static'

    if force_interactive:
        plotting_engine = 'Interactive'

    if variate_type == 'UV' and plot_name == TS_UV_PLOTS[0]:

        return uv_linePlot(data   = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label)

    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[1]:
        
        return uv_areaPlot(data   = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label)
    
    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[2]:
        
        return uv_boxPlot(data    = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label,
                           afreq = freq_variant)

    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[3]:

        return uv_ridgePlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label,
                           afreq = freq_variant)
                        
    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[4]:
        
        return uv_seasonalPlot(data = plot_data,
                                engine = plotting_engine,
                                xlabel = plot_data.index.name,
                                ylabel = x1_label,
                                afreq = freq_variant,
                                aggf = freq_agg)
                        
    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[5]:
        
        return uv_histPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label)

    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[6]:
        
        return uv_acfPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label)
    
    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[7]:
        
        return uv_pacfPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label)
    
    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[8]:
        
        return uv_qqPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel = x1_label)

    elif variate_type == 'UV' and plot_name == 'CandleStick Chart : Financial Analysis':
        
        return uv_candlestickPlot(data = plot_data,
                                  engine = plotting_engine,
                                  xlabel = plot_data.index.name,
                                  ylabel = x1_label)

    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[9]:
        
        return uv_maSmoothPlot(data = plot_data,
                                  engine = plotting_engine,
                                  xlabel = plot_data.index.name,
                                  ylabel = x1_label)

    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[10]:
        
        return uv_expSmoothPlot(data = plot_data,
                                engine = plotting_engine,
                                xlabel = plot_data.index.name,
                                ylabel = x1_label)

    elif variate_type == 'UV' and plot_name == TS_UV_PLOTS[11]:
        
        return uv_fourierSmoothPlot(data = plot_data,
                                    engine = plotting_engine,
                                    xlabel = plot_data.index.name,
                                    ylabel = x1_label)





    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[0]:

        return bv_linePlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel1 = y_label,
                           ylabel2 = x1_label)
    
    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[1]:
        
        return bv_areaPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel1 = y_label,
                           ylabel2 = x1_label)

    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[2]:
        
        return bv_violinPlot(data = plot_data,
                             engine = plotting_engine,
                             xlabel = plot_data.index.name,
                             ylabel1 = y_label,
                             ylabel2 = x1_label)

    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[3]:

        return bv_scatterPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel1 = y_label,
                           ylabel2 = x1_label)
    
    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[4]:
        
        return bv_regPlot(data = plot_data,
                           engine = plotting_engine,
                           xlabel = plot_data.index.name,
                           ylabel1 = y_label,
                           ylabel2 = x1_label)

    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[5]:
        
        return bv_kdePlot(data = plot_data,
                            engine = plotting_engine,
                            xlabel = plot_data.index.name,
                            ylabel1 = y_label,
                            ylabel2 = x1_label)

    elif variate_type == 'BV' and plot_name == TS_BV_PLOTS[6]:
        
        return bv_jointPlot(data = plot_data,
                             engine = plotting_engine,
                             xlabel = plot_data.index.name,
                             ylabel1 = y_label,
                             ylabel2 = x1_label)






    elif variate_type == 'TV' and plot_name == TS_TV_PLOTS[0]:
        
        return tv_linkedScatterPlot(data = plot_data,
                                    engine = plotting_engine,
                                    xlabel = y_label,
                                    ylabel1 = x1_label,
                                    ylabel2 = x2_label)   
    

