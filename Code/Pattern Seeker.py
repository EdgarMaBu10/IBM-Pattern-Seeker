# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as sc
from scipy.cluster import hierarchy
from mylibE import mylibE

#%% Leer los datos
data_dir = '../Data/RawData.xlsx'
data = pd.read_excel(data_dir, 'Raw data 8XX')
parametros = pd.read_excel(data_dir, 'Parametros')
parametros = parametros.iloc[2:,:8]

#%%
def replace_text(x, to_replace, replacement):
    try: 
        x= x.replace(to_replace, replacement)
    except:
        pass
    return x

#%% 
parametros= parametros.apply(replace_text, args= ('Truven simpler', 'Truven Simpler'))
data= data.apply(replace_text, args= ('Truven simpler', 'Truven Simpler'))
data= data.apply(replace_text, args= ('Truven simpler', 'Truven Simpler'))

#%%
filasdata,coldata=data.shape
for a in range(filasdata):
    for b in range(coldata):
        try:
            data.iloc[a,b]=pd.to_numeric(data.iloc[a,b])
        except:
            pass
#%%
filaspar,colpar=parametros.shape
for a in range(filaspar):
    for b in range(colpar):
        try:
            parametros.iloc[a,b]=pd.to_numeric(parametros.iloc[a,b])
        except:
            pass
        
    #%% Usar mi funcion
data_quality_report_data= mylibE.DQR(data)
data_quality_report_par = mylibE.DQR(parametros)
#%% Comprobacion parametros
NumdatosDatocolumna= data_quality_report_par.iloc[1,2] 

#%%
RepetidosIgualSeg=pd.DataFrame(columns=['Columna','Datocolumna','Segmentación'])
Suma=0
RepetidosDifSeg=pd.DataFrame(columns=['Columna','Datocolumna','Segmentación1','Segmentación2'])
Suma2=0

for k in range (0,NumdatosDatocolumna):
    Colpar=parametros.iloc[k,0]
    DCpar=parametros.iloc[k,1]
    Segpar=parametros.iloc[k,2]
    
    for i in range (k+1,NumdatosDatocolumna):
        Colpar2=parametros.iloc[i,0]
        DCpar2=parametros.iloc[i,1]
        Segpar2=parametros.iloc[i,2]
        if Colpar==Colpar2 and DCpar==DCpar2 and Segpar==Segpar2:
            RepetidosIgualSeg.loc[Suma]=[Colpar,DCpar,Segpar]
            Suma=Suma+1
            #print(Col, DC, Res, Col2, DC2, Res2)
        else:
            if Colpar==Colpar2 and DCpar==DCpar2 and Segpar!=Segpar2:
                RepetidosDifSeg.loc[Suma2]=[Colpar,DCpar,Segpar,Segpar2]
                Suma2=Suma2+1
                #print(Col, DC, Res, Col2, DC2, Res2, 'Tienen diferente segmentación')


#%%
Nocuadrados=pd.DataFrame(columns=['Columna','Datocolumna','Segmentaciónraw','Segmentacionpar'])
Suma=0
for k in range (0,NumdatosDatocolumna):
    Colpar=parametros.iloc[k,0]
    DCpar=parametros.iloc[k,1]
    Segpar=parametros.iloc[k,2]
    if Colpar in data.columns:
        Index=data[data[Colpar] == DCpar]
        #print(Colpar,DCpar,len(Index))
        Numdatosindice=len(Index)
        for d in range(Numdatosindice):
            try:
                Segraw=Index.iloc[d,29]
                if Segpar!=Segraw:
                    Nocuadrados.loc[Suma]=[Colpar,DCpar,Segraw,Segpar]
                    Suma=Suma+1
                    #print(Col, DC, Resul)
            except:
                pass
          
#%%
data.insert(31,'Segautomatizada',0)
data.insert(32,'Superpuestos',0)

