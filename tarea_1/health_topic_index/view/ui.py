from io import BytesIO
import streamlit as st

from health_topic_index.health_topic.dataset import HealthTopicDataset


# TODO: make this dynamic, so we can add or remove pages, and the sidebar will be updated
# TODO: add error page if data is not loaded, or the failure in process state
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
        # Set the sidebar
        self.display_sidebar()
        # Set a place holder for the main page
        with st.empty():
            self.display_pages()

    def display_sidebar(self):
        """
        Class method to display the sidebar of the GUI.
        """
        # Set the session state

        # Uploader
        data_file = st.sidebar.file_uploader(label="Archivo por procesar:",
                                             type=["xml"],
                                             key="upload_xml")

        # Initialize the app with the main page and return to main page if the data is not loaded
        if data_file is None and not st.session_state[self.home_page_name]:
            self.update_session_state(self.home_page_name)

        # reset the page
        # put the button at the end of the sidebar
        self.render_sidebar_buttons(data_file)

        # return the XML data file
        st.session_state['data_file'] = HealthTopicDataset.from_xml_file(data_file)

    def render_sidebar_buttons(self, data_file: BytesIO):
        """
        Render the buttons of the pages in the sidebar.
        """
        # Create a container for the sidebar
        with st.sidebar.container():
            for page_name in self.pages.keys():
                # Create a button for each page
                # Type change to primary when is Inicio
                is_disabled = data_file is None and page_name != self.home_page_name
                page_type = "primary" if page_name == self.home_page_name else "secondary"

                if st.sidebar.button(label=page_name, use_container_width=True, disabled=is_disabled, type=page_type):
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
            st.session_state[page_name] = (page_name == active_page)
        st.rerun()

    def display_pages(self):
        """
        Render the pages of the pages dict.
        """
        # Check the page to display
        for name, function in self.pages.items():
            if st.session_state[name]:
                with st.container():
                    function()
