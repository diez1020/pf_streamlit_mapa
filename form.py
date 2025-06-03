import streamlit as st
import csv
import os
import pandas as pd
from geopy.geocoders import Nominatim

# CONFIGURAR GEOLOCALIZADOR
# Nominatim es un sistema de geocodificación gratuito proporcionado por OpenStreetMap.
# Cuando usas Nominatim, debes identificar tu aplicación con un user_agent y puede ser cualquier cadena de texto, en este caso quise poner "streamlit_localizador"
geolocalizador = Nominatim(user_agent="streamlit_localizador") 

st.title("Formulario de Registro")

# Formulario
with st.form("formulario_registro"):
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    correo = st.text_input("Correo electrónico")
    ciudad = st.text_input("Ciudad")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")
    categoria = st.radio("Categoría",["🔴 Seguridad", "🔵 Servicios", "🟡 Infraestructura"])
    descripcion = st.text_area("Descripción") # esto crea un campo de texto como lo haciamos con tkinter 

    boton_enviar = st.form_submit_button("Enviar") # creamos el boton

# Procesar y guardar
archivo = 'registros.csv'
if boton_enviar:
    ubicacion = geolocalizador.geocode(direccion)

    if ubicacion:
        lat = ubicacion.latitude
        lon = ubicacion.longitude
        registros_csv = not os.path.exists(archivo) # verifica si el archivo .csv ya existe o no para agregar o no el encabezado.

        # mode='a':	Modo append (añadir), no borra lo anterior, solo agrega al final.
        # newline='' Evita que se creen líneas vacías extras al guardar en Windows
        # encoding='utf-8'	Usa codificación UTF-8, que permite tildes, ñ, emojis, etc.
        with open(archivo, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if registros_csv:
                writer.writerow(['Ciudad','Dirección', 'Latitud', 'Longitud', 'Categoría']) # crea una primer fila con esos nombre de columnas en el df
            writer.writerow([ciudad, direccion, lat, lon, categoria]) # agrega los elementos a dichas columnas

        st.success("Formulario enviado y datos geolocalizados")
        
    else:
        st.error("Dirección no encontrada. Intenta escribirla de otra forma.")

# Mostrar tabla si el archivo existe
if os.path.exists(archivo):
    st.write("## Registros guardados con coordenadas:")
    df = pd.read_csv(archivo)
    st.dataframe(df)
