from gevent import monkey

monkey.patch_all()

from movies_auth.app import create_app

app = create_app()
