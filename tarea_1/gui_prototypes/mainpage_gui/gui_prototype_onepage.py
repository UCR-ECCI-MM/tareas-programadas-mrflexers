import streamlit as st

st.set_page_config(page_title="XML Data Fixer")

# Display the main page information
def display_mainpage():

    # Home Page data: here show the app name, description, and the options of funct
    st.markdown("""
        ## XML Data Fixer :wrench:
        Computabilidad y Complejidad, **Parser** y **Lexer** de XML, Proyecto 1.

        ### Functions over the XML data:
        1. **Show data statdistics**: Show the general data of the XML file with tables and graphs.
        2. **Search specific data**: Search for specific data in the XML file. Do a query to the XML data.
        3. **Feature**: Download the fixed image.
        """
    )

    # create a let's start button centered
    with st.container():
        if st.button("Let's start", key="start", type="primary", use_container_width=True):
            st.switch_page("pages/analyst_menu.py")



display_mainpage()

