from io import BytesIO
import altair as alt
import vl_convert as vlc
import streamlit as st
import pandas as pd


def display_data_statistics_page():
    st.title("Estadísticas")

    if 'dataset' in st.session_state:
        # obtain from the dataset the top information categories
        top_info_cat_df = st.session_state.dataset.get_top_info_cat()

        # Create the bar chart
        bar_chart = create_bar_chart(top_info_cat_df, 'Conteo de temas', 'Categoría de Información')

        st.session_state.bar_chart_in_bytes = chart_to_bytes(bar_chart)

        # obtain from the dataset the update frequency
        update_frequency_df = st.session_state.dataset.get_update_frequency()

        # Create the line chart
        line_chart = create_line_chart(update_frequency_df, 'Fecha', 'Total de Temas de Salud')

        st.session_state.line_chart_in_bytes = chart_to_bytes(line_chart)

        st.write('## Categorías de Información más populares')

        st.altair_chart(bar_chart, use_container_width=True)

        st.download_button(
            label="Descargar",
            data=st.session_state.bar_chart_in_bytes,
            file_name="cat_mas_populares.png",
            mime="image/png",
            disabled=False,
        )

        st.write('## Frecuencia de Actualización de Temas de Salud')

        st.altair_chart(line_chart, use_container_width=True)

        st.download_button(
            label="Descargar",
            data=st.session_state.line_chart_in_bytes,
            file_name="frecuencia_de_temas.png",
            mime="image/png",
            disabled=False,
        )


# Cache the data to avoid recalculating it each time the state of page change
@st.cache_data
def create_bar_chart(df: pd.DataFrame, x_title: str, y_title: str) -> alt.Chart:
    """
    Create an Altair chart.
    ---
    df : pd.DataFrame
        The data to plot.
    x_title : str
        The title of the x-axis.
    y_title : str
        The title of the y-axis.
    """
    value_column = df.columns[1]  # name of the column with the values
    label_column = df.columns[0]  # name of the column with the labels

    # Create the bar chart
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{value_column}:Q', title=x_title),
        y=alt.Y(f'{label_column}:N', title=y_title, sort='-x'),
        tooltip=[label_column, value_column]  # to show details on hover
    ).configure_axis(
        labelLimit=200,  # Adjust the limit of large labels
    ).properties(
        width=1000,
        height=500  # Height of the chart
    )

    return bar_chart


@st.cache_data
def create_line_chart(df: pd.DataFrame, x_title: str, y_title: str) -> alt.LayerChart:
    """
    Create an Altair chart.
    ---
    df : pd.DataFrame
        The data to plot.
    x_title : str
        The title of the x-axis.
    y_title : str
        The title of the y-axis.
    """
    # Create the line chart
    line_chart = alt.Chart(df).mark_line(opacity=0.5).encode(
        x=alt.X('Fecha:T', title=x_title),
        y=alt.Y('Total de Temas de Salud:Q', title=y_title)
    )

    points_chart = alt.Chart(df).mark_point(shape='diamond', size=30).encode(
        x=alt.X('Fecha:T'),
        y=alt.Y('Total de Temas de Salud:Q'),
        size=alt.Size('Temas Agregados:Q'),
        tooltip=['Fecha', 'Temas Agregados', 'Total de Temas de Salud']  # to show details on hover
    )

    chart = (line_chart + points_chart).properties(width=1000, height=500)

    return chart


def chart_to_bytes(_chart) -> bytes:
    """
    Convert an Altair chart to a PNG image.
    ---
    _chart
        The Altair chart to convert to PNG.
        Have a _ to avoid hashing the chart object.
    """
    chart_bytes = vlc.vegalite_to_png(_chart.to_dict())
    return chart_bytes
