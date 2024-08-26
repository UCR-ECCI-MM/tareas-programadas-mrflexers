import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from pandas import DataFrame
from streamlit import columns

from health_topic.dataset import HealthTopicDataset

# TODO: Agregar página de error y tirarla en caso que falte data_file

st.set_page_config(layout="wide", page_title="Índice de Temas de Salud")


def display_sidebar():
    # Uploader
    data_file = st.sidebar.file_uploader(label="Archivo por procesar:",
                                         type=["xml"],
                                         key="upload_xml")

    # reset the page
    # put the button at the end of the sidebar
    with st.sidebar.container():
        if st.sidebar.button("Inicio", key="home", type="primary", use_container_width=True):
            st.session_state['data_statistics'] = False
            st.session_state['specific_data'] = False
            st.session_state['feature'] = False
            st.session_state['main_page'] = True
            # recharge the page to the main page
            st.rerun()

    # Buttons to functionalities, they are going to be in the sidebar
    # buttons activates when the data_file is already uploaded
    with st.sidebar.container():
        if st.sidebar.button("Temas de Salud", key="option2", use_container_width=True,
                             disabled=data_file is None):
            st.session_state['data_statistics'] = False
            st.session_state['specific_data'] = True
            st.session_state['feature'] = False
            st.session_state['main_page'] = False

        if st.sidebar.button("Sitios", key="option3", use_container_width=True, disabled=data_file is None):
            st.session_state['data_statistics'] = False
            st.session_state['specific_data'] = False
            st.session_state['feature'] = True
            st.session_state['main_page'] = False

        if st.sidebar.button("Estadísticas", key="option1", use_container_width=True,
                             disabled=data_file is None):
            st.session_state['data_statistics'] = True
            st.session_state['specific_data'] = False
            st.session_state['feature'] = False
            st.session_state['main_page'] = False

    # return the XML data file
    st.session_state['data_file'] = HealthTopicDataset.from_xml_file(data_file)


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
            st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
        else:
            # Get path, and pass to load
            # avail three option buttons when my_upload is not None
            display_general_data_main_page(st.session_state['data_file'])
    else:
        pass


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
        |    __Número de registros__   |                     {file.size[0]} |
        """
    )


def display_pages():
    # Check the page to display
    for page in pages:
        if st.session_state[page]:
            with st.container():
                pages[page]()


# define pages
def display_data_statistics_page():
    st.title("Estadísticas")

    if 'data_file' in st.session_state:
        df = st.session_state['data_file'].get_top_info_cat()
        st.write('## Categorías de Información más populares')
        st.bar_chart(df, x_label='Categoría de Información', y_label='Conteo de Temas')

def display_specific_data_page():
    st.title("Temas de Salud")

    if 'data_file' in st.session_state:
        st.dataframe(st.session_state['data_file'].get_health_topics(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn()},
                     hide_index=True)


def display_other_page():
    st.title("Sitios")

    if 'data_file' in st.session_state:
        st.dataframe(st.session_state['data_file'].get_sites(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn(),
                                    'URL Otro Idioma': st.column_config.LinkColumn()},
                     hide_index=True)

pages = {
    'main_page': display_main_page,
    'data_statistics': display_data_statistics_page,
    'specific_data': display_specific_data_page,
    'feature': display_other_page
}


def display_gui():
    # Set the session state
    if 'option1_pressed' not in st.session_state:
        # Initialize the button pressed
        st.session_state['data_statistics'] = False  # Show data statistics
        st.session_state['specific_data'] = False  # Search specific data
        st.session_state['feature'] = False  # Feature
        st.session_state['main_page'] = True

    # set the sidebar
    display_sidebar()
    # Set a place holder for the main page
    with st.empty():
        display_pages()


# Display DF and sidebar with different statistical views over data
display_gui()
