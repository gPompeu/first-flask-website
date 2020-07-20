from flask import(
    Blueprint,
    flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from SGCC.autorizacao import login_requerido
from SGCC.db import get_db

bp = Blueprint('cadastro_proprietario', __name__)

@bp.route('/')
def index():
    db = get_db()
    proprietarios = db.execute(
        'SELECT p.cod_proprietario,'
        ' p.nome,'
        ' p.RG,'
        ' p.CPF_CNPJ,'
        ' p.razao_social,'
        ' p.estado_de_moradia,'
        ' p.cidade_de_moradia,'
        ' p.endereco_de_moradia,'
        ' p.numero_de_moradia,'
        ' p.complemento_endereco,'
        ' p.telefone,'
        ' p.celular,'
        ' p.email,'
        ' p.liberar_acesso,'
        ' p.id_autor,'
        ' p.data_cadastro,'
        ' u.nome_usuario'
        ' FROM proprietario p'
        ' JOIN usuario u ON p.id_autor = u.id'
        ' ORDER BY p.data_cadastro DESC'
    ).fetchall()
    return render_template('cadastro_proprietario/index.html', proprietarios=proprietarios)

@bp.route('/cadastrar', methods=('GET', 'POST'))
@login_requerido
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        RG = request.form['RG']
        CPF_CNPJ = request.form['CPF_CNPJ']
        razao_social = request.form['razao_social']
        estado = request.form['estado']
        cidade = request.form['cidade']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        telefone = request.form['telefone']
        celular = request.form['celular']
        email = request.form['email']
        liberar_acesso = request.form.getlist('liberar_acesso') != []
        
        db = get_db()
        db.execute(
            'INSERT INTO proprietario('
                'nome,'
                'RG,'
                'CPF_CNPJ,'
                'razao_social,'
                'estado_de_moradia,'
                'cidade_de_moradia,'
                'endereco_de_moradia,'
                'numero_de_moradia,'
                'complemento_endereco,'
                'telefone,'
                'celular,'
                'email,'
                'liberar_acesso,'
                'id_autor)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (nome, RG, CPF_CNPJ, razao_social, estado, cidade, endereco,
             numero, complemento, telefone, celular, email, liberar_acesso, g.usuario['id'])
        )
        db.commit()
        return redirect(url_for('cadastro_proprietario.index'))

    return render_template('cadastro_proprietario/cadastrar.html')

def get_proprietario(id, verifica_autor=True):
    proprietario = get_db().execute(
        'SELECT p.cod_proprietario,'
        ' p.nome,'
        ' p.RG,'
        ' p.CPF_CNPJ,'
        ' p.razao_social,'
        ' p.estado_de_moradia,'
        ' p.cidade_de_moradia,'
        ' p.endereco_de_moradia,'
        ' p.numero_de_moradia,'
        ' p.complemento_endereco,'
        ' p.telefone,'
        ' p.celular,'
        ' p.email,'
        ' p.liberar_acesso,'
        ' p.id_autor,'
        ' p.data_cadastro,'
        ' u.nome_usuario'        
        ' FROM proprietario p'
        ' JOIN usuario u ON p.id_autor = u.id'
        ' WHERE p.cod_proprietario = ?',
        (id,)
    ).fetchone()

    if proprietario is None:
        abort(404, "Proprietário de código {0} não existe.".format(id))

    if verifica_autor and proprietario['id_autor'] != g.usuario['id']:
        abort(403)

    return proprietario

@bp.route('/<int:id>/atualizar', methods=('GET', 'POST'))
@login_requerido
def atualizar(id):
    proprietario = get_proprietario(id)

    if request.method == 'POST':
        nome = request.form['nome']
        RG = request.form['RG']
        CPF_CNPJ = request.form['CPF_CNPJ']
        razao_social = request.form['razao_social']
        estado = request.form['estado']
        cidade = request.form['cidade']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        telefone = request.form['telefone']
        celular = request.form['celular']
        email = request.form['email']
        liberar_acesso = request.form.getlist('liberar_acesso') != []

        db = get_db()
        db.execute(
            'UPDATE proprietario'
            ' SET nome=?,'
                'RG=?,'
                'CPF_CNPJ=?,'
                'razao_social=?,'
                'estado_de_moradia=?,'
                'cidade_de_moradia=?,'
                'endereco_de_moradia=?,'
                'numero_de_moradia=?,'
                'complemento_endereco=?,'
                'telefone=?,'
                'celular=?,'
                'email=?,'
                'liberar_acesso=?'
            ' WHERE cod_proprietario = ?',
            (nome, RG, CPF_CNPJ, razao_social, estado, cidade, endereco,
             numero, complemento, telefone, celular, email, liberar_acesso, proprietario['cod_proprietario'])
        )
        db.commit()
        return redirect(url_for('cadastro_proprietario.index'))

    return render_template('cadastro_proprietario/atualizar.html', proprietario=proprietario)

@bp.route('/<int:id>/deletar', methods=('POST',))
@login_requerido
def deletar(id):
    get_proprietario(id)
    db = get_db()
    db.execute('DELETE FROM proprietario WHERE cod_proprietario = ?', (id,))
    db.commit()
    return redirect(url_for('cadastro_proprietario.index'))