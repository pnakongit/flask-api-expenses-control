from flask import Flask, Response, jsonify
from werkzeug.exceptions import NotFound


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///project.db")

    # create database
    from app.db import db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # register blue prints
    from app.swagger_bp import swaggerui_blueprint
    from app.swagger_bp import SWAGGER_API_URL
    app.register_blueprint(swaggerui_blueprint)

    from app.expense import bp as expense_bp
    app.register_blueprint(expense_bp)

    # common views
    from app.swagger_utils import build_swagger

    @app.route(SWAGGER_API_URL)
    def spec() -> Response:
        return jsonify(build_swagger(app))

    @app.route("/", methods=["GET", ])
    def index() -> (Response, int):
        """
        Send a simple message, like a greeting.
        ---
        tags:
          - "echo endpoint"
        responses:
          200:
            description: OK
            schema:
             type: object
             example:
               { "message" : "Hello World!" }


        """
        return jsonify({"message": "Hello World!"}), 200

    # error handlers
    @app.errorhandler(404)
    def resource_not_found(e: NotFound) -> (Response, int):
        return jsonify(error=str(e)), 404

    return app
