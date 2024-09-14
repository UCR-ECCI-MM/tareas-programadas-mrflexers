
import streamlit as st

# TODO: Agregar página de error y tirarla en caso que falte data_file

def display_error_page():
    st.title("Error")
    st.write("No se ha cargado el archivo de datos. Por favor, cargue un archivo de datos.")
