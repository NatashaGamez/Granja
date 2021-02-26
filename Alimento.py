#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:09:49 2021

@author: Carlos
"""


import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

#%%
def Alimento_Stats_Gral(Table):
    AlimentoGral = Table.groupby(['Descripción','Fecha']).sum().reset_index()
    AlimentoGral = Table.groupby(['Descripción','Unidad','Fecha']).sum().reset_index()
    AlimentoGral['Fecha2'] = [AlimentoGral.Fecha[i-1] if i>0 else AlimentoGral.Fecha[i] for i in range(len(AlimentoGral))]
    AlimentoGral['Periodo'] = [AlimentoGral.Fecha[i]-AlimentoGral.Fecha2[i] for i in range(len(AlimentoGral))]
    AlimentoGral['Periodo'] = pd.to_numeric(AlimentoGral['Periodo'].dt.days, downcast='integer')
    AlimentoGral['Periodo'] = [0 if AlimentoGral['Periodo'][i] < 0 else AlimentoGral['Periodo'][i] for i in range(len(AlimentoGral))]
    AlimentoGral = AlimentoGral.drop(columns=['Fecha', 'Fecha2'])
    AlimentoMu = AlimentoGral.groupby(['Descripción','Unidad']).mean()
    AlimentoMu = AlimentoMu.rename(columns = {'Entrada':'MuCantidad','Importe Costo':'MuCost','Periodo':'MuPeriodo'})
    AlimentoMax = AlimentoGral.groupby(['Descripción','Unidad']).max()
    AlimentoMax = AlimentoMax.rename(columns = {'Entrada':'MaxCantidad','Importe Costo':'MaxCost','Periodo':'MaxPeriodo'})
    AlimentoMin = AlimentoGral.groupby(['Descripción','Unidad']).min()
    AlimentoMin = AlimentoMin.rename(columns = {'Entrada':'MinCantidad','Importe Costo':'MinCost','Periodo':'MinPeriodo'})
    AlimentoStd = AlimentoGral.groupby(['Descripción','Unidad']).std()
    AlimentoStd = AlimentoStd.rename(columns = {'Entrada':'StdCantidad','Importe Costo':'StdCost','Periodo':'StdPeriodo'})
    AlimentoStats = pd.concat([AlimentoMin,AlimentoMu,AlimentoStd,AlimentoMax],axis=1).reset_index()
    return AlimentoStats

def Alimento_Stats_Granja(Table):
    Table['Almacén'] = [ Table['Almacén'][i][0:3] if Table['Almacén'][i][0:2] == 'GV' else Table['Almacén'][i] for i in range(len(Table))]
    Table =  Table.groupby(['Almacén','Descripción','Unidad','Fecha']).sum().reset_index()
    Table['Fecha2'] = [Table.Fecha[i-1] if i>0 else Table.Fecha[i] for i in range(len(Table))]
    Table['Periodo'] = [Table.Fecha[i]-Table.Fecha2[i] for i in range(len(Table))]
    Table['Periodo'] = pd.to_numeric(Table['Periodo'].dt.days, downcast='integer')
    Table['Periodo'] = [0 if Table['Periodo'][i] < 0 else Table['Periodo'][i] for i in range(len(Table))]
    Table = Table.drop(columns=['Fecha', 'Fecha2'])
    AlimentoMu = Table.groupby(['Almacén','Descripción','Unidad']).mean()
    AlimentoMu = AlimentoMu.rename(columns = {'Entrada':'MuCantidad','Importe Costo':'MuCost','Periodo':'MuPeriodo'})
    AlimentoStd = Table.groupby(['Almacén','Descripción','Unidad']).std()
    AlimentoStd = AlimentoStd.rename(columns = {'Entrada':'StdCantidad','Importe Costo':'StdCost','Periodo':'StdPeriodo'})
    AlimentoStats = pd.concat([AlimentoMu,AlimentoStd],axis=1).reset_index()
    return AlimentoStats

def Acotar(StatsO,RH1):
    infC = StatsO['MuCantidad'] - StatsO['StdCantidad']
    supC = StatsO['MuCantidad'] + StatsO['StdCantidad']
    index_to_drop = []
    for i in range(len(StatsO)):
        for j in range(len(RH1)):
            if StatsO['Almacén'][i] == RH1['Almacén'][j] and \
                StatsO['Descripción'][i] == RH1['Descripción'][j] and\
                (RH1['Entrada'][j] <= infC[i] or RH1['Entrada'][j] >= supC[i]):
                    index_to_drop.append(j)  
    RH1 = RH1.drop(index_to_drop, axis = 0).reset_index(drop=True)
    return RH1    


#%%
AC = pd.read_excel('CERDO.xlsx', sheet_name='ALIMENTOS FORMULAS CERDOS').drop(columns=['Código','Tipo de movimiento','Capa','E/S',
                                                                                              'Folio','Referencia','Kilos','Salida','Importe Venta',
                                                                                              'Cliente / Proveedor','Categoría','Línea'])
AH = pd.read_excel('HUEVO.xlsx', sheet_name='FORMULAS').drop(columns=['Código','Tipo de movimiento','Capa','E/S',
                                                                             'Folio','Referencia','Kilos','Salida','Importe Venta',
                                                                             'Cliente / Proveedor','Categoría','Línea'])

SC = Alimento_Stats_Granja(AC)
SH = Alimento_Stats_Granja(AH)
#%%
AC1 = Acotar(SC,AC)
SC1 =Alimento_Stats_Granja(AC1)
AH1 = Acotar(SH,AH)
SH1 = Alimento_Stats_Granja(AH1)
#%%
with pd.ExcelWriter('Alimentos.xlsx') as writer:  
 #   AlimentoGralC.to_excel(writer, sheet_name='Alimento Gral Cerdo', index = True)
 #   AlimentoGralH.to_excel(writer, sheet_name='Alimento Gral Huevo', index = True)
    SC1.to_excel(writer, sheet_name='Alimento Granja Cerdo', index = True)
    SH1.to_excel(writer, sheet_name='Alimento Granja Huevo', index = True)
