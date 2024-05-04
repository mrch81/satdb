from django.apps import AppConfig
from utils.tle_updater import TLEUpdater


class SatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'satapp'

    def ready(self):
        tle_updater = TLEUpdater()
        tle_updater.start()
