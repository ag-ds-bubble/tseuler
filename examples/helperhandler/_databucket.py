import pandas as pd
from tqdm.notebook import tqdm
from ._individual_funcs import *

############################## DATA PATHS ##############################
# Retail Sales Data
retail_sales_datapath = 'Raw Data/retail_data.csv'
# Consumer Price Index for India with Groups and Subgroups
cpi_datapath = 'Raw Data/cpi_states_and_groups.csv'
# Total Air Passengers
airpassengers_datapath = 'Raw Data/AirPassengers.csv'
# Australlian Monthly Beer Production
beerprod_datapath = 'Raw Data/Australlian_Monthly_Beer_Production.csv'
# Australlian Electricity Priduction
elecprod_datapath = 'Raw Data/Australlian_Monthly_Electricity_Production_BillionKWh.csv'
# AntiDiabetic DrugSales
antidiabetic_datapath = 'Raw Data/AntiDiabetic_DrugSales_Mn.csv'
# Australlian Visitors
visitors20r_datapath = 'Raw Data/Australlia_Vistors_20Regions_Million.csv'
# Stocks Data
stocks_datapath = 'Raw Data/stocks_data.csv'


class DataProcessingClass:
    def __init__(self, raw_datapath, long_desc, short_desc, processing_func, plotfunc):
        self.rpath = raw_datapath
        self.long_description = long_desc
        self.short_description = short_desc
        self._processing_func = processing_func
        self._plot_func = plotfunc
        
        self.data = None
        
    def run_processingfunc(self):
        self.data = self._processing_func(self.rpath)
        
    def exploratory_plot(self):
        self._plot_func(self.data, style='ggplot')
        

class DataHolderClass:
    def __init__(self):
        self.bucket = {}
        self.dataDf = pd.DataFrame(columns=['Handle', 'Short Description'])
        
    def add_data(self, data_key, dpc_ob):
        self.bucket[data_key] = dpc_ob
        self.dataDf = self.dataDf.append({'Handle':data_key,
                                          'Short Description':dpc_ob.short_description},
                                          ignore_index=True)

    def load_data(self):
        for _, edpc in tqdm(self.bucket.items()):
            edpc.run_processingfunc()
            
            
dpc1 = DataProcessingClass(raw_datapath=airpassengers_datapath, 
                           long_desc = """Air Passengers (Monthly), Numbers in 1000's, from 1949 to 1960""",
                           short_desc = "Air Passengers",
                           processing_func = process_airpassengers,
                           plotfunc = plot_airpassengers)

dpc2 = DataProcessingClass(raw_datapath=cpi_datapath, 
                           long_desc = """India's Consumer Price index Data (Monthly), with groups and subgroups starting from 2013 to 2020""",
                           short_desc = "India CPI",
                           processing_func = process_indiacpi,
                           plotfunc = plot_indiacpi)


dpc3 = DataProcessingClass(raw_datapath=beerprod_datapath, 
                           long_desc = """Australlian Beer Production (Monthly), from , Numbers in Million Barrels, from 1956 to 1995""",
                           short_desc = "Beer Production",
                           processing_func = process_beerproduction,
                           plotfunc = plot_beerproduction)

dpc4 = DataProcessingClass(raw_datapath=antidiabetic_datapath, 
                           long_desc = """Anti-Diabetic Drug Sales (Monthly), prices in $ Million, from 1992 to 2008""",
                           short_desc = "AntiDiabetic Drug Sale",
                           processing_func = process_antidiabeticdrugs,
                           plotfunc = plot_antidiabeticdrugs)

dpc5 = DataProcessingClass(raw_datapath=elecprod_datapath, 
                           long_desc = """Australlian Electricity Production (Monthly) with Missing Values, Numbers in billion kWh, from 1956 to 1995""",
                           short_desc = "Electricity Production",
                           processing_func = process_electricityprod,
                           plotfunc = plot_electricityprod)


dpc6 = DataProcessingClass(raw_datapath=visitors20r_datapath, 
                           long_desc = """Number of Visitors in 20 Regions of Australlia (Quaterly), in Million, from 1998 to 2016""",
                           short_desc = "Visitors to 20 Regions",
                           processing_func = process_20rvisitors,
                           plotfunc = plot_20rvisitors)

dpc7 = DataProcessingClass(raw_datapath=retail_sales_datapath, 
                           long_desc = """Retail Sales Data (Weekly) columns with the name `markdown` represent data which was masked (https://www.kaggle.com/manjeetsingh/retaildataset), from 2010 to 2012""",
                           short_desc = "Retail Sales",
                           processing_func = process_retailsales,
                           plotfunc = plot_retialsales)

dpc8 = DataProcessingClass(raw_datapath=stocks_datapath, 
                           long_desc = """Stock Ticker Data (Custom Buisness Days), from 2010 to 2012""",
                           short_desc = "Stocks Data",
                           processing_func = process_stocks,
                           plotfunc = plot_stocks)

    
dataHolder = DataHolderClass()
dataHolder.add_data(data_key='airp_data', dpc_ob=dpc1)
dataHolder.add_data(data_key='india_cpi', dpc_ob=dpc2)
dataHolder.add_data(data_key='beer_prod', dpc_ob=dpc3)
dataHolder.add_data(data_key='anti_diabetic', dpc_ob=dpc4)
dataHolder.add_data(data_key='aus_elecprod', dpc_ob=dpc5)
dataHolder.add_data(data_key='visitor_20r', dpc_ob=dpc6)
dataHolder.add_data(data_key='retail_sales', dpc_ob=dpc7)
dataHolder.add_data(data_key='stocks_data', dpc_ob=dpc8)


