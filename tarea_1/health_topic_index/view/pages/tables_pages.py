import streamlit as st

def display_health_themes_page():
    st.title("Temas de Salud")

    if 'dataset' in st.session_state:
        st.dataframe(st.session_state.dataset.get_health_topics(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn()},
                     hide_index=True
        )

        csv = convert_df_to_csv(st.session_state.dataset.get_health_topics())

        st.download_button(label="Descargar como CSV", data=csv, file_name="temas_de_salud.csv",
                           mime="text/csv", icon=":material/download:")


def display_sites_page():
    st.title("Sitios")

    if 'dataset' in st.session_state:
        # TODO: descripcion column not needed
        st.dataframe(st.session_state.dataset.get_sites(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn(),
                                    'URL Otro Idioma': st.column_config.LinkColumn()},
                     hide_index=True
        )

        csv = convert_df_to_csv(st.session_state.dataset.get_health_topics())

        st.download_button(label="Descargar como CSV", data=csv, file_name="temas_de_salud.csv",
                           mime="text/csv", icon=":material/download:")

@st.cache_data
def convert_df_to_csv(df):
   return df.to_csv(index=False).encode('utf-8')

