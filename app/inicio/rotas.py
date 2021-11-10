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

from . import inicio as bp

from .. import mysql

from ..decoradores import (
    usuario_conectado,
    usuario_nao_conectado,
    admin_conectado,
    admin_nao_conectado
)

from ..formularios import OrderForm, UpdateRegisterForm


  

##############################################################
##############################################################
# SEÇÕES
##############################################################
##############################################################


"""

DOCUMENTAÇÃO DAS ROTAS

inicio()
pesquisa()
perfil()
configuracoes()

"""


@bp.route('/')
def inicio():
    
    form = OrderForm(request.form)
    
    # Create cursor
    db = mysql.connection.cursor()
    
    # Get message
    
    valores = 'camisa'
    
    db.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY RAND() LIMIT 4", (valores,))
    
    camisa = db.fetchall()
    
    valores = 'carteira'
    
    db.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY RAND() LIMIT 4", (valores,))
    
    carteira = db.fetchall()
    
    valores = 'cinto'
    
    db.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY RAND() LIMIT 4", (valores,))
    
    cinto = db.fetchall()
    
    valores = 'sapatos'
    
    db.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY RAND() LIMIT 4", (valores,))
    
    sapatos = db.fetchall()
    
    # Close Connection
    
    db.close()
    
    return render_template(
        'inicio.html',
        camisa=camisa,
        carteira=carteira,
        cinto=cinto,
        sapatos=sapatos,
        form=form
    )


@bp.route('/pesquisa', methods=['POST', 'GET'])
def pesquisa():

    form = OrderForm(request.form)
    
    if 'q' in request.args:

        q = request.args['q']
        
        # Create cursor
        db = mysql.connection.cursor()
        
        # Get message
        
        query_string = "SELECT * FROM produtos WHERE produto_nome LIKE %s ORDER BY id ASC"
        
        db.execute(query_string, ('%' + q + '%',))
        
        produtos = db.fetchall()
        
        # Close Connection
        db.close()
        
        flash('Exibindo resultados para: ' + q, 'success')
        
        return render_template('pesquisa.html', produtos=produtos, form=form)
    
    else:
        
        flash('Pesquisa novamente.', 'danger')
        
        return render_template('pesquisa.html')



@bp.route('/perfil')
@usuario_conectado
def perfil():

    if 'usuario' in request.args:

        q = request.args['usuario']
        
        db = mysql.connection.cursor()
        
        db.execute("SELECT * FROM usuarios WHERE id=%s", (q,))
        
        result = db.fetchone()
        
        if result:

            if result['id'] == session['usuario_id']:
                
                db.execute("SELECT * FROM pedidos WHERE usuario_id=%s ORDER BY id ASC", (session['usuario_id'],))
                
                res = db.fetchall()
                
                return render_template('perfil.html', result=res)
            
            else:

                flash('Não autorizado!', 'danger')

                return redirect(url_for('autorizar.entrar'))

        else:

            flash('Não autorizado! Por favor, entrar.', 'danger')

            return redirect(url_for('autorizar.entrar'))

    else:

        flash('Não autorizado!', 'danger')

        return redirect(url_for('autorizar.entrar'))


@bp.route('/configuracoes', methods=['POST', 'GET'])
@usuario_conectado
def configuracoes():


    form = UpdateRegisterForm(request.form)

    if 'usuario' in request.args:

        q = request.args['usuario']
        
        db = mysql.connection.cursor()
        
        db.execute("SELECT * FROM usuarios WHERE id=%s", (q,))
        
        result = db.fetchone()
        
        if result:

            if result['id'] == session['usuario_id']:

                if request.method == 'POST' and form.validate():

                    nome = form.nome.data

                    email = form.email.data
                    
                    senha = sha256_crypt.encrypt(str(form.senha.data))
                    
                    telefone = form.telefone.data

                    # Create Cursor
                    cur = mysql.connection.cursor()
                    
                    exe = cur.execute("UPDATE usuarios SET nome=%s, email=%s, senha=%s, telefone=%s WHERE id=%s",
                                      (nome, email, senha, telefone, q))
                    
                    if exe:
                        
                        flash('Perfil atualizado.', 'success')
                        
                        return render_template('configuracoes_usuario.html', result=result, form=form)
                    
                    else:
                        flash('Perfil não atualizado!', 'danger')

                return render_template('configuracoes_usuario.html', result=result, form=form)
            
            else:

                flash('Não autorizado!', 'danger')

                return redirect(url_for('autorizar.entrar'))

        else:

            flash('Não autorizado! Por favor, entrar.', 'danger')

            return redirect(url_for('autorizar.entrar'))

    else:

        flash('Não autorizado!', 'danger')

        return redirect(url_for('autorizar.entrar'))