#%%
Superpuestas=pd.DataFrame(columns=['Columna','Datocolumna','Segmentaciónpasada','Segmentacionnueva'])
Suma=0
data.iloc[:,[31,32]]=0
for k in range (0,NumdatosDatocolumna):
    Colpar=parametros.iloc[k,0]
    DCpar=parametros.iloc[k,1]
    Segpar=parametros.iloc[k,2]
    if Colpar in data.columns:
        Index=data[data[Colpar] == DCpar]
        Numdatosindice=len(Index)
        if Numdatosindice>0:
            for d in range(filasdata):
                DCraw=data.loc[d][Colpar]
                if DCpar==DCraw:
                    if data.iloc[d,31]!=0 and data.iloc[d,31]!=Segpar:
                        Superpuestas.loc[Suma]=[Colpar,DCpar,data.iloc[d,31],Segpar]
                        Suma=Suma+1
                        #print(Colpar,DCpar,data.iloc[d,31],Segpar)
                        data.iloc[d,31]=Segpar
                        data.iloc[d,32]=data.iloc[d,32]+1
                    else:
                        if data.iloc[d,31]==0:
                            data.iloc[d,31]=Segpar
                else:
                    pass
        else:
            pass
Filassuperpuestas=data[data['Superpuestos'] != 0]

#%%
Parametrosencontrados=pd.DataFrame(columns=['Columna','Datocolumna','Segmentación'])
Suma=0
columnasenpar=pd.DataFrame(parametros.iloc[:,0].unique())
Numcolunicaspar=len(columnasenpar)
for e in range(Numcolunicaspar):
    Colpar=columnasenpar.iloc[e,0]
    if Colpar in data.columns:
        Filasunicasencol=pd.DataFrame(data.loc[:][Colpar].unique()).dropna()
        Numfilasunicasencol=len(Filasunicasencol)
        if Numfilasunicasencol>0:
            for i in range (Numfilasunicasencol):
                Index=data[data[Colpar] == Filasunicasencol.iloc[i,0]]
                Index2=Index.loc[:][[Colpar,'Segmentation Offering']]
                Index2['Sumatoria']=0
                Numdatosenfilasunicascol=len(Index2)
                if Numdatosenfilasunicascol>1:
                    DCdata=Index2.iloc[0,0]
                    #DCraw=data.loc[d][Colpar]
                    Segdata=Index2.iloc[0,1]
                    for r in range (1,Numdatosenfilasunicascol):
                        DCdata2=Index2.iloc[r,0]
                        Segdata2=Index2.iloc[r,1]
                        if DCdata==DCdata2 and Segdata==Segdata2:
                            Index2.iloc[r,2]=1
                            if Index2['Sumatoria'].sum() +1== Numdatosenfilasunicascol:
                                Parametrosencontrados.loc[Suma]=[Colpar,DCdata,Segdata]
                                Suma=Suma+1
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
        else:
            pass
    else:
        pass
    
#%%
Parametrospropuestos=pd.DataFrame(columns=['Columna','Datocolumna','Segmentación'])
Suma2=0
NumdatosParametrosencon= len(Parametrosencontrados)

for i in range (0,NumdatosParametrosencon):
        Suma=0
        parametros['Sumatoria']=0
        Colparenc=Parametrosencontrados.iloc[i,0]
        DCparenc=Parametrosencontrados.iloc[i,1]
        Segparenc=Parametrosencontrados.iloc[i,2]
        for k in range (0,NumdatosDatocolumna):
            Colpar=parametros.iloc[k,0]
            DCpar=parametros.iloc[k,1]
            Segpar=parametros.iloc[k,2]
            if Colpar==Colparenc and DCpar==DCparenc and Segpar==Segparenc:
                parametros.iloc[Suma,-1]=1
                Suma=Suma+1
            else:
                if Colpar!=Colparenc or DCpar!=DCparenc or Segpar!=Segparenc:
                    parametros.iloc[Suma,-1]=0
                    Suma=Suma+1
                else:
                    pass
        if parametros['Sumatoria'].sum()==0:
            Parametrospropuestos.loc[Suma2]=[Colparenc,DCparenc,Segparenc]
            Suma2=Suma2+1
        else:
            pass

#%%
Segmentaciones=pd.DataFrame(data.loc[:]['Segmentation Offering'].unique()).dropna()
meses=pd.DataFrame(data.loc[:]['Month'].unique()).dropna()
NumSegmentaciones=len(Segmentaciones)
for b in range (NumSegmentaciones):
    Segmentacion=Segmentaciones.iloc[b,0]
    Index=data[data['Segmentation Offering'] == Segmentacion]
    cost_by_seg = pd.DataFrame(Index.groupby(['Month'])['Cost'].sum())
    cost_by_seg.plot(kind='bar',title=Segmentacion)
    plt.ylabel('Costo')
    plt.xlabel('Month')
    plt.show()