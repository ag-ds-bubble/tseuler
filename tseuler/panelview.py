from .slab_views import DataSummaryPanel
from .slab_views import LinkedCategoricalFilterSlab
from .slab_views import PlottingPanel

import os
import panel as pn
pn.extension()

class PanelView:
    def __init__(self, data, datadesc, dt_freq, dt_format, catcols, targetcols, freq_conv_agg):
        # Initialisations
        self.initdata = data.copy()
        self.initdata.index.name = 'dt'
        self.view = None
        self.catcols = catcols
        self.targets = targetcols
        self.freq_conv_agg = freq_conv_agg
        # Initialise Slabs
        self.S1_summ = DataSummaryPanel(data=self.initdata, data_desc = datadesc, dt_freq=dt_freq)
        self.S2_lcfs = LinkedCategoricalFilterSlab(data=self.initdata.copy(), catcols = self.catcols)
        self.S3_pltp = PlottingPanel(filterObj=self.S2_lcfs, cat_cols = self.catcols, target_cols = self.targets,
                                     data_freq=dt_freq, freq_agg_func = self.freq_conv_agg)
        # Prepare Servable View
        self.cat_buttons = {}
        self._prep_view()

    def _prep_view(self):
        # Prepare the Top slab
        top_slab = self.S1_summ.get_view()

        # Prepare Categorical Mapping Slab
        filter_slab = self.S2_lcfs.get_view()

        # Prepare the Selction Slab
        plotting_slab = self.S3_pltp.get_view()

        # Combine Full View
        self.view = pn.Column(top_slab,
                              pn.layout.Divider(),
                              filter_slab,
                              pn.layout.Divider(),
                              plotting_slab,
                              background='white', height = 1180)

