#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:22:10 2021

@author: Carlos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
#%% Funcion
def RecoleccionStats(Table):
    RH = Table
    RH =  RH.groupby(['Bodega origen','Bodega destino','Fecha']).sum().reset_index()
    RH['Fecha2'] = [RH.Fecha[i-1] if i>0 else RH.Fecha[i] for i in range(len(RH))]
    RH['Periodo'] = [RH.Fecha[i]-RH.Fecha2[i] for i in range(len(RH))]
    RH['Periodo'] = pd.to_numeric(RH['Periodo'].dt.days, downcast='integer')
    RH['Periodo'] = [0 if RH['Periodo'][i] < 0 else RH['Periodo'][i] for i in range(len(RH))]
    RH = RH.drop(columns=['Fecha', 'Fecha2'])
    RHmu = RH.groupby(['Bodega origen','Bodega destino']).mean()
    RHmu = RHmu.rename(columns = {'Cantidad': 'Cantidad mu', 'Kilos':'Kilos mu','Periodo':'Periodo mu'})
    RHstd = RH.groupby(['Bodega origen','Bodega destino']).std()
    RHstd = RHstd.rename(columns = {'Cantidad': 'Cantidad std', 'Kilos':'Kilos std','Periodo':'Periodo std'})
    RHmin = RH.groupby(['Bodega origen','Bodega destino']).min()
    RHmin = RHmin.rename(columns = {'Cantidad': 'Cantidad min', 'Kilos':'Kilos min','Periodo':'Periodo min'})
    RHmax = RH.groupby(['Bodega origen','Bodega destino']).max()
    RHmax = RHmin.rename(columns = {'Cantidad': 'Cantidad max', 'Kilos':'Kilos max','Periodo':'Periodo max'})
    
    RHmuO = RH.groupby(['Bodega origen']).mean()
    RHmuO = RHmuO.rename(columns = {'Cantidad': 'Cantidad mu', 'Kilos':'Kilos mu','Periodo':'Periodo mu'})
    RHstdO = RH.groupby(['Bodega origen']).std()
    RHstdO = RHstdO.rename(columns = {'Cantidad': 'Cantidad std', 'Kilos':'Kilos std','Periodo':'Periodo std'})
    RHminO = RH.groupby(['Bodega origen']).min()
    RHminO = RHminO.rename(columns = {'Cantidad': 'Cantidad min', 'Kilos':'Kilos min','Periodo':'Periodo min'})
    RHmaxO = RH.groupby(['Bodega origen']).max()
    RHmaxO = RHmaxO.rename(columns = {'Cantidad': 'Cantidad max', 'Kilos':'Kilos max','Periodo':'Periodo max'})
    StatsOD = pd.concat([RHmu,RHstd,RHmin,RHmax], axis = 1).reset_index()
    StatsO = pd.concat([RHmuO,RHstdO,RHminO,RHmaxO], axis = 1).reset_index()
    return StatsO

def Acotar(StatsO,RH1):
    infC = StatsO['Cantidad mu'] - StatsO['Cantidad std']
    supC = StatsO['Cantidad mu'] + StatsO['Cantidad std']
    infK = StatsO['Kilos mu'] - StatsO['Kilos std']
    supK = StatsO['Kilos mu'] + StatsO['Kilos std']
    index_to_drop = []
    for i in range(len(StatsO)):
        for j in range(len(RH1)):
            if StatsO['Bodega origen'][i] == RH1['Bodega origen'][j] and \
                (RH1['Cantidad'][j] <= infC[i] or RH1['Cantidad'][j] >= supC[i]) and\
                 (RH1['Kilos'][j] <= infK[i] or RH1['Kilos'][j] >= supK[i]):
                    index_to_drop.append(j)  
    RH1 = RH1.drop(index_to_drop, axis = 0).reset_index(drop=True)
    return RH1                
    
#%% Carga datos Y analizar
RH1 = pd.read_excel('HUEVO.xlsx', sheet_name='RECOLECCION').drop(columns=['Código','No. Cajas','Tamaño Caja',
                                                                         'Folio','Producto','Lote'])
Stats1 = RecoleccionStats(RH1)
RH2 = Acotar(Stats1,RH1)
Stats2 = RecoleccionStats(RH2)
RH3 = Acotar(Stats2,RH2)
Stats3 = RecoleccionStats(RH3)
#%%
with pd.ExcelWriter('Recoleccion.xlsx') as writer:  
 #   StatsOD.to_excel(writer, sheet_name='Recoleccion Origen y Destino', index = True)
    Stats3.to_excel(writer, sheet_name='Recoleccion Metricas', index = True)