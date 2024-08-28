
from health_topic.gui import Gui

from health_topic.pages.main_page import display_main_page
from health_topic.pages.stadistics_pages import display_data_statistics_page
from health_topic.pages.tables_pages import display_health_themes_page, display_sites_page

# TODO: add error page if data is not loaded, or the failure in process state

# Initialize the GUI
gui = Gui()

# add pages to gui
gui.add_page("Inicio", display_main_page)
gui.add_page("Estadísticas", display_data_statistics_page)
gui.add_page("Temas de Salud", display_health_themes_page)
gui.add_page("Sitios", display_sites_page)

# Run the GUI
gui.run()
