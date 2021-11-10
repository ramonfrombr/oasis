from . import mysql

def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return 

def conteudo_filtrado(produto_id):
    

    db = mysql.connection.cursor()
    

    db.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))  # getting id row
    

    dados = db.fetchone()  # get row info
    

    dados_categoria = dados['categoria']  # get id categoria ex shirt
    

    print('Exibindo resultados para PRODUTO_ID: ' + produto_id)
    

    n_produtos_da_categoria = db.execute("SELECT * FROM produtos WHERE categoria=%s", (dados_categoria,))  # get all shirt categoria
    

    print('Total de produtos encontrados: ' + str(n_produtos_da_categoria))
    

    lista_produtos_da_categoria = db.fetchall()  # get all row
    

    db.execute("SELECT * FROM produto_caracteristicas WHERE produto_id=%s", (produto_id,))  # id level info
    

    id_level = db.fetchone()
    

    lista_ids_recomendados = []
    

    lista_caracteristicas = [
        'v_shape',
        'polo',
        'clean_text',
        'design',
        'leather',
        'color',
        'formal',
        'converse',
        'loafer',
        'hook',
        'chain'
    ]
    


    # Para cada produto
    for produto in lista_produtos_da_categoria:
        
        # Seleciona as caracteristicas do produto
        db.execute("SELECT * FROM produto_caracteristicas WHERE produto_id=%s", (produto['id'],))
        
        # Seleciona o primeiro resultado
        f_level = db.fetchone()
        
        # Define o nível de combinação como sendo 0
        nivel_combinacao = 0
        
        # Se o produto da lista 
        if f_level['produto_id'] != int(produto_id):

            # Para cada característica na lista de características
            for caracteristica in lista_caracteristicas:

                # Se forem iguais
                if f_level[caracteristica] == id_level[caracteristica]:

                    # Os produtos possuem a característica em comum
                    nivel_combinacao += 1

            # Se todas as caracteristicas forem iguais (11 no total)
            if nivel_combinacao == 11:
                lista_ids_recomendados.append(f_level['produto_id'])
    


    print('Total de recomendações encontradas: ' + str(lista_ids_recomendados))
    
    
    # Se houver recomendações
    if lista_ids_recomendados:
        
        db = mysql.connection.cursor()
        
        # Transforma o vetor em uma string para a consulta SQL
        placeholders = ','.join((str(n) for n in lista_ids_recomendados))
        
        consulta_produtos_recomendados = 'SELECT * FROM produtos WHERE id IN (%s)' % placeholders
        
        db.execute(consulta_produtos_recomendados)
        
        lista_recomendados = db.fetchall()
        
        return lista_recomendados, lista_ids_recomendados, n_produtos_da_categoria, produto_id
    
    # Se não houver recomendações
    else:
        return ''

