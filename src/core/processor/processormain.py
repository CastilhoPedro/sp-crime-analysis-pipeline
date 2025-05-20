from utils.support import *
from utils.folders import *
import pandas as pd
import os
import userpaths as usr



class formatacaoDados:
    def __init__(self):
        
        self.dfcolumns=[
            'Homicídio Doloso',
            'Nº De Vítimas Em Homicídio Doloso',
            'Homicídio Doloso Por Acidente De Trânsito',
            'Nº De Vítimas Em Homicídio Doloso Por Acidente De Trânsito',
            'Homicídio Culposo Por Acidente De Trânsito',
            'Homicídio Culposo Outros',
            'Tentativa De Homicídio',
            'Lesão Corporal Seguida De Morte',
            'Lesão Corporal Dolosa',
            'Lesão Corporal Culposa Por Acidente De Trânsito',
            'Lesão Corporal Culposa - Outras',
            'Latrocínio',
            'Nº De Vítimas Em Latrocínio',
            'Total De Estupro',
            'Estupro',
            'Estupro De Vulnerável',
            'Total De Roubo - Outros',
            'Roubo - Outros',
            'Roubo De Veículo',
            'Roubo A Banco',
            'Roubo De Carga',
            'Furto - Outros',
            'Furto De Veículo',
            'Mes',
            'Ano',
            'Municipio'
        ]
        
        self.main_folder = landzonepath
        self.main_df = pd.DataFrame(columns=self.dfcolumns)

        

    def __get_years(self, file_path: str) -> list:
        df = pd.read_excel(file_path, sheet_name=None)
        return list(df.keys())

    def insert_date_columns(self, df: pd.DataFrame, year: str) -> pd.DataFrame:
        df['Mes'] = df.index
        df['Ano'] = year
        return df

    def add_city(self, file_path: str, df: pd.DataFrame) -> pd.DataFrame:
        for i in list_cities:
            if i in file_path:
                df['Municipio'] = i
        return df

    def kill_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.loc[(df['Mes'] != 'Total') & (df['Homicídio Doloso'] != '...')]
        return df

    def add_total_column(self, df: pd.DataFrame) -> pd.DataFrame:
        int_columns = ['Homicídio Doloso', 'Nº De Vítimas Em Homicídio Doloso',
        'Homicídio Doloso Por Acidente De Trânsito',
        'Nº De Vítimas Em Homicídio Doloso Por Acidente De Trânsito',
        'Homicídio Culposo Por Acidente De Trânsito',
        'Homicídio Culposo Outros', 'Tentativa De Homicídio',
        'Lesão Corporal Seguida De Morte', 'Lesão Corporal Dolosa',
        'Lesão Corporal Culposa Por Acidente De Trânsito',
        'Lesão Corporal Culposa - Outras', 'Latrocínio',
        'Nº De Vítimas Em Latrocínio', 'Total De Estupro', 'Estupro',
        'Estupro De Vulnerável', 'Total De Roubo - Outros', 'Roubo - Outros',
        'Roubo De Veículo', 'Roubo A Banco', 'Roubo De Carga', 'Furto - Outros',
        'Furto De Veículo']

        str_columns = ['Ano', 'Mes', 'Municipio']

        df[int_columns] = df[int_columns].astype(int)
        df[str_columns] = df[str_columns].astype(str)

        subdf = df[int_columns]
        df['Total'] = subdf.sum(axis=1)
        return df

    def process_data(self, file_path):
        
        for year in self.__get_years(file_path):
            
            df = pd.read_excel(file_path, sheet_name=year)
            df = df.transpose()
            
            self.insert_date_columns(df=df, year=year)

            if len(df.columns) == 25:
                df.columns = self.dfcolumns[:-1]
            elif len(df.columns) == 26:
                df.columns = self.dfcolumns
            
            
            df = df.drop(df.index[0])
            
            df = self.add_city(file_path, df)
            df = self.kill_rows(df)
            df = self.add_total_column(df)

            self.main_df = pd.concat([self.main_df, df])
        return self.main_df




if __name__ == '__main__':
    dados1 = formatacaoDados()
    for i in os.listdir(dados1.main_folder):
        dados1.process_data(os.path.join(dados1.main_folder, i))
