import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpl
plt.rcParams['legend.facecolor'] = 'darkgray'


############################## STOCKS DATA ##############################
def process_stocks(path):
    data = pd.read_csv('Raw Data/stocks_data.csv', parse_dates=True)
    return data
    
def plot_stocks(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.set_index('Date').groupby('Name').close.plot(title='Closing Price of tickers', legend=True)
    _=plt.xlabel('Dates')
    _=plt.ylabel('Qty')


############################## RETAIL SALES ##############################
def process_retailsales(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    return data
    
def plot_retialsales(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.groupby('Store').Weekly_Sales.plot(title='Weekly Sales all stores')
    _=plt.xlabel('Dates')
    _=plt.ylabel('Qty')
    

############################## VISITORS TO 20 REGIONS ##############################
def process_20rvisitors(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.index=pd.to_datetime(data.index.str.replace(' ',''))
    data.columns = ['Regions', 'Visitors']
    data.index.name = 'Quarter'
    return data
    
def plot_20rvisitors(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=sns.lineplot(x='Quarter', y='Visitors', hue='Regions', data=data.reset_index())
    _=plt.title('Quaterly Vistors to 20 regions in Australlia')
    _=plt.ylabel('Visitors (Million)')
    
    

############################## ELECTRICITY PRODUCTION ##############################
def process_electricityprod(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['Production']
    return data
    
def plot_electricityprod(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='Australlian Monthly Electricity Production')
    _=plt.ylabel('Billion kWh')
    _=plt.xlabel('Dates')


############################## ANTI-DIABETIC DRUG SALES ##############################
def process_antidiabeticdrugs(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    return data
    
def plot_antidiabeticdrugs(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='AntiDiabetic Drug Sale')
    _=plt.ylabel('$ Mn')
    _=plt.xlabel('Dates')



############################## INDIA CPI ##############################
def process_indiacpi(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    return data
    
def plot_indiacpi(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    pltdata=data.set_index('Date').copy()
    pltdata=pltdata[pltdata.State.isin(['Delhi', 'Gujarat'])]
    pltdata=pltdata[pltdata.Description.isin(['Health', 'Meat and fish',
                                        'Clothing and footwear', 'Housing',
                                        'Fuel and light','Vegetables'])]

    _=pltdata.groupby(['State', 'Description']).Combined.plot(legend=True, marker='o', markersize=3)
    _=plt.legend(ncol=2)
    
    

############################## BEER PRODUCTION DATA ##############################
def process_beerproduction(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['MBP']
    return data
    
def plot_beerproduction(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(title='Monthly Beer Production in Australlia')

############################## AIR PASSENGERS ##############################
def process_airpassengers(path):
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    data.columns = ['Passengers']
    return data
    
def plot_airpassengers(data, style='ggplot'):
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['figure.figsize'] = (15,7)
    plt.style.use(style)
    _=data.plot(marker='o', markersize=3.5, title='Air Passengers')
    _=plt.ylabel("Air Passengers (1000's)")
    
    
    