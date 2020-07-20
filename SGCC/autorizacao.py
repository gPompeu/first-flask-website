import functools

from flask import (
    Blueprint,
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from SGCC.db import get_db

bp = Blueprint('autorizacao', __name__, url_prefix='/autorizacao')

@bp.route('/registrar_se', methods=('GET', 'POST'))
def registrar_se():
    if request.method =='POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        db = get_db()
        error = None

        if not nome_usuario:
            error = 'Nome de usuário obrigatório'
        elif not senha:
            error = 'Senha obrigatória'
        elif db.execute(
            'SELECT id FROM usuario WHERE nome_usuario = ?', (nome_usuario,)
        ).fetchone() is not None:
            error = 'Usuário {} já está registrado.'.format(nome_usuario)

        if error is None:
            db.execute(
                'INSERT INTO usuario (nome_usuario, senha) VALUES (?, ?)',
                (nome_usuario, generate_password_hash(senha))
            )
            db.commit()
            return redirect(url_for('autorizacao.entrar'))

        flash(error)

    return render_template('autorizacao/registrar_se.html')

@bp.route('/entrar', methods=('GET', 'POST'))
def entrar():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        db = get_db()
        error = None
        usuario = db.execute(
            'SELECT * FROM usuario WHERE nome_usuario = ?', (nome_usuario,)
        ).fetchone()

        if usuario is None:
            error = 'Nome de usuário incorreto.'
        elif not check_password_hash(usuario['senha'], senha):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['usuario_id'] = usuario['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('autorizacao/entrar.html')

@bp.before_app_request
def carregar_usuario_logado():
    usuario_id = session.get('usuario_id')

    if usuario_id is None:
        g.usuario = None
    else:
        g.usuario = get_db().execute(
            'SELECT * FROM usuario WHERE id = ?', (usuario_id,)
        ).fetchone()

@bp.route('/sair')
def sair():
    session.clear()
    return redirect(url_for('index'))

def login_requerido(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for('autorizacao.entrar'))

        return view(**kwargs)

    return wrapped_view