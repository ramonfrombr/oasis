from flask import (
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

from . import admin as bp

from .. import mysql

from ..decoradores import (
    admin_conectado,
    admin_nao_conectado
)

from ..formularios import LoginAdmin, RegistrarAdmin

from flask_uploads import UploadSet, IMAGES

fotos = UploadSet('photos', IMAGES)



@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():

    form = RegistrarAdmin(request.form)
    
    if request.method == 'POST' and form.validate():

        nome = form.nome.data

        sobrenome = form.sobrenome.data

        email = form.email.data

        telefone = form.telefone.data

        endereco = form.endereco.data

        senha = form.senha.data

        tipo = 'gerente'

        codigo_confirmacao = 0

        senha_hash = sha256_crypt.hash(senha)
        
        # Conexão com banco de dados
        db = mysql.connection.cursor()

        # Selecione usuário a partir do email
        resultado = db.execute("INSERT INTO admin (nome, sobrenome, email, telefone, endereco, senha, tipo, codigo_confirmacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [nome, sobrenome, email, telefone, endereco, senha_hash, tipo, codigo_confirmacao])

        mysql.connection.commit()

        db.close()

        return redirect(url_for('admin.entrar'))
    else:
        return render_template('admin/registrar.html', form=form)


@bp.route('/entrar', methods=['GET', 'POST'])
@admin_nao_conectado
def entrar():

    form = LoginAdmin(request.form)

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

                return redirect(url_for('.painel'))

            else:

                flash('Senha incorreta', 'danger')

                return render_template('admin/entrar.html', form=form)

        else:

            flash('Usuario não encontrado', 'danger')
            
            # Close connection
            db.close()
            
            return render_template('admin/entrar.html', form=form)
    
    return render_template('admin/entrar.html', form=form)


@bp.route('/sair')
def sair():

    if 'admin_conectado' in session:
        
        session.clear()
        
        return redirect(url_for('admin_entrar'))
    
    return redirect(url_for('admin.admin'))


@bp.route('/painel')
@admin_conectado
def painel():

    # Conexão com banco de dados
    db = mysql.connection.cursor()
    
    n_produtos = db.execute("SELECT * FROM produtos")
    
    produtos = db.fetchall()
    
    n_pedidos = db.execute("SELECT * FROM pedidos")
    
    n_usuarios = db.execute("SELECT * FROM usuarios")
    
    return render_template(
        'admin/painel.html',
        produtos=produtos,
        n_produtos=n_produtos,
        n_pedidos=n_pedidos,
        n_usuarios=n_usuarios
    )


@bp.route('/pedidos')
@admin_conectado
def pedidos():

    # Conexão com banco de dados
    db = mysql.connection.cursor()
    
    n_produtos = db.execute("SELECT * FROM produtos")
    
    n_pedidos = db.execute("SELECT * FROM pedidos")
    
    pedidos = db.fetchall()
    
    n_usuarios = db.execute("SELECT * FROM usuarios")
    
    return render_template(
        'admin/pedidos.html',
        pedidos=pedidos,
        n_pedidos=n_pedidos,
        n_produtos=n_produtos,
        n_usuarios=n_usuarios
    )


@bp.route('/usuarios')
@admin_conectado
def usuarios():
    
    # Conexão com banco de dados
    db = mysql.connection.cursor()
    
    n_produtos = db.execute("SELECT * FROM produtos")
    
    n_pedidos = db.execute("SELECT * FROM pedidos")
    
    n_usuarios = db.execute("SELECT * FROM usuarios")
    
    usuarios = db.fetchall()
    
    return render_template(
        'admin/usuarios.html',
        usuarios=usuarios,
        n_usuarios=n_usuarios,
        n_pedidos=n_pedidos,
        n_produtos=n_produtos
    )


@bp.route('/adicionar_produto', methods=['POST', 'GET'])
@admin_conectado
def adicionar_produto():

    if request.method == 'POST':
        
        nome = request.form.get('nome')
        preco = request.form['preco']
        descricao = request.form['descricao']
        disponivel = request.form['disponivel']
        categoria = request.form['categoria']
        item = request.form['item']
        codigo = request.form['codigo']
        foto = request.files['foto']
        
        # Se todos os campos forem preenchidos
        if nome and preco and descricao and disponivel and categoria and item and codigo and foto:
            
            # Formata o nome do arquivo
            nome_arquivo = foto.filename
            nome_arquivo2 = nome_arquivo.replace("'", "")
            nome_arquivo3 = nome_arquivo2.replace(" ", "_")
            
            # Se a extensão do arquivo for permitida
            if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                # Tenta salvar a foto em app/static/image/produto
                salvar_foto = fotos.save(foto, folder=categoria)
                
                if salvar_foto:
                    
                    # Conexão com banco de dados
                    db = mysql.connection.cursor()
                    
                    db.execute("INSERT INTO produtos(produto_nome,preco,descricao, disponivel,categoria,item,produto_codigo,foto)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (nome, preco, descricao, disponivel, categoria, item, codigo, nome_arquivo3))
                    
                    # COMMIT
                    mysql.connection.commit()
                    
                    produto_id = db.lastrowid
                    
                    db.execute("INSERT INTO produto_caracteristicas(produto_id)" "VALUES(%s)", [produto_id])
                    
                    if categoria == 'camisa':

                        level = request.form.getlist('camisa')

                        for lev in level:
                            
                            yes = 'yes'
                            
                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            db.execute(query, (yes, produto_id))
                            
                            # COMMIT
                            mysql.connection.commit()
                    
                    elif categoria == 'carteira':

                        level = request.form.getlist('carteira')
                        
                        for lev in level:

                            yes = 'yes'
                            
                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            db.execute(query, (yes, produto_id))
                            
                            # COMMIT
                            mysql.connection.commit()
                    
                    elif categoria == 'cinto':

                        level = request.form.getlist('cinto')
                        
                        for lev in level:

                            yes = 'yes'

                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            db.execute(query, (yes, produto_id))
                            
                            # COMMIT
                            mysql.connection.commit()

                    elif categoria == 'sapatos':

                        level = request.form.getlist('sapatos')
                        
                        for lev in level:

                            yes = 'yes'

                            query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(field=lev)
                            
                            db.execute(query, (yes, produto_id))
                            
                            # COMMIT
                            mysql.connection.commit()
                    else:
                        flash('Categoria de produto não encontrada.', 'danger')
                        return redirect(url_for('.adicionar_produto'))
                    
                    # Fecha Conexão
                    db.close()

                    flash('Produto adicionado. 😄', 'success')

                    return redirect(url_for('.adicionar_produto'))

                else:
                    flash('Aconteceu um problema e a foto não foi salva. Tente novamente.', 'danger')
                    return redirect(url_for('.adicionar_produto'))
            else:
                flash('Extensão de arquivo não permitida. Carregue imagens com extensão .png, .jpg, ou .jpeg.', 'danger')
                return redirect(url_for('.adicionar_produto'))
        else:
            flash('Por favor, complete todo o formulário. 🧐', 'danger')
            return redirect(url_for('.adicionar_produto'))
    else:
        return render_template('admin/adicionar_produto.html')


@bp.route('/editar_produto', methods=['POST', 'GET'])
@admin_conectado
def editar_produto():

    if 'id' in request.args:
        
        produto_id = request.args['id']
        
        # Conexão com banco de dados
        db = mysql.connection.cursor()
        
        res = db.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
        
        produto = db.fetchall()
        
        db.execute("SELECT * FROM produto_caracteristicas WHERE produto_id=%s", (produto_id,))
        
        produto_caracteristicas = db.fetchall()
        
        if res:
            
            if request.method == 'POST':


                nome = request.form.get('nome')
                preco = request.form['preco']
                descricao = request.form['descricao']
                disponivel = request.form['disponivel']
                categoria = request.form['categoria']
                item = request.form['item']
                codigo = request.form['codigo']
                foto = request.files['foto']
                
                # Create Cursor
                if nome and preco and descricao and disponivel and categoria and item and codigo and foto:
                    

                    # Formata o nome do arquivo
                    nome_arquivo = foto.filename
                    nome_arquivo2 = nome_arquivo.replace("'", "")
                    nome_arquivo3 = nome_arquivo2.replace(" ", "_")
                    
                    # Se a extensão do arquivo for permitida
                    if nome_arquivo3.lower().endswith(('.png', '.jpg', '.jpeg')):

                        foto.filename = nome_arquivo3
                        
                        salvar_foto = fotos.save(foto, folder=categoria)
                        
                        if salvar_foto:

                            # Create Cursor
                            #cur = mysql.connection.cursor()

                            exe = db.execute(
                                "UPDATE produtos SET produto_nome=%s, preco=%s, descricao=%s, disponivel=%s, categoria=%s, item=%s, produto_codigo=%s, foto=%s WHERE id=%s",
                                (nome, preco, descricao, disponivel, categoria, item, codigo, nome_arquivo3, produto_id))
                            
                            if exe:

                                if categoria == 'camisa':

                                    level = request.form.getlist('camisa')
                                    
                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)
                                        
                                        db.execute(query, (yes, produto_id))
                                        
                                        # COMMIT
                                        mysql.connection.commit()
                                
                                elif categoria == 'carteira':

                                    level = request.form.getlist('carteira')
                                    
                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)

                                        db.execute(query, (yes, produto_id))

                                        # COMMIT
                                        mysql.connection.commit()

                                elif categoria == 'cinto':

                                    level = request.form.getlist('cinto')

                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)
                                        
                                        db.execute(query, (yes, produto_id))

                                        # COMMIT
                                        mysql.connection.commit()

                                elif categoria == 'sapatos':

                                    level = request.form.getlist('sapatos')
                                    
                                    for lev in level:

                                        yes = 'yes'

                                        query = 'UPDATE produto_caracteristicas SET {field}=%s WHERE produto_id=%s'.format(
                                            field=lev)

                                        db.execute(query, (yes, produto_id))

                                        # COMMIT
                                        mysql.connection.commit()

                                else:
                                    flash('Categoria de produito não encontrada. 🧐', 'danger')
                                    return redirect(url_for('.adicionar_produto'))

                                flash('Produto atualizado. 😄', 'success')
                                return redirect(url_for('.editar_produto'))
                            else:
                                flash('Dados atualizados. 😄', 'success')
                                return redirect(url_for('.editar_produto'))
                        else:
                            flash('Aconteceu um problema e a foto não foi salva. Tente novamente.', 'danger')
                            return render_template(
                                'admin/editar_produto.html',
                                produto=produto,
                                produto_caracteristicas=produto_caracteristicas
                            )
                    else:
                        flash('Extensão de arquivo não permitida. Carregue imagens com extensão .png, .jpg, ou .jpeg.', 'danger')
                        return render_template(
                            'admin/editar_produto.html',
                            produto=produto,
                            produto_caracteristicas=produto_caracteristicas
                        )

                else:
                    flash('Por favor, complete todo o formulário. 🧐', 'danger')
                    return render_template(
                        'admin/editar_produto.html',
                        produto=produto,
                        produto_caracteristicas=produto_caracteristicas
                    )
            else:
                return render_template(
                    'admin/editar_produto.html',
                    produto=produto,
                    produto_caracteristicas=produto_caracteristicas
                )
        else:
            return redirect(url_for('.entrar'))
    else:
        return redirect(url_for('.entrar'))


@bp.route('/desenvolvedor', methods=['POST', 'GET'])
def desenvolvedor():

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

