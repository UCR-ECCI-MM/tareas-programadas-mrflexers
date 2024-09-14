
import streamlit as st

def display_health_themes_page():
    st.title("Temas de Salud")

    if 'data_file' in st.session_state:
        st.dataframe(st.session_state['data_file'].get_health_topics(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn()},
                     hide_index=True)


def display_sites_page():
    st.title("Sitios")

    if 'data_file' in st.session_state:
        st.dataframe(st.session_state['data_file'].get_sites(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn(),
                                    'URL Otro Idioma': st.column_config.LinkColumn()},
                     hide_index=True)
