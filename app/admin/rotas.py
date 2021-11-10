from flask import Flask, render_template, flash, redirect, url_for, session, request, logging

from passlib.hash import sha256_crypt

from . import admin as bp

from .. import mysql

from ..decoradores import usuario_conectado, usuario_nao_conectado, admin_conectado, admin_nao_conectado


@bp.route('/admin_entrar', methods=['GET', 'POST'])
@admin_nao_conectado
def admin_entrar():

    if request.method == 'POST':

        # Selecione o email
        email = request.form['email']

        # Selecione a senha digitada
        senha_digitada = request.form['senha']

        # Conexão com banco de dados
        db = mysql.connection.cursor()

        # Selecione usuário a partir do email
        resultado = db.execute("SELECT * FROM admin WHERE email=%s", [email])

        # Se a consulta gerar resultado
        if resultado > 0:

            # Selecione os dados do primeiro resultado
            dados = db.fetchone()
            
            senha = dados['senha']
            
            usuario_id = dados['id']
            
            nome = dados['nome']

            # Compare as senhas
            if sha256_crypt.verify(senha_digitada, senha):
                
                # passed
                session['admin_conectado'] = True
                
                session['admin_uid'] = usuario_id
                
                session['admin_nome'] = nome

                return redirect(url_for('admin'))

            else:

                flash('Senha incorreta', 'danger')

                return render_template('pages/entrar.html')

        else:

            flash('Usuario não encontrado', 'danger')
            
            # Close connection
            db.close()
            
            return render_template('pages/entrar.html')
    
    return render_template('pages/entrar.html')


@bp.route('/admin_sair')
def admin_sair():

    if 'admin_conectado' in session:
        
        session.clear()
        
        return redirect(url_for('admin_entrar'))
    
    return redirect(url_for('admin'))


@bp.route('/admin')
@admin_conectado
def admin():

    db = mysql.connection.cursor()
    
    n_produtos = db.execute("SELECT * FROM produtos")
    
    produtos = db.fetchall()
    
    n_pedidos = db.execute("SELECT * FROM pedidos")
    
    n_usuarios = db.execute("SELECT * FROM usuarios")
    
    return render_template(
        'pages/inicio.html',
        produtos=produtos,
        n_produtos=n_produtos,
        n_pedidos=n_pedidos,
        n_usuarios=n_usuarios
    )


@bp.route('/pedidos')
@admin_conectado
def pedidos():

    db = mysql.connection.cursor()
    
    n_produtos = db.execute("SELECT * FROM produtos")
    
    n_pedidos = db.execute("SELECT * FROM pedidos")
    
    pedidos = db.fetchall()
    
    n_usuarios = db.execute("SELECT * FROM usuarios")
    
    return render_template(
        'pages/todos_pedidos.html',
        pedidos=pedidos,
        n_pedidos=n_pedidos,
        n_produtos=n_produtos,
        n_usuarios=n_usuarios
    )


@bp.route('/usuarios')
@admin_conectado
def usuarios():
    
    db = mysql.connection.cursor()
    
    n_produtos = db.execute("SELECT * FROM produtos")
    
    n_pedidos = db.execute("SELECT * FROM pedidos")
    
    n_usuarios = db.execute("SELECT * FROM usuarios")
    
    usuarios = db.fetchall()
    
    return render_template(
        'pages/todos_usuarios.html',
        usuarios=usuarios,
        n_usuarios=n_usuarios,
        n_pedidos=n_pedidos,
        n_produtos=n_produtos
    )


