#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:14:31 2021

@author: Carlos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def Precios_Stats(Table):
    T2 = pd.DataFrame(Table.iloc[:,1])
    c = Table.columns
    c = pd.DataFrame(c)
    for i in range(Table.shape[1]):
        if i>1:
            T2[[c.iloc[i,0]+' DIFF']] = Table.iloc[:,i] - Table.iloc[:,1]   
    T2 = T2.drop(T2.columns[0],axis=1)
    mu = pd.DataFrame(T2.mean())
    mu = mu.rename(columns={0:'Mu'})
    Std = pd.DataFrame(T2.std())
    Std = Std.rename(columns={0:'Std'})
    Stats = pd.concat([mu,Std], axis=1)
    return Stats
#%%
PrecioCerdo = pd.read_excel('CERDO.xlsx', sheet_name='Precio').fillna(0).replace(' ',0)
PCStats = Precios_Stats(PrecioCerdo)
PrecioHuevo = pd.read_excel('HUEVO.xlsx', sheet_name='Precio').fillna(0).replace(' ',0)
PHStats = Precios_Stats(PrecioHuevo)
#%%
with pd.ExcelWriter('Precios.xlsx') as writer:  
    PCStats.to_excel(writer, sheet_name='Metricas Precio Cerdo', index = True)
    PHStats.to_excel(writer, sheet_name='Metricas Huevo', index = True)

