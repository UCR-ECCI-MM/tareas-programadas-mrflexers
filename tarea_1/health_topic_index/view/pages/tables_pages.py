import streamlit as st


def display_health_themes_page():
    st.title("Temas de Salud")

    if 'dataset' in st.session_state:
        health_topics_df = st.session_state.dataset.get_health_topics()
        st.dataframe(health_topics_df,
                     height=get_output_height(health_topics_df),
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn()},
                     hide_index=True
                     )

        download_csv(health_topics_df, "temas_salud.csv")


def display_sites_page():
    st.title("Sitios")

    if 'dataset' in st.session_state:
        sites_df = st.session_state.dataset.get_sites()
        st.dataframe(sites_df,
                     height=get_output_height(sites_df),
                     use_container_width=True,
                     column_config={'URL': st.column_config.LinkColumn(),
                                    'URL Otro Idioma': st.column_config.LinkColumn()},
                     hide_index=True
                     )

        download_csv(sites_df, "sitios.csv")


def get_output_height(df):
    return min(600, 50 + 30 * len(df))


def download_csv(df, filename):
    csv = convert_df_to_csv(df)
    st.download_button(label="Descargar", data=csv, file_name=filename,
                       mime="text/csv")


@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')
