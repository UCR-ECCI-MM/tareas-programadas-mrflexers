import streamlit as st


def display_data_statistics_page():
    st.title("Estadísticas")

    if 'dataset' in st.session_state:
        df = st.session_state.dataset.get_top_info_cat()
        st.write('## Categorías de Información más populares')
        st.bar_chart(df, x_label='Categoría de Información', y_label='Conteo de Temas')
