import streamlit as st

from health_topic_index.health_topic.dataset import HealthTopicDataset


def display_main_page():
    # Home Page data: here show the app name, description, and the options of funct
    st.markdown("""
        ## Índice de Temas de Salud :hospital:

        Arrastrar un archivo XML al panel de navegación, y luego seleccionar la opción deseada para explorar los datos.
        """
    )

    MAX_FILE_SIZE = 150 * 1024 * 1024  # 150MB

    if st.session_state.upload_file is not None:
        if st.session_state.upload_file.size > MAX_FILE_SIZE:
            st.error("El archivo es muy grande, por favor subir un archivo de tamaño menor a 200MB.")
        else:
            # Get path, and pass to load
            # avail three option buttons when my_upload is not None
            display_general_data_main_page(st.session_state.dataset)


# General data into the main page
def display_general_data_main_page(file: HealthTopicDataset):
    """Display general data of the XML file in the main page."""
    st.markdown(
        f"""
        ___
        ## Información General

        |                              |                                    |
        |------------------------------|------------------------------------|
        |    __Nombre del archivo__    | {st.session_state.upload_file.name} |
        | __Fecha y hora de creación__ |                   {file.timestamp} |
        |    __Número de registros__   |                {file.size.iloc[0]} |
        """
    )
