import streamlit as st

def display_health_topics_page():
    if 'dataset' in st.session_state:
        health_topics_df = st.session_state.dataset.get_health_topics()
        st.title("Temas de Salud")
        st.dataframe(health_topics_df,
                     height=get_output_height(health_topics_df),
                     use_container_width=True,
                     column_config={'Título': st.column_config.Column(width="medium"),
                                    'URL': st.column_config.LinkColumn()},
                     hide_index=True
                     )

        download_csv(health_topics_df, "temas_salud.csv")
    else:
        st.error("Ocurrió un error al renderizar la interfaz")


def display_sites_page():
    if 'dataset' in st.session_state:
        sites_df = st.session_state.dataset.get_sites()
        st.title("Sitios")
        st.dataframe(sites_df,
                     height=get_output_height(sites_df),
                     use_container_width=True,
                     column_config={'Título': st.column_config.Column(width="large"),
                                    'URL': st.column_config.LinkColumn(),
                                    'URL Otro Idioma': st.column_config.LinkColumn()},
                     hide_index=True
                     )

        download_csv(sites_df, "sitios.csv")
    else:
        st.error("Ocurrió un error al renderizar la interfaz")


def get_output_height(df):
    return min(700, 50 + 30 * len(df))


def download_csv(df, filename):
    csv = convert_df_to_csv(df)
    st.download_button(label="Descargar", data=csv, file_name=filename,
                       mime="text/csv")


@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')
