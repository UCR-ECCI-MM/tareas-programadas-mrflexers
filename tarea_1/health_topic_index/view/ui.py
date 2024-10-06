import streamlit as st
from health_topic_index import setup_logger

from health_topic_index.health_topic.dataset import HealthTopicDataset

logger = setup_logger(__name__)


class UI:
    """
    Class to manage the different pages of the GUI.
    """

    def __init__(self):
        # Initialize the pages
        self.pages = {}
        self.home_page_name = None
        st.set_page_config(layout="wide", page_title="Índice de Temas de Salud")

    def add_page(self, name: str, function: callable):
        """
        Class method to add a page to the GUI.

        Parameters
        ----------
        name : str
            The name of the page to add.
        function : callable
            The function to display the page.

        Warnings
        --------
        The first added page will be set as the home page.
        """
        self.pages[name] = function

        # Set the first added page as the home page
        if not self.home_page_name:
            self.home_page_name = name

        # Initialize the session state of the new page
        if name not in st.session_state:
            st.session_state[name] = False

    def run(self):
        """
        Class method to run the GUI in the application
        """
        try:
            # Set the sidebar
            self.display_sidebar()
            # Set a place holder for the main page
            with st.empty():
                self.display_pages()
        except Exception:
            logger.exception("An error occurred while rendering the GUI")
            st.error("Ocurrió un error al renderizar la interfaz")

    def display_sidebar(self):
        """
        Class method to display the sidebar of the GUI.
        """
        with st.sidebar:
            # Uploader
            data_file = st.file_uploader(label="Archivo por procesar:",
                                         type=["xml"],
                                         key="upload_file")

            # If the file is not uploaded, initialize the dataset and the home page
            if data_file is None:
                # Initialize the session variable of the dataset
                st.session_state['dataset'] = None
                if not st.session_state[self.home_page_name]:
                    self.update_session_state(self.home_page_name)
            else:
                if st.session_state['dataset'] is None:
                    try:
                        st.session_state['dataset'] = HealthTopicDataset.from_xml_file(data_file)
                    except Exception:
                        logger.exception("An error occurred while loading the dataset")

            # reset the page
            # put the button at the end of the sidebar
            with st.container():
                self.render_sidebar_buttons()
                self.render_sidebar_search()

    def render_sidebar_buttons(self):
        """
        Render the buttons of the pages in the sidebar.
        """
        # Create a button for each page
        for page_name in self.pages.keys():
            # Create a button for each page
            # Type change to primary when is Inicio
            is_disabled = st.session_state.dataset is None and page_name != self.home_page_name
            page_type = "primary" if page_name == self.home_page_name else "secondary"

            if st.button(label=page_name, use_container_width=True,
                         disabled=is_disabled, type=page_type):
                self.update_session_state(page_name)

    def update_session_state(self, active_page: str):
        """
        Update the session state of the pages.

        Parameters
        ----------
        active_page : str
            The name of the active page.
        """
        for page_name in self.pages.keys():
            st.session_state[page_name] = page_name == active_page
        # TODO: look if this is necessary, because can cause a rerender of dataset
         st.rerun()

    def render_sidebar_search(self):
        # add a separator
        st.markdown("---")
        # show the search box if dataset is not None
        if st.session_state.dataset is not None:
            input_search_text = st.text_input(
                label="Buscador inteligente",
               # on_change=self.send_filter_command,
                placeholder="Escriba aquí..."
            )
            if st.button("Buscar"):
                self.send_filter_command(input_search_text)

    def send_filter_command(self, text: str):
        """
        Send the search box value to the search engine to filter the dataset.
        """
        print(text)
        st.session_state['dataset'].semantic_filter(text)

    def display_pages(self):
        """
        Render the pages of the pages dict.
        """
        # Check the page to display
        for name, function in self.pages.items():
            if st.session_state[name]:
                with st.container():
                    function()
