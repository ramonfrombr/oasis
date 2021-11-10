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

import datetime

import timeit

from . import secao as bp

from .. import mysql



from ..formularios import OrderForm

from ..funcoes_auxiliares import conteudo_filtrado, wrappers

from ..decoradores import (
    usuario_conectado,
    usuario_nao_conectado,
    admin_conectado,
    admin_nao_conectado
)


##############################################################
##############################################################
# SEÇÕES PRODUTOS
##############################################################
##############################################################


@bp.route('/camisa', methods=['GET', 'POST'])
def camisa():
    
    form = OrderForm(request.form)
    
    # Create cursor
    db = mysql.connection.cursor()
    
    # Get message
    valores = 'camisa'
    
    db.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY id ASC", (valores,))
    
    produtos = db.fetchall()
    
    # Close Connection
    db.close()
    
    if request.method == 'POST' and form.validate():

        nome = form.nome.data
        
        telefone = form.telefone.data
        
        pedido_local = form.pedido_local.data
        
        quantidade = form.quantidade.data
        
        produto_id = request.args['pedido']
        
        agora = datetime.datetime.now()
        
        semana = datetime.timedelta(days=7)
        
        data_entrega = agora + semana
        
        agora_horario = data_entrega.strftime("%y-%m-%d %H:%M:%S")
        
        # Create Cursor
        db = mysql.connection.cursor()
        
        
        if 'usuario_id' in session:

            usuario_id = session['usuario_id']
            
            db.execute("INSERT INTO pedidos(usuario_id, produto_id, ofname, telefone, pedido_local, quantidade, entrega_data) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (usuario_id, produto_id, nome, telefone, pedido_local, quantidade, agora_horario))
        else:
            db.execute("INSERT INTO pedidos(produto_id, ofname, telefone, pedido_local, quantidade, entrega_data) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (produto_id, nome, telefone, pedido_local, quantidade, agora_horario))
        
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        db.close()

        flash('Pedido feito com sucesso', 'success')
        
        return render_template('camisa.html', camisa=produtos, form=form)
    



    if 'ver' in request.args:
        
        produto_id = request.args['ver']
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = curso.fetchall()
        
        x = conteudo_filtrado(produto_id)
        
        wrappered = wrappers(conteudo_filtrado, produto_id)
        
        #execution_time = timeit.timeit(wrappered, number=0)
        
        # print('Execution time: ' + str(execution_time) + ' usec')
        if 'usuario_id' in session:
            
            usuario_id = session['usuario_id']
            
            # Create cursor
            cur = mysql.connection.cursor()
            
            cur.execute("SELECT * FROM produto_visita WHERE usuario_id=%s AND produto_id=%s", (usuario_id, produto_id))
            
            result = cur.fetchall()
            
            if result:
                
                now = datetime.datetime.now()
                
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                
                cur.execute("UPDATE produto_visita SET data=%s WHERE usuario_id=%s AND produto_id=%s",
                            (now_time, usuario_id, produto_id))
            else:
                
                cur.execute("INSERT INTO produto_visita(usuario_id, produto_id) VALUES(%s, %s)", (usuario_id, produto_id))
                
                mysql.connection.commit()
        
        return render_template('ver_produto.html', x=x, camisas=produto)
    
    elif 'pedido' in request.args:
        
        produto_id = request.args['pedido']
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = curso.fetchall()
        
        x = conteudo_filtrado(produto_id)
        
        return render_template('pedido_produto.html', x=x, camisas=produto, form=form)
    
    return render_template('camisa.html', camisa=produtos, form=form)



@bp.route('/carteira', methods=['GET', 'POST'])
def carteira():
    
    form = OrderForm(request.form)
    
    # Create cursor
    cur = mysql.connection.cursor()
    
    # Get message
    values = 'carteira'
    
    cur.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY id ASC", (values,))
    
    produtos = cur.fetchall()
    
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        
        name = form.nome.data
        
        mobile = form.telefone_num.data
        
        pedido_local = form.pedido_local.data
        
        quantity = form.quantity.data
        
        produto_id = request.args['pedido']

        now = datetime.datetime.now()
        
        week = datetime.timedelta(days=7)
        
        delivery_date = now + week
        
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        
        # Create Cursor
        curs = mysql.connection.cursor()
        
        if 'usuario_id' in session:
            
            usuario_id = session['usuario_id']
            
            curs.execute("INSERT INTO pedidos(usuario_id, produto_id, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (usuario_id, produto_id, name, mobile, pedido_local, quantity, now_time))
        else:
            curs.execute("INSERT INTO pedidos(produto_id, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (produto_id, name, mobile, pedido_local, quantity, now_time))
       
        # Commit cursor
        mysql.connection.commit()
        
        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        
        return render_template('carteira.html', carteira=produtos, form=form)
    
    if 'ver' in request.args:
       
        q = request.args['ver']
        
        produto_id = q
        
        x = conteudo_filtrado(produto_id)
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (q,))
        
        produtos = curso.fetchall()
        
        return render_template('ver_produto.html', x=x, camisas=produtos)
    
    elif 'pedido' in request.args:
        
        produto_id = request.args['pedido']
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = curso.fetchall()
        
        x = conteudo_filtrado(produto_id)
        
        return render_template('order_produto.html', x=x, camisas=produto, form=form)
    
    return render_template('carteira.html', carteira=produtos, form=form)


@bp.route('/cinto', methods=['GET', 'POST'])
def cinto():
    form = OrderForm(request.form)
    
    # Create cursor
    cur = mysql.connection.cursor()
    
    # Get message
    values = 'cinto'
    
    cur.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY id ASC", (values,))
    
    produtos = cur.fetchall()
    
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        
        name = form.nome.data
        
        mobile = form.telefone_num.data
        
        pedido_local = form.pedido_local.data
        
        quantity = form.quantity.data
        
        produto_id = request.args['pedido']
        
        now = datetime.datetime.now()
        
        week = datetime.timedelta(days=7)
        
        delivery_date = now + week
        
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        
        # Create Cursor
        curs = mysql.connection.cursor()
        
        if 'usuario_id' in session:
            
            usuario_id = session['usuario_id']
            
            curs.execute("INSERT INTO pedidos(usuario_id, produto_id, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (usuario_id, produto_id, name, mobile, pedido_local, quantity, now_time))
        else:

            curs.execute("INSERT INTO pedidos(produto_id, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (produto_id, name, mobile, pedido_local, quantity, now_time))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        
        return render_template('cintos.html', cinto=produtos, form=form)
    
    if 'ver' in request.args:
        
        q = request.args['ver']
        
        produto_id = q
        
        x = conteudo_filtrado(produto_id)
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (q,))
        
        produtos = curso.fetchall()
        
        return render_template('ver_produto.html', x=x, camisas=produtos)
    
    elif 'pedido' in request.args:
        
        produto_id = request.args['pedido']
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = curso.fetchall()
        
        x = conteudo_filtrado(produto_id)
        
        return render_template('order_produto.html', x=x, camisas=produto, form=form)
    
    return render_template('cinto.html', cinto=produtos, form=form)


@bp.route('/sapatos', methods=['GET', 'POST'])
def sapatos():

    form = OrderForm(request.form)
    
    # Create cursor
    cur = mysql.connection.cursor()
    
    # Get message
    values = 'sapatos'
    
    cur.execute("SELECT * FROM produtos WHERE categoria=%s ORDER BY id ASC", (values,))
    
    produtos = cur.fetchall()
    
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        
        nome = form.nome.data
        
        telefone = form.telefone.data
        
        pedido_local = form.pedido_local.data
        
        quantidade = form.quantidade.data
        
        produto_id = request.args['pedido']
        
        now = datetime.datetime.now()
        
        week = datetime.timedelta(days=7)
        
        delivery_date = now + week
        
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        
        # Create Cursor
        curs = mysql.connection.cursor()
        
        if 'usuario_id' in session:
            
            usuario_id = session['usuario_id']
            
            curs.execute("INSERT INTO pedidos(usuario_id, produto_id, ofname, telefone, pedido_local, quantidade, entrega_data) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (usuario_id, produto_id, nome, telefone, pedido_local, quantidade, now_time))
        
        else:
            curs.execute("INSERT INTO pedidos(produto_id, ofname, telefone, pedido_local, quantidade, entrega_data) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (produto_id, nome, telefone, pedido_local, quantidade, now_time))
        
        # Commit cursor
        mysql.connection.commit()
        
        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        
        return render_template('sapatos.html', sapatos=produtos, form=form)
    
    if 'ver' in request.args:
        
        q = request.args['ver']
        
        produto_id = q
        
        x = conteudo_filtrado(produto_id)
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (q,))
        
        produtos = curso.fetchall()

        form.produto_id = produto_id
        
        return render_template('ver_produto.html', x=x, camisas=produtos)
    
    elif 'pedido' in request.args:
        
        produto_id = request.args['pedido']
        
        curso = mysql.connection.cursor()
        
        curso.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = curso.fetchall()
        
        x = conteudo_filtrado(produto_id)

        form.produto_id = produto_id
        
        return render_template('order_produto.html', x=x, camisas=produto, form=form)
    
    

    return render_template('sapatos.html', sapatos=produtos, form=form)

