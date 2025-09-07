from django.apps import AppConfig
import os
from django.db.utils import OperationalError
from django.db import connections

class AdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_app'

    def ready(self):
        from django.contrib.auth import get_user_model

        # Only run if environment variable is set
        if os.environ.get("CREATE_SUPERUSER", "False") == "True":
            try:
                # Check if the database is ready
                db_conn = connections['default']
                db_conn.cursor()
            except OperationalError:
                return

            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                print("Creating superuser...")
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="SuperSecretPassword123"
                )
                print("Superuser created!")
