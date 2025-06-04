from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
    verbose_name = 'Appointment Booking System'

    def ready(self):
        import appointments.signals

        # Start the scheduler only if not in migration or testing
        from django.conf import settings
        from django.core.management import get_commands
        import sys

        # Check if we're running migrations or tests
        is_migration = 'migrate' in sys.argv or 'makemigrations' in sys.argv
        is_test = 'test' in sys.argv
        is_collectstatic = 'collectstatic' in sys.argv
        is_check = 'check' in sys.argv

        run_scheduler = getattr(settings, 'RUN_SCHEDULER_IN_DEBUG', False)

        if not (is_migration or is_test or is_collectstatic or is_check) and (not settings.DEBUG or run_scheduler):
            try:
                # Import and start scheduler in a separate thread to avoid blocking
                import threading
                from appointments.scheduler import start_scheduler_delayed

                # Start scheduler after a short delay to ensure DB is ready
                timer = threading.Timer(2.0, start_scheduler_delayed)
                timer.daemon = True
                timer.start()
            except Exception as e:
                print(f"Error starting appointment scheduler: {e}")
