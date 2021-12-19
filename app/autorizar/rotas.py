from flask import(
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging
)

from passlib.hash import sha256_crypt

from . import autorizar as bp

from ..decoradores import (
    usuario_conectado,
    usuario_nao_conectado,
    admin_conectado,
    admin_nao_conectado
)

from .. import mysql

from ..formularios import LoginForm, RegisterForm

##############################################################
##############################################################
# AUTORIZAÇÃO
##############################################################
##############################################################

"""

DOCUMENTAÇÃO DAS ROTAS

entrar()
sair()
inscrever()

"""



@bp.route('/inscrever', methods=['GET', 'POST'])
@usuario_nao_conectado
def inscrever():

    form = RegisterForm(request.form)
    
    if request.method == 'POST' and form.validate():
        
        nome = form.nome.data
        
        email = form.email.data
        
        nome_usuario = form.nome_usuario.data
        
        senha = sha256_crypt.encrypt(str(form.senha.data))
        
        telefone = form.telefone.data

        # Create Cursor
        db = mysql.connection.cursor()
        
        db.execute("INSERT INTO usuarios(nome, email, nome_usuario, senha, telefone) VALUES(%s, %s, %s, %s, %s)",
                    (nome, email, nome_usuario, senha, telefone))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        db.close()

        flash('Agora você está cadastrado e pode entrar na sua conta. 🙂', 'success')

        return redirect(url_for('autorizar.entrar'))
        
    return render_template('autorizar/inscrever.html', form=form)



# User Login
@bp.route('/entrar', methods=['GET', 'POST'])
@usuario_nao_conectado
def entrar():

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():

        # GEt user form
        nome_usuario = form.nome_usuario.data

        # password_candidate = request.form['password']
        senha_digitada = form.senha.data

        # Create cursor
        db = mysql.connection.cursor()

        # Get user by nome_usuario
        result = db.execute("SELECT * FROM usuarios WHERE nome_usuario=%s", [nome_usuario])

        if result > 0:

            # Get stored value
            data = db.fetchone()
            
            senha = data['senha']
            
            usuario_id = data['id']
            
            nome_usuario = data['nome_usuario']

            # Compare password
            if sha256_crypt.verify(senha_digitada, senha):

                # passed
                session['usuario_conectado'] = True
                
                session['usuario_id'] = usuario_id
                
                session['nome_usuario'] = nome_usuario
                
                x = '1'
                
                db.execute("UPDATE usuarios SET online=%s WHERE id=%s", (x, usuario_id))

                flash('Você acessou sua conta! Boas compras!', 'success')
                return redirect(url_for('inicio.inicio'))

            else:
                flash('Nome de usuário ou senha incorretos.', 'danger')
                return render_template('autorizar/entrar.html', form=form)
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')

            # Fecha a conexão
            db.close()

            return render_template('autorizar/entrar.html', form=form)

    return render_template('autorizar/entrar.html', form=form)


@bp.route('/sair')
def sair():

    if 'usuario_id' in session:

        # Create cursor
        db = mysql.connection.cursor()

        uid = session['usuario_id']

        x = '0'
        
        db.execute("UPDATE usuarios SET online=%s WHERE id=%s", (x, uid))
        
        session.clear()
        
        flash('Agora ocê está conectado. 🙂', 'success')
        
        return redirect(url_for('inicio.inicio'))
    
    return redirect(url_for('.entrar'))

