class mylibE:
    def DQR(data):
        #REPORTE DE CALIDAD DE LOS DATOS
        import pandas as pd
        #% lista de variables que se encuentran en la base de datos
        columns = pd.DataFrame(list(data.columns.values), columns=['Nombres'], index= list(data.columns.values))
        
        #% Lista de tipos de variables
        data_types = pd.DataFrame(data.dtypes, columns=['Tipo'])
        
        #% Lista de datos presentes
        present_values = pd.DataFrame(data.count(), columns=['Datos Presentes'])
        
        #% Lista de datos faltantes
        miss_values = pd.DataFrame(data.isnull().sum(), columns=['Datos Faltantes'])
        
        #% Lista de valores unicos
        unique_values = pd.DataFrame(columns=['Datos Unicos'])
        for col in list(data.columns.values):
            unique_values.loc[col]=[data[col].nunique()]
        
        #% Lista de valores minimos
        min_values = pd.DataFrame(columns=['Minimo'])
        for col in list(data.columns.values):
            try:
                min_values.loc[col]=[data[col].min()]
            except:
                pass
            
        #% Lista de valores maximos
        max_values = pd.DataFrame(columns=['Maximo'])
        for col in list(data.columns.values):
            try:
                max_values.loc[col]=[data[col].max()]
            except:
                pass
            
        #% Reporte final
        data_quality_report = columns.join(data_types).join(present_values).join(miss_values).join(unique_values).join(min_values).join(max_values)
        return data_quality_report