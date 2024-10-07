import streamlit as st

from health_topic_index.health_topic.dataset import HealthTopicDataset


def display_main_page():
    # Home Page data: here show the app name, description, and the options of funct
    st.markdown("# Índice de Temas de Salud :hospital:")

    if st.session_state['dataset'] is None:
        st.markdown("### _Subir un archivo de temas de salud o cargar desde MedlinePlus para comenzar_")

    MAX_FILE_SIZE = 150 * 1024 * 1024  # 150MB

    if st.session_state['dataset'] is not None:
        if st.session_state['dataset_source'] == 'uploader':
            if st.session_state['data_file'].size > MAX_FILE_SIZE:
                st.error("Por favor subir un archivo de tamaño menor a 150MB.")
                return
        # Proceed to display general data
        display_general_data_main_page(st.session_state['dataset'])


# General data into the main page
def display_general_data_main_page(file: HealthTopicDataset):
    """Display general data of the XML file in the main page."""

    if st.session_state['dataset'] is None:
        st.error("El archivo no se pudo procesar, por favor subir un archivo MedlinePlus XML válido.")
    else:
        file_name = st.session_state['data_file'].name

        st.markdown(
            f"""
            ___
            ## Información General

            |                              |                                    |
            |------------------------------|------------------------------------|
            |    __Nombre del archivo__    | {file_name} |
            | __Fecha y hora de creación__ | {file.timestamp} |
            |    __Número de registros__   | {file.size.iloc[0]} |
            """
        )
