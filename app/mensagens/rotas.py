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

from . import mensagens as bp

from .. import mysql

from ..formularios import MessageForm





##############################################################
##############################################################
# MENSAGENS
##############################################################
##############################################################


@bp.route('/conversa/<string:id>', methods=['GET', 'POST'])
def conversa(id):

    if 'usuario_id' in session:

        form = MessageForm(request.form)
        
        # Create cursor
        db = mysql.connection.cursor()

        # lid name
        get_result = db.execute("SELECT * FROM usuarios WHERE id=%s", [id])
        
        l_data = db.fetchone()
        
    
        if get_result > 0:

            session['nome'] = l_data['nome']
            
            usuario_id = session['usuario_id']
            
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                
                txt_body = form.conteudo.data
                
                # Create cursor
                db = mysql.connection.cursor()
                
                db.execute("INSERT INTO mensagens(conteudo, autor, destinatario) VALUES(%s, %s, %s)",
                            (txt_body, id, usuario_id))
                
                # Commit cursor
                mysql.connection.commit()

            # Get usuarios
            db.execute("SELECT * FROM usuarios")

            usuarios = db.fetchall()

            # Close Connection
            db.close()
            
            return render_template('conversa.html', usuarios=usuarios, form=form)
        
        else:

            flash('Sem permissão!', 'danger')
            
            return redirect(url_for('inicio.inicio'))
    
    else:

        return redirect(url_for('autorizar.entrar'))


@bp.route('/conversas', methods=['GET', 'POST'])
def conversas():

    if 'lid' in session:
        
        id = session['lid']
        
        usuario_id = session['usuario_id']
        
        # Create cursor
        db = mysql.connection.cursor()
        
        # Get message
        db.execute("SELECT * FROM mensagens WHERE (autor=%s AND destinatario=%s) OR (autor=%s AND destinatario=%s) "
                    "ORDER BY id ASC", (id, usuario_id, usuario_id, id))
        
        conversas = db.fetchall()
        
        # Close Connection
        db.close()
        
        return render_template('conversas.html', conversas=conversas, )
    
    return redirect(url_for('autorizar.entrar'))


