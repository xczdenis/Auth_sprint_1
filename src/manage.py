import os

from app import cli, create_app, db

app = create_app()
cli.register(app, db)

if __name__ == "__main__":
    app.run(host=os.getenv("APP_HOST", ""), port=os.getenv("APP_PORT", ""))
