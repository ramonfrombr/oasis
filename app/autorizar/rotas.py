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

from ..formularios import LoginForm, OrderForm, UpdateRegisterForm, RegisterForm

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
        cur = mysql.connection.cursor()

        # Get user by nome_usuario
        result = cur.execute("SELECT * FROM usuarios WHERE nome_usuario=%s", [nome_usuario])

        if result > 0:

            # Get stored value
            data = cur.fetchone()
            
            senha = data['senha']
            
            usuario_id = data['id']
            
            nome = data['nome']

            # Compare password
            if sha256_crypt.verify(senha_digitada, senha):

                # passed
                session['usuario_conectado'] = True
                
                session['usuario_id'] = usuario_id
                
                session['s_name'] = nome
                
                x = '1'
                
                cur.execute("UPDATE usuarios SET online=%s WHERE id=%s", (x, usuario_id))

                flash('Você acessou sua conta! Boas compras!', 'success')
                return redirect(url_for('inicio.inicio'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('entrar.html', form=form)


        else:
            flash('Username not found', 'danger')

            # Close connection
            cur.close()

            return render_template('entrar.html', form=form)

    return render_template('entrar.html', form=form)


@bp.route('/sair')
def sair():

    if 'usuario_id' in session:

        # Create cursor
        cur = mysql.connection.cursor()

        uid = session['usuario_id']

        x = '0'
        
        cur.execute("UPDATE usuarios SET online=%s WHERE id=%s", (x, uid))
        
        session.clear()
        
        flash('You are logged out', 'success')
        
        return redirect(url_for('inicio.inicio'))
    
    return redirect(url_for('entrar'))


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
        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO usuarios(nome, email, nome_usuario, senha, telefone) VALUES(%s, %s, %s, %s, %s)",
                    (nome, email, nome_usuario, senha, telefone))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now inscrevered and can entrar', 'success')

        return redirect(url_for('inicio.inicio'))
    
    return render_template('inscrever.html', form=form)

