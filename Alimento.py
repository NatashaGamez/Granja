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
def Alimentos_Stats(Table):
    AlimentoGral = Table.groupby(['Descripción','Fecha']).sum().reset_index()
    AlimentoGral['Fecha2'] = [AlimentoGral.Fecha[i-1] if i>0 else AlimentoGral.Fecha[i] for i in range(len(AlimentoGral))]
    AlimentoGral['Periodo'] = [AlimentoGral.Fecha[i]-AlimentoGral.Fecha2[i] for i in range(len(AlimentoGral))]
    AlimentoGral['Periodo'] = pd.to_numeric(AlimentoGral['Periodo'].dt.days, downcast='integer')
    AlimentoGral['Periodo'] = [0 if AlimentoGral['Periodo'][i] < 0 else AlimentoGral['Periodo'][i] for i in range(len(AlimentoGral))]
    AlimentoGral = AlimentoGral.drop(columns=['Fecha', 'Fecha2'])
    AlimentoMu = AlimentoGral.groupby('Descripción').mean()
    AlimentoMu = AlimentoMu.rename(columns = {'Entrada':'MuCantidad','Importe Costo':'MuCost','Periodo':'MuPeriodo'})
    AlimentoMax = AlimentoGral.groupby('Descripción').max()
    AlimentoMax = AlimentoMax.rename(columns = {'Entrada':'MaxCantidad','Importe Costo':'MaxCost','Periodo':'MaxPeriodo'})
    AlimentoMin = AlimentoGral.groupby('Descripción').min()
    AlimentoMin = AlimentoMin.rename(columns = {'Entrada':'MinCantidad','Importe Costo':'MinCost','Periodo':'MinPeriodo'})
    AlimentoStd = AlimentoGral.groupby('Descripción').std()
    AlimentoStd = AlimentoStd.rename(columns = {'Entrada':'StdCantidad','Importe Costo':'StdCost','Periodo':'StdPeriodo'})
    AlimentoStats = pd.concat([AlimentoMin,AlimentoMu,AlimentoStd,AlimentoMax],axis=1)
    return AlimentoStats

#%%
AlimentoC = Alimentos_Stats(pd.read_excel('CERDO.xlsx', sheet_name='ALIMENTOS FORMULAS CERDOS').drop(columns=['Código','Tipo de movimiento','Capa','E/S',
                                                                                             'Folio','Referencia','Kilos','Salida','Importe Venta',
                                                                                             'Cliente / Proveedor','Categoría','Línea']))
AlimentoH = Alimentos_Stats(pd.read_excel('HUEVO.xlsx', sheet_name='FORMULAS').drop(columns=['Código','Tipo de movimiento','Capa','E/S',
                                                                                             'Folio','Referencia','Kilos','Salida','Importe Venta',
                                                                                             'Cliente / Proveedor','Categoría','Línea']))
with pd.ExcelWriter('Alimentos.xlsx') as writer:  
    AlimentoC.to_excel(writer, sheet_name='Alimento Cerdo', index = True)
    AlimentoH.to_excel(writer, sheet_name='Alimento Huevo', index = True)
