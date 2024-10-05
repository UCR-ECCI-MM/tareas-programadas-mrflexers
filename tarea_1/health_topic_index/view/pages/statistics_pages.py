from io import BytesIO
import altair as alt
import vl_convert as vlc
import streamlit as st

def display_data_statistics_page():
    st.title("Estadísticas")

    if 'dataset' in st.session_state:
        # obtain from the dataset the top information categories
        df = st.session_state.dataset.get_top_info_cat()

        value_column = df.columns[1]
        label_column = df.columns[0]

        st.write('## Categorías de Información más populares')

        # Create the bar chart
        bar_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f'{value_column}:Q', title='Conteo de Temas'),
            y=alt.Y(f'{label_column}:N', title='Categoría de Información', sort='-x'),
            tooltip=[label_column, value_column]  # to show details on hover
        ).configure_axis(
            labelLimit=200,  # Adjust the limit of large labels
        ).properties(
            width=1000,
            height=500  # Height of the chart
        )

        # use on_select when the graph need to be dynamic
        st.altair_chart(bar_chart, use_container_width=True)


    # Generar botones de descarga para PNG y SVG
    st.download_button(
        label="Descargar",
        data=chart_to_bytes(bar_chart),
        file_name="cat_mas_populares.png",
        mime="image/png",
    )


def chart_to_bytes(chart: alt.Chart) -> BytesIO:
    chart_bytes = vlc.vegalite_to_png(chart.to_dict())
    return chart_bytes
