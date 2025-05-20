from core.webscraper.webscraper_ssp import chromeDriverSSP
from core.processor.processormain import formatacaoDados
from googleapis.sheets import googleSheets
from utils.folders import *
import os

class Ctrl:
    def __init__(self):
        self.driver = chromeDriverSSP()
        self.formatter = formatacaoDados()
        self.gsheets = googleSheets()
    
    def execute_driver(self):
        self.driver.get_monthly_data()
        self.driver.quit()

    def process_data(self):
        for i in os.listdir(landzonepath):
            df = self.formatter.process_data(os.path.join(landzonepath, i))
        return df

    def send_df_to_sheets(self, df):
        self.gsheets.concat_dfs(df)


if __name__ == '__main__':
    exec = Ctrl()
    exec.execute_driver()
    df = exec.process_data()
    exec.send_df_to_sheets(df)
    kill_folders()