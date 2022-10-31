from app import cli, create_app, db
from config import settings

app = create_app()
cli.register(app, db)

if __name__ == "__main__":
    app.run(host=settings.APP_HOST, port=settings.APP_PORT)
