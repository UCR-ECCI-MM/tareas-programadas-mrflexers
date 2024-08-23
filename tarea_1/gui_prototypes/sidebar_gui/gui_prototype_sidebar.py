
import streamlit as st

st.set_page_config(layout="wide", page_title="XML Data Fixer")

def display_sidebar():
    # navigation menu
    st.sidebar.markdown("# Sidebar Panel")

    # Uploader

    datafile = st.sidebar.file_uploader(label="Upload XML data file",
                             type=["xml"],
                             key="upload_xml")

    # reset the page
    # put the button at the end of the sidebar
    with st.sidebar.container():
        if st.sidebar.button("Home", key="home", type="primary", use_container_width=True):
            st.session_state['data_stadistics'] = False
            st.session_state['specific_data'] = False
            st.session_state['feature'] = False
            st.session_state['mainpage'] = True
            # recharge the page to the main page
            st.rerun()

    # Buttons to functionalities
    st.sidebar.markdown("## Functions")
    with st.sidebar.container():
        if st.sidebar.button("Show data statistics", key="option1",use_container_width=True):
            st.session_state['data_stadistics'] = True
            st.session_state['specific_data'] = False
            st.session_state['feature'] = False
            st.session_state['mainpage'] = False

        if st.sidebar.button("Search specific data", key="option2", use_container_width=True):
            st.session_state['data_stadistics'] = False
            st.session_state['specific_data'] = True
            st.session_state['feature'] = False
            st.session_state['mainpage'] = False

        if st.sidebar.button("Feature", key="option3",use_container_width=True):
            st.session_state['data_stadistics'] = False
            st.session_state['specific_data'] = False
            st.session_state['feature'] = True
            st.session_state['mainpage'] = False





def display_mainpage():

    # Home Page data: here show the app name, description, and the options of funct
    st.markdown("""
        ## XML Data Fixer :wrench:
        Computabilidad y Complejidad, **Parser** y **Lexer** de XML, Proyecto 1.

        First drag and drop the XML file to the sidebar panel, then select the options to fix the XML data.

        ### Functions over the XML data:
        1. **Show data statdistics**: Show the general data of the XML file with tables and graphs.
        2. **Search specific data**: Search for specific data in the XML file. Do a query to the XML data.
        3. **Feature**: Download the fixed image.
        """
    )

    #col1, col2 = st.columns(2)
    MAX_FILE_SIZE = 150 * 1024 * 1024  # 150MB

    if st.session_state.upload_xml is not None:
        if st.session_state.upload_xml.size > MAX_FILE_SIZE:
            st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
        else:
            # avail three option buttons when my_upload is not None
            display_general_data_mainpage()
    else:
        pass


def display_general_data_mainpage():
    st.markdown(
        f"""
        ___
        ## General Dataset Information
        __File name__: {st.session_state.upload_xml.name} \n
        __Register Amount__: 100 \n
        __Date__: 2021-10-01 \n
        __Time__: 12:00:00 \n
        """
    )

def display_pages():
    # Check the page to display
    if st.session_state['mainpage']:
        with st.container():
            display_mainpage()

    if st.session_state['data_stadistics']:
        with st.container():
            st.title("Data Statistics")
            st.markdown(
                """
                ## Data Statistics
                This page shows the general data of the XML file with tables and graphs.
                """
            )

    if st.session_state['specific_data']:
        with st.container():
            st.title("Search specific data")
            st.markdown(
                """
                ## Search specific data
                This page shows the general data of the XML file with tables and graphs.
                """
            )

    if st.session_state['feature']:
        with st.container():
            st.title("Feature")



# Set the session state
if 'option1_pressed' not in st.session_state:
    # Initialize the button pressed
    st.session_state['data_stadistics'] = False # Show data statistics
    st.session_state['specific_data'] = False # Search specific data
    st.session_state['feature'] = False # Feature
    st.session_state['mainpage'] = True

 # set the sidebar
display_sidebar()
# Set a place holder for the main page
with st.empty():
    display_pages()
