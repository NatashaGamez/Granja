#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:52:58 2021

@author: Carlos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
#%% Funciones
def Stats(Table):
    mu = Table.groupby(['Categoría']).mean().reset_index()
    std = Table.groupby(['Categoría']).std().reset_index()
    S = pd.concat([mu,std],axis=0).reset_index(drop=True)
    S['Medida'] = ['mu','std']
    return mu, std, S

def Acotar(mu,std,Table):
    infK = mu['Kilo'] - std['Kilo']
    supK = mu['Kilo'] +  std['Kilo']
    infC = mu['Costo']
    supU = mu['Utilidad Bruta']
    index_to_drop = []
    for i in range(len(mu)):
        for j in range(len(Table)):
            if mu['Categoría'][i] == 'Cerdos':
                infP =  mu['Peso'] - std['Peso']
                supP = mu['Peso'] + std['Peso']
                infTE = mu['TiempoEngorda'] - std['TiempoEngorda']
                supTE = mu['TiempoEngorda'] + std['TiempoEngorda']
                if Table['Peso'][j] <= infP[i] or Table['Peso'][j] >= supP[i]:
                            index_to_drop.append(j)
            if mu['Categoría'][i] == 'Borregos':
                infP = mu['Peso'] - std['Peso']
                supP = mu['Peso'] + std['Peso']
                if Table['Peso'][j] <= infP[i] or Table['Peso'][j] >= supP[i] and \
                        Table['Costo'][j] >= infC[i] and Table['Utilidad Bruta'][j] <= supU[i]:
                            index_to_drop.append(j)
            if mu['Categoría'][i] == 'Huevo' and  Table['Kilo'][j] <= infK[i] or Table['Kilo'][j] >= supK[i]:
                             index_to_drop.append(j)       
    Table = Table.drop(index_to_drop, axis=0).reset_index(drop=True)
    index_to_drop = []
    for i in range(len(mu)):
        for j in range(len(Table)):
            if mu['Categoría'][i] == 'Cerdos':
                if Table['TiempoEngorda'][j] <= infTE[i] or Table['TiempoEngorda'][j] >= supTE[i] and \
                        Table['Costo'][j] >= infC[i] and Table['Utilidad Bruta'][j] <= supU[i]:
                            index_to_drop.append(j)
            if mu['Categoría'][i] == 'Huevo' and Table['Costo'][j] >= infC[i] and Table['Utilidad Bruta'][j] <= supU[i]:
                 index_to_drop.append(j)
    Table = Table.drop(index_to_drop, axis=0).reset_index(drop=True)                        
    return Table
#%% Cerdo
CV = pd.read_excel('CERDO.xlsx', sheet_name='DataFiltrada', header = None).drop(0,axis=0).reset_index(drop=True)
CV = CV.rename(columns = CV.iloc[0]).drop(0,axis=0).drop(columns =['Almacén','Capa','E/S','Unidad','Cliente / Proveedor',
                                                                            'FechaNacimiento','Semana del año']).reset_index(drop=True)
CV[['TiempoEngorda','Kilo','Cabezas','Venta','Costo','Costo Uni','Peso','Precio','Utilidad Bruta']] = CV[['TiempoEngorda','Kilo',
                                                                                                         'Cabezas','Venta','Costo','Costo Uni','Peso',
                                                                                                         'Precio','Utilidad Bruta']].apply(pd.to_numeric)
for i in range(4):
    Cmu,Cstd,CS = Stats(CV)
    CV = Acotar(Cmu,Cstd,CV)
#%% Huevo
HV = pd.read_excel('Huevo.xlsx', sheet_name='DataFil', header = None).drop(0,axis=0).reset_index(drop=True)   
HV = HV.iloc[:,:15]  
HV = HV.rename(columns = HV.iloc[0]).drop(0,axis=0).drop(columns =['Almacén','E/S','Unidad','Cliente / Proveedor',
                                                                   'Semana del año']).reset_index(drop=True)  
HV[['Kilo','Venta','Costo','Costo Uni','Precio','Utilidad Bruta']] = HV[['Kilo','Venta','Costo','Costo Uni',
                                                                         'Precio','Utilidad Bruta']].apply(pd.to_numeric)
for i in range(len(HV)):
    if HV.Precio[i] < 0:
        d = i
HV = HV.drop(d, axis=0).reset_index(drop=True)
Hmu,Hstd,HS = Stats(HV)
#%% Borrego
BV = pd.read_excel('BORREGO.xlsx', sheet_name='DataFil', header = None).drop(0,axis=0).reset_index(drop=True)   
BV = BV.rename(columns = BV.iloc[0]).drop(0,axis=0).drop(columns =['Almacén','E/S','Unidad','Cliente / Proveedor',
                                                                            'Semana del año']).reset_index(drop=True)
BV[['Kilo','Cabezas','Venta','Costo','Costo Uni','Peso','Precio','Utilidad Bruta']] = BV[['Kilo','Cabezas','Venta','Costo',
                                                                                          'Costo Uni','Peso','Precio','Utilidad Bruta']].apply(pd.to_numeric)
for i in range(4):
    Bmu,Bstd,BS = Stats(BV)
    BV = Acotar(Bmu,Bstd,BV)
#%% Excel
with pd.ExcelWriter('Ventas.xlsx') as writer:   
    CS.to_excel(writer, sheet_name='Ventas Cerdo Metricas', index = False)
    HS.to_excel(writer, sheet_name='Ventas Huevo Metricas', index = False)
    BS.to_excel(writer, sheet_name='Ventas Borrego Metricas', index = False)
