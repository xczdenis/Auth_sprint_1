from movies_auth.app import cli, create_app, db, error_handlers
from movies_auth.app.settings import app_settings

app = create_app()
cli.register(app, db)
error_handlers.register(app)


if __name__ == "__main__":
    app.run(
        host=app_settings.APP_HOST,
        port=app_settings.APP_PORT,
        debug=app_settings.DEBUG,
        use_reloader=app_settings.RELOAD,
    )
