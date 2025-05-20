import pandas as pd
import json
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe


class googleSheets:
    def __init__(self):
        
        with open('credentials.json', 'r', encoding='utf-8') as txt_file:
            cred_dict = txt_file.read()


        creds = Credentials.from_service_account_info(cred_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        gc = gspread.authorize(creds)

        DB = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TxcQDOXCh7EPmkjpg8UIDK3NiKFk9G142WYmLs2cyGg/edit?gid=0#gid=0')  # ou .open("nome da planilha")

        self.sheet = DB.worksheet("DB")
        self.df = get_as_dataframe(self.sheet)

    def concat_dfs(self, df):
        self.df = pd.concat([self.df, df], ignore_index=True)
        self.df = self.df.drop_duplicates(subset=['Mes', 'Ano', 'Municipio'], keep='last')
        
        self.sheet.clear()
        set_with_dataframe(worksheet= self.sheet, dataframe= self.df)


