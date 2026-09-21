from django.apps import AppConfig


class DatabaseConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.database"

    def ready(self):

        from config.database import connect_db

        connect_db()