@bp.route('/adicionar_produto', methods=['POST', 'GET'])
@admin_conectado
def adicionar_produto():

    if request.method == 'POST':
        
        name = request.form.get('name')
        
        price = request.form['price']
        
        description = request.form['description']
        
        available = request.form['available']
        
        categoria = request.form['categoria']
        
        item = request.form['item']
        
        code = request.form['code']
        
        file = request.files['picture']
        
        if name and price and description and available and categoria and item and code and file:
            
            pic = file.filename
            
            photo = pic.replace("'", "")
            
            picture = photo.replace(" ", "_")
            
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                
                save_photo = photos.save(file, folder=categoria)
                
                if save_photo:
                    
                    # Create Cursor
                    curs = mysql.connection.cursor()
                    
                    curs.execute("INSERT INTO produtos(pName,price,description,available,categoria,item,pCode,picture)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (name, price, description, available, categoria, item, code, picture))
                    
                    mysql.connection.commit()
                    
                    produto_id = curs.lastrowid
                    
                    curs.execute("INSERT INTO produto_caracteristicas(produto_id)" "VALUES(%s)", [produto_id])
                    
                    if categoria == 'camisa':

                        level = request.form.getlist('camisa')

                        for lev in level:
                            
                            yes = 'yes'
                            
                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            curs.execute(query, (yes, produto_id))
                            
                            # Commit cursor
                            mysql.connection.commit()
                    
                    elif categoria == 'carteira':

                        level = request.form.getlist('carteira')
                        
                        for lev in level:

                            yes = 'yes'
                            
                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            curs.execute(query, (yes, produto_id))
                            
                            # Commit cursor
                            mysql.connection.commit()
                    
                    elif categoria == 'cinto':

                        level = request.form.getlist('cinto')
                        
                        for lev in level:

                            yes = 'yes'

                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            curs.execute(query, (yes, produto_id))
                            
                            # Commit cursor
                            mysql.connection.commit()

                    elif categoria == 'sapatos':

                        level = request.form.getlist('sapatos')
                        
                        for lev in level:

                            yes = 'yes'

                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            curs.execute(query, (yes, produto_id))
                            
                            # Commit cursor
                            mysql.connection.commit()
                    else:

                        flash('Product level not fund', 'danger')
                        
                        return redirect(url_for('admin_adicionar_produto'))
                    
                    # Close Connection
                    curs.close()

                    flash('Product added successful', 'success')

                    return redirect(url_for('admin_adicionar_produto'))

                else:

                    flash('Picture not save', 'danger')

                    return redirect(url_for('admin_adicionar_produto'))
            
            else:

                flash('File not supported', 'danger')

                return redirect(url_for('admin_adicionar_produto'))
        
        else:

            flash('Please fill up all form', 'danger')
            
            return redirect(url_for('admin_adicionar_produto'))
    
    else:

        return render_template('pages/adicionar_produto.html')


@bp.route('/editar_produto', methods=['POST', 'GET'])
@admin_conectado
def editar_produto():

    if 'id' in request.args:
        
        produto_id = request.args['id']
        
        curso = mysql.connection.cursor()
        
        res = curso.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = curso.fetchall()
        
        curso.execute("SELECT * FROM produto_caracteristicas WHERE produto_id=%s", (produto_id,))
        
        produto_caracteristicas = curso.fetchall()
        
        if res:
            
            if request.method == 'POST':

                name = request.form.get('name')
                
                price = request.form['price']
                
                description = request.form['description']
                
                available = request.form['available']
                
                categoria = request.form['categoria']
                
                item = request.form['item']
                
                code = request.form['code']
                
                file = request.files['picture']
                
                # Create Cursor
                if name and price and description and available and categoria and item and code and file:
                    
                    pic = file.filename
                    
                    photo = pic.replace("'", "")
                    
                    picture = photo.replace(" ", "")
                    
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):

                        file.filename = picture
                        
                        save_photo = photos.save(file, folder=categoria)
                        
                        if save_photo:

                            # Create Cursor
                            cur = mysql.connection.cursor()

                            exe = curso.execute(
                                "UPDATE produtos SET pName=%s, price=%s, description=%s, available=%s, categoria=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, categoria, item, code, picture, produto_id))
                            
                            if exe:

                                if categoria == 'camisa':

                                    level = request.form.getlist('camisa')
                                    
                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)
                                        
                                        cur.execute(query, (yes, produto_id))
                                        
                                        # Commit cursor
                                        mysql.connection.commit()
                                
                                elif categoria == 'carteira':

                                    level = request.form.getlist('carteira')
                                    
                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)

                                        cur.execute(query, (yes, produto_id))

                                        # Commit cursor
                                        mysql.connection.commit()

                                elif categoria == 'cinto':

                                    level = request.form.getlist('cinto')

                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)
                                        
                                        cur.execute(query, (yes, produto_id))

                                        # Commit cursor
                                        mysql.connection.commit()

                                elif categoria == 'sapatos':

                                    level = request.form.getlist('sapatos')
                                    
                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)

                                        cur.execute(query, (yes, produto_id))

                                        # Commit cursor
                                        mysql.connection.commit()

                                else:

                                    flash('Product level not fund', 'danger')

                                    return redirect(url_for('admin_adicionar_produto'))

                                flash('Product updated', 'success')

                                return redirect(url_for('editar_produto'))

                            else:

                                flash('Data updated', 'success')

                                return redirect(url_for('editar_produto'))

                        else:

                            flash('Pic not upload', 'danger')

                            return render_template('pages/editar_produto.html', produto=produto,
                                                   produto_caracteristicas=produto_caracteristicas)
                    else:

                        flash('File not support', 'danger')

                        return render_template('pages/editar_produto.html', produto=produto,
                                               produto_caracteristicas=produto_caracteristicas)

                else:

                    flash('Fill all field', 'danger')

                    return render_template('pages/editar_produto.html', produto=produto,
                                           produto_caracteristicas=produto_caracteristicas)

            else:

                return render_template('pages/editar_produto.html', produto=produto, produto_caracteristicas=produto_caracteristicas)
        else:

            return redirect(url_for('admin_entrar'))
    else:

        return redirect(url_for('admin_entrar'))



@bp.route('/developer', methods=['POST', 'GET'])
def developer():

    form = DeveloperForm(request.form)
    
    if request.method == 'POST' and form.validate():

        q = form.id.data
        
        curso = mysql.connection.cursor()
        
        result = curso.execute("SELECT * FROM produtos WHERE id=%s", (q,))
        
        if result > 0:

            x = conteudo_filtrado(q)

            wrappered = wrappers(conteudo_filtrado, q)
            
            execution_time = timeit.timeit(wrappered, number=0)
            
            seconds = ((execution_time / 1000) % 60)

            return render_template('developer.html', form=form, x=x, execution_time=seconds)
        else:

            nothing = 'Nothing found'

            return render_template('developer.html', form=form, nothing=nothing)
    else:
        return render_template('developer.html', form=form)

