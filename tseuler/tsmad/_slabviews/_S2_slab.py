import panel as pn
import pandas as pd
import numpy as np

class SelectorDD:
    def __init__(self, name, data=None, prev_selector=None, next_selector=None):
        # Initialise Variables
        self.name = name
        self.prev_selector = prev_selector
        self.next_selector = next_selector
        self.selector = None
        self.data = data
        self.options = [None]
        self.value = None
        self.width = 100
        # Data Pipe and Options and Value Extraction
        self.update_filtereddata('init')
        # Call for update
        self.selector = pn.widgets.Select(name=self.name,
                                          options=self.options,
                                          width=self.width,
                                          value=self.value)
        self.selector.param.watch(self.update, 'value')
        
    def __str__(self):
        if self.next_selector and self.prev_selector:
            return f'{self.prev_selector.name}->[{self.name}]->{self.next_selector.name}'
        elif self.next_selector:
            return f'[{self.name}]->{self.next_selector.name}'
        elif self.prev_selector:
            return f'{self.prev_selector.name}->[{self.name}]'
        else:
            return f'[{self.name}]'
        
    def __repr__(self):
        if self.next_selector and self.prev_selector:
            return f'{self.prev_selector.name}->[{self.name}]->{self.next_selector.name}'
        elif self.next_selector:
            return f'[{self.name}]->{self.next_selector.name}'
        elif self.prev_selector:
            return f'{self.prev_selector.name}->[{self.name}]'
        
    def update(self, event):
        if event.type=='changed':
            self.update_filtereddata('event')
            self.update_call()
    
    def update_filtereddata(self, calltype='event'):
        # Get the data from the Previous Selector filtered df
        if self.prev_selector:
            self.parent_df = self.prev_selector.filtered_df.copy()
        else:
            self.parent_df = self.data.copy()
        # Get the options and vlaue
        self.options = sorted(self.parent_df[self.name].unique().tolist())
        self.value = self.options[0]
        self.width = int(np.clip(int(max([len(str(k)) for k in self.options])*11), 80, 150))
        if calltype == 'event':
            self.value = self.selector.value
        # Filter the dataframe
        self.filtered_df = self.parent_df[self.parent_df[self.name]==self.value].copy()
        
    def update_call(self):

        if self.prev_selector:
            self.parent_df = self.prev_selector.filtered_df.copy()
        else:
            self.parent_df = self.data.copy()
        self.selector.options = self.options
        self.selector.value = self.value
        self.selector.width = self.width
        if self.next_selector:
            self.next_selector.update_filtereddata('init')
            self.next_selector.update_call()
        
class LinkedCategoricalFilterSlab:
    def __init__(self, data, catcols):
        self.data = data.copy()
        self.catcols = catcols
        # Prepare the LinkedCatList
        self.linked_cat_list = []
        for eidx, ecatcol in enumerate(self.catcols):
            if eidx:
                sdd = SelectorDD(ecatcol, prev_selector=self.linked_cat_list[-1])
            else:
                sdd = SelectorDD(ecatcol, data=self.data.copy())
            self.linked_cat_list.append(sdd)
        # Add Next Selectors to each SelectorDD
        for i in range(len(self.linked_cat_list)-1):
            self.linked_cat_list[i].next_selector = self.linked_cat_list[i+1]
        
    def __str__(self):
        res = ''
        for es in self.linked_cat_list:
            res += es.name+'->'
        return res[:-2]

    def get_view(self):
        _desc = pn.Column('### Categorical Filters :', pn.pane.HTML('Dataframe categorical depth filtering', margin=(5, 5,5,5)))
        _desc = [_desc]+[k.selector for k in self.linked_cat_list]
        return pn.Row(*_desc, margin=(-20,5,-20,5))

    def get_current_filter_depth(self):
        return "".join([k.name+'('+str(k.selector.value)+')'+'→' for k in self.linked_cat_list])[:-1]
    
    def get_filtereddata(self):
        if self.catcols:
            return self.linked_cat_list[-1].filtered_df.copy()
        else:
            return self.data
  
