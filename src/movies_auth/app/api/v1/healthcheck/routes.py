from flasgger import swag_from

from movies_auth.app.api.v1.healthcheck import bp


@bp.route("/ping", methods=["GET"])
@swag_from("docs/ping.yml")
def ping():
    return "pong"
