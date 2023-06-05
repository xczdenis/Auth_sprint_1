import click


def register(app, db):
    @app.cli.command()
    @click.argument("login")
    @click.argument("password")
    def createsuperuser(login, password):
        """Create superuser."""
        from movies_auth.app.models import User

        user = User.query.filter_by(login=login).first()
        if not user:
            new_user = User()
            new_user.login = login
            new_user.is_superuser = True
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            print("User '{login}' successfully created.".format(login=login))
        else:
            print("User with login '{login}' already exists.".format(login=login))
