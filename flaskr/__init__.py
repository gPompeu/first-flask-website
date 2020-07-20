import os

from flask import Flask

def create_app(test_config=None):
    # Cria e configura o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Carrega o intance config, se existir, quando não testando
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega o config de teste se for passado
        app.config.from_mapping(test_config)

    # Certifica que a pasta da instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Uma simples página que diz oi
    @app.route('/hello')
    def ola():
        return 'Olá, mundo!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app