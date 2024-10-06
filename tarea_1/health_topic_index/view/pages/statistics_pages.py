from io import BytesIO
import altair as alt
import vl_convert as vlc
import streamlit as st
import pandas as pd

def display_data_statistics_page():
    st.title("Estadísticas")

    if 'dataset' in st.session_state:
        # obtain from the dataset the top information categories
        df = st.session_state.dataset.get_top_info_cat()


        st.write('## Categorías de Información más populares')

        # Create the bar chart
        bar_chart = create_bar_chart(df, 'Conteo de temas', 'Categoría de Información')

        # use on_select when the graph need to be dynamic
        st.altair_chart(bar_chart, use_container_width=True)

        # Aquí se genera el gráfico en bytes
        chart_in_bytes = chart_to_bytes(bar_chart)

        # Una vez que el gráfico esté listo, reemplazar el botón con uno habilitado
        st.download_button(
            label="Descargar",
            data=chart_in_bytes,
            file_name="cat_mas_populares.png",
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
    value_column = df.columns[1] # name of the column with the values
    label_column = df.columns[0] # name of the column with the labels

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
def chart_to_bytes(_chart: alt.Chart) -> BytesIO:
    """
    Convert an Altair chart to a PNG image.
    ---
    _chart : alt.Chart
        The Altair chart to convert to PNG.
        Have a _ to avoid hashing the chart object.
    """
    chart_bytes = vlc.vegalite_to_png(_chart.to_dict())
    return chart_bytes
