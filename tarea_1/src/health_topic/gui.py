
import streamlit as st
from .pages.main_page import display_main_page
from .pages.stadistics_pages import display_data_statistics_page
from .pages.tables_pages import display_health_themes_page, display_sites_page
from .dataset import HealthTopicDataset


# TODO: make this dynamic, so we can add or remove pages, and the sidebar will be updated
# TODO: add error page if data is not loaded, or the failure in process state
class Gui:
    """
    Class to manage the different pages of the GUI
    """

    # Pages to display
    pages = {
        "main_page": display_main_page,
        "data_statistics": display_data_statistics_page,
        "health_themes_table": display_health_themes_page,
        "sites_table": display_sites_page,
    }

    def __init__(self):
        st.set_page_config(layout="wide", page_title="Índice de Temas de Salud")


    # TODO: use this when before the run method to add new pages, to be able of expand the GUI
    def add_page(self, name, function):
        """
        Class method to add a page to the GUI
        """
        self.pages[name] = function

    def run(self):
        """
        Class method to run the GUI in the application
        """
        # Set the session state
        if 'option1_pressed' not in st.session_state:
            # Initialize the button pressed
            st.session_state['main_page'] = True
            st.session_state['data_statistics'] = False
            st.session_state['health_themes_table'] = False
            st.session_state['sites_table'] = False

        # set the sidebar
        self.display_sidebar()
        # Set a place holder for the main page
        with st.empty():
            self.display_pages()


    # TODO: make this dynamic, so we can add or remove pages, and the sidebar will be updated
    def display_sidebar(self):
        """
        Class method to display the sidebar of the GUI
        """
        # Uploader
        data_file = st.sidebar.file_uploader(label="Archivo por procesar:",
                                            type=["xml"],
                                            key="upload_xml")

        # reset the page
        # put the button at the end of the sidebar
        with st.sidebar.container():
            if st.sidebar.button("Inicio", key="home", type="primary",
                                 use_container_width=True):
                st.session_state['main_page'] = True
                st.session_state['data_statistics'] = False
                st.session_state['health_themes_table'] = False
                st.session_state['sites_table'] = False
                # recharge the page to the main page
                st.rerun()

        # Buttons to functionalities, they are going to be in the sidebar
        # buttons activates when the data_file is already uploaded
        with st.sidebar.container():
            if st.sidebar.button("Estadísticas", key="option1", use_container_width=True,
                                disabled=data_file is None):
                st.session_state['main_page'] = False
                st.session_state['data_statistics'] = True
                st.session_state['health_themes_table'] = False
                st.session_state['sites_table'] = False

            if st.sidebar.button("Temas de Salud", key="option2", use_container_width=True,
                                disabled=data_file is None):
                st.session_state['main_page'] = False
                st.session_state['data_statistics'] = False
                st.session_state['health_themes_table'] = True
                st.session_state['sites_table'] = False

            if st.sidebar.button("Sitios", key="option3", use_container_width=True,
                                 disabled=data_file is None):
                st.session_state['main_page'] = False
                st.session_state['data_statistics'] = False
                st.session_state['health_themes_table'] = False
                st.session_state['sites_table'] = True

        # return the XML data file
        st.session_state['data_file'] = HealthTopicDataset.from_xml_file(data_file)

    def display_pages(self):
        """
        Class method to display the pages of pages dict
        """
        # Check the page to display
        pages = self.pages
        for page in pages:
            if st.session_state[page]:
                with st.container():
                    pages[page]()
