import streamlit as st
import requests
import pandas as pd

# ===== Función para obtener datos Pluz Energia =====
def obtener_tarifas_pluz(indice_fecha):
    regiones = [
        {"id": "150000", "indices": [0, 4, 18, 21, 23, 13, 7, 5, 9, 6, 8, 31, 29, 1, 3, 2],
         "nombres": ["Lima norte", "Huacho", "Supe-Barranca", "Huaral-Chancay", "Pativilca",
                     "Churín", "Ravira-Pacaraos", "Canta", "Yaso", "Hoyos-Acos", "Sayán-Humaya",
                     "SER Chillón", "Valle del Caral", "Lima Sur", "Cañete", "Lunahuaná"]},
    ]

    df_final = pd.DataFrame()

    for region in regiones:
        url = f"https://www.osinergmin.gob.pe/Tarifas/Electricidad/PliegoTarifario?Id={region['id']}"
        response = requests.get(url)
        response.raise_for_status()
        tablas = pd.read_html(response.text)

        for idx, nombre in zip(region["indices"], region["nombres"]):
            df = tablas[0]
            columna_d = df.iloc[4:190, 3].reset_index(drop=True)
            df_final[nombre] = columna_d

    return df_final

# ===== Interfaz Streamlit =====
st.title("Scraping Tarifas de Electricidad")

distribuidora = st.selectbox("Selecciona distribuidora", ["Pluz Energia Perú", "Luz del Sur"])
fecha = st.selectbox("Selecciona fecha", ["Última actualización", "Penúltima actualización"])

if st.button("Generar Excel"):
    if distribuidora == "Pluz Energia Perú":
        indice_fecha = 0 if fecha == "Última actualización" else 1
        df_final = obtener_tarifas_pluz(indice_fecha)
        nombre_archivo = "tarifas_pluz.xlsx"
        df_final.to_excel(nombre_archivo, index=False)
        st.success("Excel generado con éxito")
        st.download_button(label="Descargar Excel", data=open(nombre_archivo, "rb").read(), file_name=nombre_archivo)

    elif distribuidora == "Luz del Sur":
        st.warning("Funcionalidad Luz del Sur próximamente.")
