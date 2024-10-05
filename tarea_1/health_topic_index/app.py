from health_topic_index.view import (
    UI,
    display_main_page,
    display_data_statistics_page,
    display_health_themes_page,
    display_sites_page,
)

def main():
    # Initialize the GUI
    gui = UI()

    # add pages to gui
    gui.add_page("Inicio", display_main_page)
    gui.add_page("Estadísticas", display_data_statistics_page)
    gui.add_page("Temas de Salud", display_health_themes_page)
    gui.add_page("Sitios", display_sites_page)

    # Run the GUI
    gui.run()

if __name__ == "__main__":
    main()
