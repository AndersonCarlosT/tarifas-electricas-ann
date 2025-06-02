import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

regiones = [
    {"id": "150000", "indices": [0, 4, 18, 21, 23, 13, 7, 5, 9, 6, 8, 31, 29, 1, 3, 2],
     "nombres": ["Lima norte", "Huacho", "Supe-Barranca", "Huaral-Chancay", "Pativilca",
                 "Churín", "Ravira-Pacaraos", "Canta", "Yaso", "Hoyos-Acos", "Sayán-Humaya", 
                 "SER Chillón", "Valle del Caral", "Lima Sur", "Cañete", "Lunahuaná"]},

    {"id": "130000", "indices": [0], "nombres": ["Trujillo"]},
    {"id": "110000", "indices": [2], "nombres": ["Chincha Baja Densidad"]},
    {"id": "40000", "indices": [0], "nombres": ["Arequipa"]},
    {"id": "200000", "indices": [0, 7], "nombres": ["Piura", "Paita"]},
    {"id": "180000", "indices": [1], "nombres": ["Ilo"]},
    {"id": "120000", "indices": [0], "nombres": ["Huancayo"]},
    {"id": "60000", "indices": [0], "nombres": ["Cajamarca"]},
    {"id": "20000", "indices": [0], "nombres": ["Chimbote"]},
    {"id": "140000", "indices": [0], "nombres": ["Chiclayo"]},
    {"id": "110000", "indices": [0], "nombres": ["Ica"]},
    {"id": "210000", "indices": [0], "nombres": ["Juliaca"]},
    {"id": "250000", "indices": [0], "nombres": ["Pucallpa"]},
    {"id": "20000", "indices": [23], "nombres": ["Santa"]},
    {"id": "130000", "indices": [15], "nombres": ["Paiján-Malabrigo"]},
    {"id": "40000", "indices": [7], "nombres": ["Repartición-La Cano"]},
    {"id": "80000", "indices": [0], "nombres": ["Cusco"]}
]

def run_scraping():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

    df_final = pd.DataFrame()

    for region in regiones:
        url = f"https://www.osinergmin.gob.pe/Tarifas/Electricidad/PliegoTarifario?Id={region['id']}"
        
        for idx, nombre in zip(region["indices"], region["nombres"]):
            driver.get(url)
            time.sleep(4)
            select_depa = Select(wait.until(EC.presence_of_element_located((By.ID, "DDLSE"))))
            select_depa.select_by_index(idx)
            time.sleep(4)
            select_fecha = Select(driver.find_element(By.ID, "DDLFecha"))
            select_fecha.select_by_index(0)
            time.sleep(4)
            tabla = driver.find_element(By.ID, "TbPliego")
            html_tabla = tabla.get_attribute('outerHTML')
            df = pd.read_html(html_tabla)[0]
            columna_d = df.iloc[4:190, 3].reset_index(drop=True)
            df_final[nombre] = columna_d

    driver.quit()
    df_final.to_excel("output.xlsx", index=False)
    return "output.xlsx"
