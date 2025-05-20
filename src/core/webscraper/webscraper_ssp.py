from utils.folders import *
from utils.support import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common import exceptions
import time





class chromeDriverSSP:
    
    def __init__(self):
        self.service = Service()


        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        

        self.filepath = landzonepath
        
        prefs = {
            "download.default_directory": f"{self.filepath}",
            'detach': False
            }


        self.options.add_experimental_option("prefs", prefs)
        

        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 300)
        
        
        self.lista_municipios = list_cities
        self.lista_municipios.append('fim')

        for i in os.listdir(self.filepath):
            os.remove(os.path.join(self.filepath, i))


    def __webwait__(self):
        return self.wait.until(EC.invisibility_of_element((By.XPATH, "//p[@class='ng-tns-c16-0']")))
    
    
    def __load_window__(self, url: str):
        self.driver.get(url)
        self.__webwait__()


    def interact_element(self, formcontrolname: str, checkelement: str):
            for i in self.driver.find_elements(By.XPATH, f"//select/option[@class='ng-star-inserted']"):
                if checkelement.lower() in i.text.lower():
                    i.click()
                    self.__webwait__()
                    break
    

    def __get_mon_archive__(self, municipio: str):
        """Método para exportar a planilha Excel da aba de dados mensais.

        Args:
            municipio (str): municício (deve ser escrito igual está no portal da SSP) 
        """
        
        self.interact_element(formcontrolname='mensalRegiao', checkelement="Grande São Paulo")
        self.interact_element(formcontrolname='mensalMunicipio', checkelement=municipio)
        
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-success btn-export']"))).click()

    def __get_year_archive__(self, municipio: str):
        self.interact_element(formcontrolname='anualMunicipio', checkelement=municipio)
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-success btn-export']").click()

    

    def get_monthly_data(self):
        self.__load_window__(url= "https://www.ssp.sp.gov.br/estatistica/dados-mensais")
        for num, i in enumerate(self.lista_municipios, start=1):
            if i != 'fim':
                self.__get_mon_archive__(i)
                #Garantiremos que a aplicação espere até que o arquivo esteja na pasta
                while len(os.listdir(self.filepath)) < num: 
                    time.sleep(0.5)
            else:
                return
            
    
    def quit(self):
        return self.driver.quit()



if __name__ == "__main__":
    teste = chromeDriverSSP()
    teste.get_monthly_data()
    teste.quit()
