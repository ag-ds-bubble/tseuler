from ._slabviews import DataSummaryPanel
from ._slabviews import LinkedCategoricalFilterSlab
from ._slabviews import PlottingPanel

import os
import panel as pn
pn.extension()

class PanelView:
    def __init__(self, data, datadesc, dt_freq, dt_format,
                 catcols, targetcols, how_aggregate, force_interactive):
        # Initialisations
        self.initdata = data.copy()
        self.initdata.index.name = 'dt'
        self.view = None
        self.catcols = catcols
        self.targets = targetcols
        self.how_aggregate = how_aggregate
        self.force_interactive = force_interactive

        # Initialise Slabs
        self.S1_summ = DataSummaryPanel(data=self.initdata, data_desc = datadesc, dt_freq=dt_freq)
        self.S2_lcfs = LinkedCategoricalFilterSlab(data=self.initdata.copy(), catcols = self.catcols)
        self.S3_pltp = PlottingPanel(filterObj=self.S2_lcfs, cat_cols = self.catcols, target_cols = self.targets,
                                     data_freq=dt_freq, how_aggregate = self.how_aggregate, force_interactive = self.force_interactive)
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
                              background='white', height = 1220)

