import streamlit as st 
import pandas as pd 
import plotly.express as px
import csv
import sqlite3
import os
import folium # libreria de mapas en python # pip install folium
import folium.plugins
from streamlit_folium import st_folium # widget de streamlit para mostrar los mapas # pip install streamlit_folium
from folium.plugins import MarkerCluster
from groq import Groq
from geopy.geocoders import Nominatim
def inicializar_db():
    conexion = sqlite3.connect('Quejas_ciudadanas.db')
    cursor = conexion.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Quejas(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   Nombre TEXT,
                   Apellido TEXT,
                   Correo TEXT,
                   Ciudad TEXT,
                   Direccion TEXT,
                   Telefono TEXT,
                   Categoria TEXT,
                   Descripcion TEXT
                )
                   ''') 
    conexion.commit()
    conexion.close()


    
inicializar_db()
funciones = ['Google Sheet','IA', 'Formulario','Mapa Quejas', 'Datos']
eleccion = st.sidebar.selectbox('Funciones', funciones, index=0)
if eleccion == 'Google Sheet':
    # urls corregidas para exportar como csv
    url1 = "https://docs.google.com/spreadsheets/d/1dT92xolv1BKSydRFxNu6tYsTNBI9biQhnhn94DXq2xo/export?format=csv&gid=1504708429"
    url2 = "https://docs.google.com/spreadsheets/d/1dT92xolv1BKSydRFxNu6tYsTNBI9biQhnhn94DXq2xo/export?format=csv&gid=528616646"
    url3 = "https://docs.google.com/spreadsheets/d/1dT92xolv1BKSydRFxNu6tYsTNBI9biQhnhn94DXq2xo/export?format=csv&gid=21426309"
    url4 = "https://docs.google.com/spreadsheets/d/1dT92xolv1BKSydRFxNu6tYsTNBI9biQhnhn94DXq2xo/export?format=csv&gid=445871243"
    # crear una funcion para cargar y limpiar los datos
    def cargar_datos():
        df1 = pd.read_csv(url1)
        df2 = pd.read_csv(url2)
        df3 = pd.read_csv(url3)
        df4 = pd.read_csv(url4)
        
        # dropna elimina las filas que tienen un valor vacio o null
        # df2[df2.columns[0]].astype(str) convierte la primera columna en texto
        # pd.to_numeric(df2[df2.columns[1]], errors='coerce') convierte la segunda columna a numerica
        # coerce: si algun valor no se puede convertir que lo clasifique como null o lo remplaza por NaN
        df2 = df2.dropna()
        df2[df2.columns[0]] = df2[df2.columns[0]].astype(str)
        df2[df2.columns[1]] = pd.to_numeric(df2[df2.columns[1]], errors='coerce')
        df2 = df2.dropna()

        df3 = df3.dropna()
        df3[df3.columns[0]] = df3[df3.columns[0]].astype(str)
        df3[df3.columns[1]] = pd.to_numeric(df3[df3.columns[1]], errors='coerce')
        df3 = df3.dropna()

        df4 = df4.dropna()
        df4[df4.columns[0]] = df4[df4.columns[0]].astype(str)
        df4[df4.columns[1]] = pd.to_numeric(df4[df4.columns[1]], errors='coerce')
        df4 = df4.dropna()
        
        return df1, df2, df3, df4
    df1, df2, df3, df4 = cargar_datos()

    # Mostrar titulo
    st.title('Visualizacion de google sheet')
    radio = st.radio('¿Que tabla desea ver?', ['tabla 1', 'tabla 2', 'tabla 3', 'tabla 4'], horizontal=True)

    if radio == 'tabla 1':
        st.subheader('Jugadores de la nba entre la temporada 1996-97 a 2000-01')
        st.dataframe(df1)
    elif radio == 'tabla 2':
        @st.experimental_fragment(run_every=4)
        def carga_hoja2():
            _, df2, _, _ = cargar_datos()
            st.subheader('Cantidad de jugadores por equipo entre 1996-2000')
            st.dataframe(df2)

        @st.experimental_fragment(run_every=4)
        def grafico_hoja2():
            _, df2, _, _ = cargar_datos()
            st.subheader('Cantidad de jugadores en los principales equipos')
            fig = px.bar(
                df2,
                x=df2.columns[0],
                y=df2.columns[1],
                title="Jugadores en los principales equipos",
                color=df2.columns[0]
            )
            st.plotly_chart(fig, use_container_width=True)

        carga_hoja2()
        grafico_hoja2()
    elif radio == 'tabla 3':
        @st.experimental_fragment(run_every=4)
        def carga_hoja3():
            _, _, df3, _ = cargar_datos()
            st.subheader('Cantidad de jugadores por ronda de draft entre 1996-2000')
            st.dataframe(df3)

        @st.experimental_fragment(run_every=4)
        def grafico_hoja3():
            _, _, df3, _ = cargar_datos()
            st.subheader('Porcentaje de jugadores escogidos en 1ra y 2da ronda del draft (buscar draft si no lo conoce)')
            fig = px.pie(
                df3,
                values=df3.columns[1],
                names=df3.columns[0],
                title="Jugadores en primera y segunda ronda del draft",
            )
            st.plotly_chart(fig, use_container_width=True)

        carga_hoja3()
        grafico_hoja3()
    elif radio == 'tabla 4':
        @st.experimental_fragment(run_every=4)
        def carga_hoja4():
            _, _, _, df4 = cargar_datos()
            st.subheader('Cantidad de jugadores por temporada entre 1996-2000')
            st.dataframe(df4)

        @st.experimental_fragment(run_every=4)
        def grafico_hoja4():
            _, _, _, df4 = cargar_datos()
            st.subheader('Cantidad de jugadores en cada temporada')
            fig = px.bar(
                df4,
                x=df4.columns[0],
                y=df4.columns[1],
                title="Jugadores por temporada",
                color=df4.columns[0]
            )
            st.plotly_chart(fig, use_container_width=True)

        carga_hoja4()
        grafico_hoja4()
elif eleccion == 'IA':
    client = Groq(api_key='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')

    modelos = {'llama3-8b-8192', 'llama3-70b-8192', 'llama-3.3-70b-versatile'}
    # i es un fragmento de la respuesta que me dara la IA
    # i.choices[0] accede al primer resultado generado
    # i.choices[0].delta es el diccionario donde esta el contenido (la mejor respuesta por parte de la IA)
    # i.choices[0].delta.content es la clave de ese diccionario, osea, la respuesta a la pregunta que hizo el usuario
    def generar_respuestas_chat(respuesta_ia):
        for i in respuesta_ia:
            if i.choices[0].delta.content:
                yield i.choices[0].delta.content

    # inicializar el historial de streamlit
    # st.session_state.mensajes: es una lista que se usa para guardar historial completo del chat,
    # incluyendo lo que escribes como user y lo que responde la maquina
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = []

    # vamos a mostrar todo el historial del chat en la pantalla de streamlit
    # st.container(): crea un contenedor visual en streamlit
    # mensaje in st.session_state.mensajes: recorre uno a uno los mensajes que estan guardados en la lista que ya estan guardados en el historial del chat
    # st.chat_message(mensaje['role']): Crea una simulacion de un chat intercambiando roles entre usuario y maquina
    # st.markdown(mensaje['content']) muestra el contenido del mensaje (el texto del usuario o la IA)
        

    with st.container():
        for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje['role']):
                st.markdown(mensaje['content'])

    # mostramos la lista de modelos en el sidebar
    # index=0 por defecto me muestra el primer elemento en la lista de modelos
    parModelo = st.sidebar.selectbox('Modelos', options=modelos, index=0)
    if parModelo == 'llama-3.3-70b-versatile':
        st.sidebar.warning('modelo solo en ingles')
    prompt = st.chat_input('Pregunte sin miedo aqui')
    
    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.mensajes.append({'role': 'user', 'content': prompt})
        try:
            mensaje_conversaciones = st.session_state.mensajes
            respuesta_ia = client.chat.completions.create(
                model=parModelo,
                messages= mensaje_conversaciones,
                stream=True
            )
            with st.chat_message('assistant'):
                respuestas_bot = generar_respuestas_chat(respuesta_ia)
                #st.write_stream se encarga de recibir el generador de texto que se hizo con el yield
                respuesta_completa = st.write_stream(respuestas_bot)
            st.session_state.mensajes.append({'role': 'assistant', 'content':respuesta_completa})
        except Exception as e:
            st.error(e)
elif eleccion == 'Formulario':
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
        evidencia = st.file_uploader('Sube una imagen', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

        boton_enviar = st.form_submit_button("Enviar") # creamos el boton
        direccion_completa = direccion + ' ' + ciudad
    # Procesar y guardar
    archivo = 'registros.csv'
    if boton_enviar:
        ubicacion = geolocalizador.geocode(direccion_completa, timeout=10)
        conexion = sqlite3.connect('Quejas_ciudadanas.db')
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Quejas (Nombre, Apellido, Correo, Ciudad, Direccion, Telefono, Categoria, Descripcion) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, correo, ciudad, direccion_completa, telefono, categoria, descripcion))
        conexion.commit()
        conexion.close()
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
                writer.writerow([ciudad, direccion_completa, lat, lon, categoria]) # agrega los elementos a dichas columnas
            st.success("Formulario enviado y datos geolocalizados")   
                     
            
        else:
            st.error("Dirección no encontrada. Intenta escribirla de otra forma.")
elif eleccion == 'Mapa Quejas':
    archivo = 'registros.csv'
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)   
    
    TipoMapa= st.radio('Tipo de marcadores', options=['Grupo', 'Individual'], horizontal=True)
    mapa = folium.Map(location=[6.242827227796505, -75.6132478], zoom_start=10) # crea un mapa interactivo usando la librería Folium 
    if TipoMapa == 'Grupo':
        mapa_grupo = MarkerCluster().add_to(mapa) # Crea un grupo de marcadores agrupados en un mapa de Folium, y lo añade al mapa principal llamado mapa.
    #recorre fila por fila el DataFrame dfRestaurantes, y en cada iteración crea un marcador de Folium 
    # usando los datos de esa fila: la latitud, longitud y el nombre del restaurante.
    for index, row in df.iterrows():
        if row['Categoría'] == '🔴 Seguridad':
            marker = folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=row['Categoría'],
                icon=folium.Icon(color="red", icon="remove-sign"), # 'info-sign', 'cloud', 'ok-sign', 'remove-sign','star', 'heart', 'flag', 'home', 'gift', 'glass','leaf', 'fire', 'camera', 'envelope', 'bell'
                )
        elif row['Categoría'] == '🔵 Servicios':
            marker = folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=row['Categoría'],
                icon=folium.Icon(color="blue", icon="info-sign"),
                )
        elif row['Categoría'] == '🟡 Infraestructura':
            marker = folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=row['Categoría'],
                icon=folium.Icon(color="green", icon="home"),
                )
        if TipoMapa == 'Grupo':
            marker.add_to(mapa_grupo)
        else:
            marker.add_to(mapa)
    # folium.plugins.Fullscreen Es un plugin de Folium que permite que el usuario pueda poner el mapa en modo pantalla completa        
    folium.plugins.Fullscreen(
        position="topright",
        title="Pantalla Completa",
        title_cancel="cancelar",
        force_separate_button=True, #Hace que el botón sea independiente, no dentro de otros controles del mapa.
    ).add_to(mapa)
    out = st_folium(mapa, height=600, use_container_width=True) # permite ver el mapa de folium
    #st.write(out) # permite ver las coordenadas en formato json donde me paro en el mapa
elif eleccion == 'Datos':
    st.header('Dataframe con los datos de longitud y latitud')
    contrasena = 'map1020'
    password = st.text_input('Contraseña', type='password')
    if password:
        if password == contrasena:
            # Mostrar tabla si el archivo existe
            archivo = 'registros.csv'
            if os.path.exists(archivo):
                    st.write("## Registros guardados con coordenadas:")
                    df = pd.read_csv(archivo)
                    st.dataframe(df)

        else:
            st.error('contraseña incorrecta')