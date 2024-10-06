from health_topic_index import setup_logger

from health_topic_index.view import (
    UI,
    display_main_page,
    display_data_statistics_page,
    display_health_themes_page,
    display_sites_page,
)

logger = setup_logger(__name__)


def main():
    # Initialize the GUI
    gui = UI()

    # add pages to gui
    gui.add_page("Inicio", display_main_page)
    gui.add_page("Estadísticas", display_data_statistics_page)
    gui.add_page("Temas de Salud", display_health_themes_page)
    gui.add_page("Sitios", display_sites_page)

    # Run the GUI
    try:
        gui.run()
    except Exception:
        logger.exception("An error occurred in the main app")

if __name__ == "__main__":
    main()
