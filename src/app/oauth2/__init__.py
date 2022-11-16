from app.oauth2 import base

oauth_manager = base.OAuthManager()

yandex_oauth = base.YandexOAuthProvider()
mail_oauth = base.MailOAuthProvider()
google_oauth = base.GoogleOAuthProvider()
