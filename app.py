import os
from flask import Flask, request, jsonify, redirect, session, render_template, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from PIL import Image as PILImage
from io import BytesIO
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from reportlab.lib.colors import white
from werkzeug.security import generate_password_hash
from flask import Flask, jsonify, request
import db
from flask import Flask, render_template
from flask_cors import CORS
from datetime import timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, send_file
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
import os
from flask_cors import CORS
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import timedelta


app = Flask(__name__, static_url_path='/static')
CORS(app)
CORS(app, supports_credentials=True)
app.secret_key = 'guilherme21'

# Configurações do Banco de Dados
DATABASE = 'luminarbrasil'
USER = 'postgres'
PASSWORD = '217881'
HOST = 'localhost'
PORT = '5432'


app.config['SECRET_KEY'] = os.urandom(32)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'guilherme21'
app.permanent_session_lifetime = timedelta(minutes=190)  # Sessão expira após 30 minutos de inatividade

# Configuração do banco de dados
# Configuração do banco de dados
DATABASE_URL = "postgres://postgres:217881@localhost/luminarbrasil?client_encoding=utf8"



# Conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
@app.route('/editar_orcamento/<int:id>', methods=['GET'])
def editar_orcamento(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM orcamentos WHERE id = %s', (id,))
    orcamento = cur.fetchone()
    cur.close()
    conn.close()
    # Exclua 'idorcamento' e 'idusuario' dos dados que serão editados
    del orcamento['numeroorcamento']
    del orcamento['idusuario']
    return render_template('editar_orcamento.html', orcamento=orcamento)
@app.route('/editar_orcamento/<int:id>', methods=['POST'])
def atualizar_orcamento(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    dados_atualizados = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Certifique-se de que todos os nomes de campos correspondam aos do formulário e da tabela do banco de dados
    cur.execute('''
        UPDATE orcamentos SET
        numeroorcamento = %s, 
        quantidadeprodutos = %s,
        idproduto = %s,
        quantidade = %s,
        valorunitario = %s,
        precototal = %s,
        dataorcamento = %s,
        nomeempresa = %s,
        cnpj = %s,
        telefone = %s,
        email = %s,
        endereco = %s,
        informacoesadicionais = %s,
        dadoscliente = %s,
        tipofrete = %s,
        formapagamento = %s,
        quantidadeparcelas = %s,
        nomevendedor = %s,
        prazoentrega = %s
        WHERE id = %s
    ''', (
        dados_atualizados['numeroorcamento'],
        dados_atualizados['quantidadeprodutos'],
        dados_atualizados['idproduto'],
        dados_atualizados['quantidade'],
        dados_atualizados['valorunitario'],
        dados_atualizados['precototal'],
        dados_atualizados['dataorcamento'],
        dados_atualizados['nomeempresa'],
        dados_atualizados['cnpj'],
        dados_atualizados['telefone'],
        dados_atualizados['email'],
        dados_atualizados['endereco'],
        dados_atualizados['informacoesadicionais'],
        dados_atualizados['dadoscliente'],
        dados_atualizados['tipofrete'],
        dados_atualizados['formapagamento'],
        dados_atualizados['quantidadeparcelas'],
        dados_atualizados['nomevendedor'],
        dados_atualizados['prazoentrega'],
        id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/orcamentos')
def orcamentos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('orcamentos.html')

@app.route('/get_orcamentos', methods=['GET'])
def get_orcamentos():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orcamentos WHERE idusuario = %s', (user_id,))
    orcamentos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(orcamentos)


    
    
    
    novos_dados = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    
    
@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/produtos', methods=['GET'])
def get_produtos():
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    cursor.close()
    db.put_connection(connection)
    return jsonify(produtos)

@app.route('/produtos', methods=['POST'])
def add_produto():
    novo_produto = request.json
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO produtos (nome, imagem) VALUES (%s, %s) RETURNING *', (novo_produto['nome'], novo_produto['imagem']))
    produto = cursor.fetchone()
    connection.commit()
    cursor.close()
    db.put_connection(connection)
    return jsonify(produto)

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    produto_atualizado = request.json
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE produtos SET nome = %s, imagem = %s WHERE id = %s RETURNING *', (produto_atualizado['nome'], produto_atualizado['imagem'], id))
    produto = cursor.fetchone()
    connection.commit()
    cursor.close()
    db.put_connection(connection)
    return jsonify(produto)

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    db.put_connection(connection)
    return jsonify({'status': 'success'})

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    nome = data.get('nome')
    imagem = data.get('imagem')

    if not nome or not imagem:
        return jsonify({'error': 'Nome e imagem são obrigatórios'}), 400

    try:
        # Conexão com o banco de dados
        with psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO produtos (nome, imagem) VALUES (%s, %s) RETURNING id;", (nome, imagem))
                product_id = cursor.fetchone()[0]
                connection.commit()
        return jsonify({'status': 'success', 'id': product_id}), 201
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500
    
@app.route('/get_products', methods=['GET'])
def get_products():
    try:
        with psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nome, imagem FROM produtos;")
                products = cursor.fetchall()
        products_list = [{'id': product[0], 'nome': product[1], 'imagem': product[2]} for product in products]
        return jsonify(products_list), 200
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.json.get('email')
        senha = request.json.get('senha')
        print(f"Tentativa de login para {email} com senha {senha}")

        try:
            # Conexão com o banco de dados
            with psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as connection:
                with connection.cursor() as cursor:
                    # Busca o user_id, a senha e o nome do usuário no banco de dados
                    cursor.execute("SELECT id, senhahash, nome FROM usuarios WHERE email = %s;", [email])
                    result = cursor.fetchone()
                    if result:
                        user_id, senhahash, nome = result
                        print(f"Senha hash no banco de dados para {email}: {senhahash}")
                        # Verifica a senha
                        if check_password_hash(senhahash, senha):
                            session['user_id'] = user_id  # Configura o user_id na sessão
                            session['user_email'] = email
                            session['user_name'] = nome
                            return jsonify({'status': 'success'}), 200
                        else:
                            print("Senha incorreta")
                    else:
                        print("Email não encontrado no banco de dados")
                return jsonify({'status': 'error', 'message': 'Credenciais inválidas'}), 401
        except Exception as e:
            print(f"Erro ao tentar fazer login: {e}")
            return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

# Rota para o painel do usuário
@app.route('/painel')
def painel():
    if 'user_name' not in session:
        return redirect('/login')
    user_name = session['user_name']
    return render_template('painel.html', user_name=user_name)


def is_valid_image(file):
    try:
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return False
        with PILImage.open(file) as img:
            img.verify()
        file.seek(0)
        return True
    except Exception as e:
        print(f"Invalid image: {e}")
        return False

def adicionar_logo_e_plano_de_fundo(canvas, doc, numero_orcamento, data_orcamento):
    caminho_logo = r"D:\imagens sistema node\logo.png"
    caminho_plano_fundo = r"D:\imagens sistema node\plano.png"

    logo = Image(caminho_logo, width=120, height=120)
    logo.drawOn(canvas, 40, 0)

    plano_fundo = Image(caminho_plano_fundo, width=letter[0], height=letter[1])
    plano_fundo.drawOn(canvas, 0, 0)
    
    canvas.setFillColor(white)
    canvas.drawRightString(letter[0] - 50, letter[1] - 45, f"Orçamento: {numero_orcamento}")
    canvas.drawRightString(letter[0] - 50, letter[1] - 35, f"Data: {data_orcamento}")
    canvas.drawRightString(letter[0] - 50, letter[1] - 20, "Validade: 7 dias")

def gerar_pdf(numero_orcamento, data_orcamento, produtos, valor_total, quantidade_produtos,
              nome_empresa, cnpj, telefone, email, nome_cliente, frete, prazo_entrega,
              forma_pagamento, num_parcelas, valor_parcela, entrada):
    doc = SimpleDocTemplate(f"orcamento_{numero_orcamento}.pdf", pagesize=letter)
    
    
    

    data = [["Imagens meramente ilustrativas", "Item", "Descrição do Produto", "Quantidade", "Valor/Uni", "Valor/Total"]]
    for idx, produto in enumerate(produtos, 1):
        nome = produto["nome"]
        quantidade = produto["quantidade"]
        preco_unitario = produto["preco_unitario"]
        preco_total = produto["preco_total"]

        imagem_path = produto.get("imagem")
        if imagem_path:
            imagem = Image(imagem_path, width=40, height=40)
        else:
            imagem = "No image"

        data.append([imagem, str(idx), nome, quantidade, preco_unitario, preco_total])

    elementos = []
    
    styles = getSampleStyleSheet()
    
    # Adicionar título "Itens e Valores" com fonte de tamanho 12
    estilo_titulo = styles["Heading1"]
    estilo_titulo.fontSize = 12
    titulo = Paragraph("Itens e Valores", estilo_titulo)
    elementos.append(titulo)
    linha_divisoria = HRFlowable(width="100%", thickness=3, spaceAfter=0.5, lineCap="round", color=colors.HexColor("#1A7B79"))
    elementos.append(linha_divisoria)
    elementos.append(Spacer(1, 24))  # Espaço em branco antes do cabeçalho
   
    # Adicionar tabela com produtos
    tabela_produtos = Table(data)
    tabela_produtos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#93C5C8")),
                                          ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 0), (-1, 0), 12),
                                          ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                          ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                          ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elementos.append(tabela_produtos)
    elementos.append(Spacer(1, 24)) 
    # Adicionar informações da empresa
    estilo_titulo = styles["Heading1"]
    titulo = Paragraph("Informações da Empresa", estilo_titulo)
    elementos.append(titulo)
    linha_divisoria = HRFlowable(width="100%", thickness=3, spaceAfter=20, lineCap="round", color=colors.HexColor("#1A7B79"))
    elementos.append(linha_divisoria)
    
    estilo_normal = styles["BodyText"]
    nome_empresa_p = Paragraph(f"<b>Nome da Empresa:</b> {nome_empresa}", estilo_normal)
    cnpj_p = Paragraph(f"<b>CNPJ:</b> {cnpj}", estilo_normal)
    telefone_p = Paragraph(f"<b>Telefone:</b> {telefone}", estilo_normal)
    email_p = Paragraph(f"<b>Email:</b> {email}", estilo_normal)
    elementos.extend([nome_empresa_p, cnpj_p, telefone_p, email_p])
    elementos.append(Spacer(1, 24))
   
    # Adicionar informações do cliente
    estilo_titulo = styles["Heading1"]
    titulo = Paragraph("Informações Adicionais", estilo_titulo)
    elementos.append(titulo)
    linha_divisoria = HRFlowable(width="100%", thickness=3, spaceAfter=6, lineCap="round", color=colors.HexColor("#1A7B79"))
    elementos.append(linha_divisoria)
    
    estilo_normal = styles["BodyText"]
    
    cliente_info = f"OBS: {nome_cliente}"
    elementos.append(Paragraph(cliente_info, estilo_normal))
    elementos.append(Spacer(1, 24))  # Espaço em branco antes do cabeçalho

    # Adicionar informações de frete
    estilo_titulo = styles["Heading1"]
    titulo = Paragraph("Informações de Entrega", estilo_titulo)
    elementos.append(titulo)
    linha_divisoria = HRFlowable(width="100%", thickness=3, spaceAfter=6, lineCap="round", color=colors.HexColor("#1A7B79"))
    elementos.append(linha_divisoria)
    
    estilo_normal = styles["BodyText"]
    espaco = "<br/>"
    frete_info = f"Frete: {frete}{espaco}Prazo de entrega: {prazo_entrega}"
    elementos.append(Paragraph(frete_info, estilo_normal))
    elementos.append(Spacer(1, 24))  # Espaço em branco antes do cabeçalho

    # Adicionar informações de pagamento
    estilo_titulo = styles["Heading1"]
    titulo = Paragraph("Informações de Pagamento", estilo_titulo)
    elementos.append(titulo)
    linha_divisoria = HRFlowable(width="100%", thickness=3, spaceAfter=6, lineCap="round", color=colors.HexColor("#1A7B79"))
    elementos.append(linha_divisoria)
    
    estilo_normal = styles["BodyText"]
    espaco = "<br/>"
    pagamento_info = f"Forma de pagamento: {forma_pagamento}{espaco}Número de parcelas: {num_parcelas}{espaco}Valor da parcela: R$ {valor_parcela:.2f}{espaco}Entrada: R$ {entrada:.2f}"
    elementos.append(Paragraph(pagamento_info, estilo_normal))
    elementos.append(Spacer(1, 24))  # Espaço em branco antes do cabeçalho
    
    # Adicionar valor total
    valor_total_info = f"Valor Total: R$ {valor_total:.2f}"
    elementos.append(Paragraph(valor_total_info, estilo_normal))

    

    # Adicionar texto após o valor total
    texto_apos_valor_total = "Esta cotação/pedido considera as informações acima descritas. É de responsabilidade do cliente a confirmação das informações apresentadas e a solicitação de alteração se for o caso, isentando a Luminar Brasil  de eventuais questionamentos, multas ou acréscimos de tributos realizados pelo Estado de destino da mercadoria."
    elementos.append(Paragraph(texto_apos_valor_total, estilo_normal))
    
    estilo_normal = styles["BodyText"]
    dados_conta1 = [
        Paragraph("<b>Dados da conta:</b>", estilo_normal),
        Paragraph("Banco: 336 - Banco C6 S.A.", estilo_normal),
        Paragraph("Agência: 0001", estilo_normal),
        Paragraph("Conta corrente: 22910323-5", estilo_normal),
        Paragraph("CNPJ: 20.656.549/0001-46", estilo_normal),
        Paragraph("Nome: LUMINAR BRASIL", estilo_normal),
        Paragraph("Chave Pix: luminarfinanceiro@hotmail.com", estilo_normal)
    ]
    elementos.extend(dados_conta1)

    dados_conta2 = [
        Paragraph("Agência: 0001", estilo_normal),
        Paragraph("Conta: 1345909-6", estilo_normal),
        Paragraph("Instituição: 403 - Cora SCD", estilo_normal),
        Paragraph("Nome da Empresa: Luminar Brasil", estilo_normal),
        Paragraph("PIX CNPJ: 20.656.549/0001-46 BANCO CORA", estilo_normal)
    ]
    elementos.extend(dados_conta2)
    
    doc.build(elementos, onFirstPage=lambda canvas, doc: adicionar_logo_e_plano_de_fundo(canvas, doc, numero_orcamento, data_orcamento))
    
@app.route("/painel")
def gerar_orcamento_login():
    return render_template("painel.html")

@app.route("/home")
def gerar_orcamento():
    return render_template("home.html")

@app.route("/gerar_orcamento", methods=["POST"])
def gerar_orcamento_form():
    numero_orcamento = request.form.get("numero_orcamento")
    data_orcamento = request.form.get("data_orcamento")
    quantidade_produtos = int(request.form.get("quantidade_produtos"))

    produtos = []
    valor_total = 0

    for i in range(quantidade_produtos):
        quantidade = int(request.form.get(f"produtos[{i}][quantidade]"))
        nome = request.form.get(f"produtos[{i}][nome_produto]")
        preco = float(request.form.get(f"produtos[{i}][preco_produto]"))
        preco_total = quantidade * preco

        imagem = request.files.get(f"produtos[{i}][imagem]")
        if imagem and is_valid_image(imagem):
            imagem_content = BytesIO(imagem.read())
        else:
            imagem_content = None

        produtos.append({
            "nome": nome,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "preco_total": preco_total,
            "imagem": imagem_content
        })
        valor_total += preco_total

    nome_empresa = request.form.get("nome_empresa")
    cnpj = request.form.get("cnpj")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    nome_cliente = request.form.get("nome_cliente")
    frete = request.form.get("frete")
    prazo_entrega = request.form.get("prazo_entrega")
    forma_pagamento = request.form.get("forma_pagamento")
    num_parcelas = int(request.form.get("num_parcelas", 0))
    valor_parcela = float(request.form.get("valor_parcela", 0))
    entrada = float(request.form.get("entrada", 0))

    gerar_pdf(numero_orcamento, data_orcamento, produtos, valor_total, quantidade_produtos,
              nome_empresa, cnpj, telefone, email, nome_cliente, frete, prazo_entrega,
              forma_pagamento, num_parcelas, valor_parcela, entrada)

    return send_file(f"orcamento_{numero_orcamento}.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
