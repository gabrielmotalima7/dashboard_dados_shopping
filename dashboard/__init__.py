from flask import Flask

def init_app():
    app = Flask(__name__)
    with app.app_context():
        from .analise_comparativa import init_dashboard_analise_comparativa
        from .analise_individual import init_dashboard_analise_individual
        app = init_dashboard_analise_comparativa(app)
        app = init_dashboard_analise_individual(app)
        return app