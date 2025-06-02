import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/unique-chrome-profile")
    return webdriver.Chrome(options=chrome_options)

# Lista de regiones y subzonas
regiones = [
    {"id": "150000", "indices": [0, 4, 18, 21, 23, 13, 7, 5, 9, 6, 8, 31, 29, 1, 3, 2],
     "nombres": ["Lima norte", "Huacho", "Supe-Barranca", "Huaral-Chancay", "Pativilca",
                 "Churín", "Ravira-Pacaraos", "Canta", "Yaso", "Hoyos-Acos", "Sayán-Humaya",
                 "SER Chillón", "Valle del Caral", "Lima Sur", "Cañete", "Lunahuaná"]},
    {"id": "130000", "indices": [0], "nombres": ["Trujillo"]},
    # ... otras regiones (agrega todas si quieres)
]

def obtener_tarifas_selenium():
    driver = create_driver()
    wait = WebDriverWait(driver, 15)
    df_final = pd.DataFrame()

    for region in regiones:
        url = f"https://www.osinergmin.gob.pe/Tarifas/Electricidad/PliegoTarifario?Id={region['id']}"
        driver.get(url)
        time.sleep(3)

        for idx, nombre in zip(region["indices"], region["nombres"]):
            st.write(f"Extrayendo datos de: {nombre} (índice {idx})")

            # Seleccionar subzona
            select_depa = Select(wait.until(EC.presence_of_element_located((By.ID, "DDLSE"))))
            select_depa.select_by_index(idx)
            time.sleep(3)

            # Seleccionar fecha (última actualización, índice 0)
            select_fecha = Select(driver.find_element(By.ID, "DDLFecha"))
            select_fecha.select_by_index(0)
            time.sleep(3)

            # Obtener tabla HTML
            tabla = driver.find_element(By.ID, "TbPliego")
            html_tabla = tabla.get_attribute('outerHTML')
            df = pd.read_html(html_tabla)[0]

            # Extraer columna deseada (por ejemplo columna 3 filas 4:190)
            columna_d = df.iloc[4:190, 3].reset_index(drop=True)
            df_final[nombre] = columna_d

    driver.quit()
    return df_final

# Streamlit app
st.title("Scraping Tarifas de Electricidad")

if st.button("Generar Excel con Selenium"):
    with st.spinner("Extrayendo datos... Esto puede tardar unos minutos"):
        try:
            df_result = obtener_tarifas_selenium()
            archivo_excel = "tarifas_electricas.xlsx"
            df_result.to_excel(archivo_excel, index=False)
            st.success("Excel generado correctamente")
            st.download_button("Descargar Excel", data=open(archivo_excel, "rb").read(), file_name=archivo_excel)
        except Exception as e:
            st.error(f"Error durante la extracción: {e}")
