import requests
from io import BytesIO
from datetime import datetime, timedelta

import streamlit as st

from health_topic_index import setup_logger

from health_topic_index.health_topic.dataset import HealthTopicDataset

MEDLINEPLUS_FILE_URL = "https://medlineplus.gov/xml/mplus_topics_{date}.xml"

logger = setup_logger(__name__)


class UI:
    """
    Class to manage the different pages of the GUI.
    """

    @staticmethod
    def _date_generator():
        current_date = datetime.today()
        while True:
            yield current_date.strftime("%Y-%m-%d")
            current_date -= timedelta(days=1)

    @staticmethod
    def _fetch_file_from_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            file_content = response.content
            file_name = url.split('/')[-1]  # Extract the file name from the URL
            # Create a BytesIO object
            file_buffer = BytesIO(file_content)
            file_buffer.name = file_name  # Set the name attribute
            # Optionally, set the content type
            file_buffer.type = response.headers.get('Content-Type')
            return file_buffer
        else:
            return None

    def __init__(self):
        # Initialize the pages
        self.pages = {}
        self.home_page_name = None
        st.set_page_config(
            layout="wide",
            page_title="Índice de Temas de Salud",
            page_icon=":robot_face:"
        )

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
            self._display_sidebar()
            # Set a place holder for the main page
            with st.empty():
                self._display_pages()
        except Exception:
            logger.exception("An error occurred while rendering the GUI")
            st.error("Ocurrió un error al renderizar la interfaz")

    def _display_sidebar(self):
        """
        Class method to display the sidebar of the GUI.
        """
        with st.sidebar:
            # if st.button(label="Cargar datos de MedlinePlus", use_container_width=True):
            #     self._load_latest_data_from_medlineplus()
            #     if "upload_file" in st.session_state:
            #         st.session_state['upload_file'] = None

            # Uploader
            data_file = st.file_uploader(label="Archivo por procesar:",
                                         type=["xml"],
                                         key="upload_file")

            # If the file is not uploaded, initialize the dataset and the home page
            if data_file is None:
                # Initialize the session variable of the dataset
                st.session_state['file_id'] = None
                st.session_state['dataset'] = None
                if not st.session_state[self.home_page_name]:
                    self._update_active_page(self.home_page_name)
            else:
                incoming_file_id = data_file.file_id
                current_file_id = st.session_state['file_id']

                if current_file_id is None or incoming_file_id != current_file_id:
                    try:
                        st.session_state['dataset'] = HealthTopicDataset.from_xml_file(data_file)
                        st.session_state['file_id'] = incoming_file_id
                    except Exception:
                        logger.exception("An error occurred while loading the dataset")

            # reset the page
            # put the button at the end of the sidebar
            with st.container():
                self._render_sidebar_buttons()
                self._render_sidebar_search()

    def _render_sidebar_buttons(self):
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
                self._update_active_page(page_name)

    def _update_active_page(self, active_page: str):
        """
        Updates session state with regard to which page is active.

        Parameters
        ----------
        active_page : str
            The name of the active page.
        """
        for page_name in self.pages.keys():
            st.session_state[page_name] = page_name == active_page

    def _render_sidebar_search(self):
        # add a separator
        st.markdown("---")
        # show the search box if dataset is not None
        if st.session_state.dataset is not None:
            st.text_input(
                label="Filtro semántico",
                key="search_box",  # Clave para que el valor se almacene en st.session_state['search_box']
                on_change=self._send_filter_command,  # Función que se llamará cuando el texto cambie
                placeholder="Escriba aquí..."
            )

    def _send_filter_command(self):
        """
        Send the search box value to the search engine to filter the dataset.
        """
        search_term = st.session_state.get('search_box', '')

        st.session_state['dataset'].semantic_filter(search_term)

    def _display_pages(self):
        """
        Render the pages of the pages dict.
        """
        # Check the page to display
        for name, function in self.pages.items():
            if st.session_state[name]:
                with st.container():
                    function()

    def _load_latest_data_from_medlineplus(self):
        """
        Set file to the latest health topic file from medlineplus.gov

        Example: https://medlineplus.gov/xml/mplus_topics_2024-10-03.xml
        """
        date_gen = self._date_generator()
        latest_file = None
        for _ in range(7):
            date = next(date_gen)
            url = MEDLINEPLUS_FILE_URL.format(date=date)
            latest_file = self._fetch_file_from_url(url)
            if latest_file:
                try:
                    st.session_state['dataset'] = HealthTopicDataset.from_xml_file(latest_file)
                    st.session_state['file_id'] = 'web'
                except Exception:
                    logger.exception("An error occurred while loading the dataset")
                break

        if latest_file is None:
            st.error("No se pudo obtener el archivo más reciente de MedlinePlus")
