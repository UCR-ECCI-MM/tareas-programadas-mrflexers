
import streamlit as st
from ..dataset import HealthTopicDataset

def display_main_page():
    # Home Page data: here show the app name, description, and the options of funct
    st.markdown("""
        ## Índice de Temas de Salud :hospital:

        Arrastrar un archivo XML al panel de navegación, y luego seleccionar la opción deseada para explorar los datos.
        """
                )

    # col1, col2 = st.columns(2)
    MAX_FILE_SIZE = 150 * 1024 * 1024  # 150MB

    if st.session_state.upload_xml is not None:
        if st.session_state.upload_xml.size > MAX_FILE_SIZE:
            st.error("El archivo es muy grande, por favor subir un archivo de tamaño menor a 200MB.")
        else:
            # Get path, and pass to load
            # avail three option buttons when my_upload is not None
            display_general_data_main_page(st.session_state['data_file'])


# General data into the main page
def display_general_data_main_page(file: HealthTopicDataset):
    """Display general data of the XML file in the main page."""
    st.markdown(
        f"""
        ___
        ## Información General

        |                              |                                    |
        |------------------------------|------------------------------------|
        |    __Nombre del archivo__    | {st.session_state.upload_xml.name} |
        | __Fecha y hora de creación__ |                   {file.timestamp} |
        |    __Número de registros__   |                {file.size.iloc[0]} |
        """
    )