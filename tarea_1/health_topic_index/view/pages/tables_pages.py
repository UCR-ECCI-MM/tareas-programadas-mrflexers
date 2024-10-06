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

        download_csv(st.session_state.dataset.get_health_topics(), "temas_salud.csv")


def display_sites_page():
    st.title("Sitios")

    if 'dataset' in st.session_state:
        # TODO: description column not needed
        st.dataframe(st.session_state.dataset.get_sites(),
                     height=600,
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn(),
                                    'URL Otro Idioma': st.column_config.LinkColumn()},
                     hide_index=True
        )

        download_csv(st.session_state.dataset.get_sites(), "sitios.csv")


def download_csv(df, filename):
    csv = convert_df_to_csv(df)
    st.download_button(label="Descargar", data=csv, file_name=filename,
                       mime="text/csv")

@st.cache_data
def convert_df_to_csv(df):
   return df.to_csv(index=False).encode('utf-8')

