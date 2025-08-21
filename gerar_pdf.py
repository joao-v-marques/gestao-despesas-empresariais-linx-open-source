import os
from datetime import datetime
from fpdf import FPDF

def gerar_pdf(solicitacao, fornecedor, cnpj, id):
    pdf = FPDF()
    pdf.add_page()

    # Adiciona imagem de fundo (o formulário escaneado)
    pdf.image("static/img/Logo - Grupo Kato Preto.png", x=10, y=10, w=50)

    pdf.set_xy(165, 20)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font("Arial", size=24, style="B") 
    pdf.cell(50, 5, id)

    pdf.set_text_color(0, 0, 0)

    # Info. Revendas ---------------------------------------------------------------------------------------------------------------------------------------
    pdf.set_font("Arial", size=10)
    pdf.set_xy(15, 40)
    pdf.cell(50, 5, "Valtra - Maringá/PR")
    pdf.set_xy(19, 45)
    pdf.cell(55, 5, "(44) 3220-5100")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(15, 55)
    pdf.cell(50, 5, "Valtra - Paranavai/PR")
    pdf.set_xy(19, 60)
    pdf.cell(55, 5, "(44) 3421-3141")

    pdf.line(55, 40, 55, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(65, 40)
    pdf.cell(50, 5, "Valtra/Fendt")
    pdf.set_xy(60, 45)
    pdf.cell(50, 5, "Campo Mourão/PR")
    pdf.set_xy(64, 50)
    pdf.cell(55, 5, "(44) 3016-7800")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(60, 56)
    pdf.cell(50, 5, "Kato - Goioerê/PR")
    pdf.set_xy(64, 61)
    pdf.cell(55, 5, "(44) 3521-8400")

    pdf.line(100, 40, 100, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(105, 40)
    pdf.cell(50, 5, "Valtra - Ubiratã/PR")
    pdf.set_xy(109, 45)
    pdf.cell(55, 5, "(44) 3543-4014")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(105, 55)
    pdf.cell(50, 5, "Valtra - Umuarama/PR")
    pdf.set_xy(109, 60)
    pdf.cell(55, 5, "(44) 3626-4300")

    pdf.line(145, 40, 145, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(150, 40)
    pdf.cell(50, 5, "Valtra/Fendt - Londrina/PR")
    pdf.set_xy(154, 45)
    pdf.cell(55, 5, "(43) 3305-0880")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(150, 55)
    pdf.cell(50, 5, "Valtra - Cornélio Procópio/PR")
    pdf.set_xy(154, 60)
    pdf.cell(55, 5, "(43) 3132-4040")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(75, 70)
    pdf.cell(50, 5, "Valtra")
    pdf.set_xy(67, 75)
    pdf.cell(50, 5, "Jardim Alegre/PR")
    pdf.set_xy(67, 80)
    pdf.cell(50, 5, "(43) 3122-0050")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(112, 70)
    pdf.cell(50, 5, "Valtra")
    pdf.set_xy(111, 75)
    pdf.cell(50, 5, "Irati/PR") 
    pdf.set_xy(105, 80)
    pdf.cell(55, 5, "(42) 3423-3400")


    # Requisição de compra ---------------------------------------------------------------------------------------------------------------------------------------    
    pdf.set_font("Arial", size=18, style='BU')
    pdf.set_xy(0, 88)  # y = posição vertical
    pdf.cell(pdf.w, 10, "REQUISIÇÃO DE COMPRA", align='C')

    # Data ---------------------------------------------------------------------------------------------------------------------------------------
    pdf.set_font("Arial", size=16, style='')
    pdf.set_xy(0, 25)
    
    pdf.cell(pdf.w, 8, datetime.now().strftime("%d/%m/%Y"), align='C')

    # Nome ------------------------------------------------------------------------------------------------------------------------
    pdf.set_xy(10, 100)
    pdf.set_font("Arial", size=14, style='B')  
    pdf.cell(50, 5, "Nome:")

    pdf.line(27, 104, 205, 104)

    # Fornecedor -----------------------------------------------------------------------------------------------------------------------------------
    pdf.set_xy(10, 113)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(30, 5, "Fornecedor:")

    pdf.line(40, 117, 140, 117)

    pdf.set_font("Arial", size=14)
    pdf.set_xy(40, 112.5)
    pdf.cell(50, 5, fornecedor['nome'])

    # CNPJ ------------------------------------------------------------------------------------------------------------------------
    pdf.set_xy(140, 113)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(50, 5, "CNPJ:")

    pdf.line(157, 117, 205, 117)

    pdf.set_font("Arial", size=14)
    pdf.set_xy(158, 112.5)
    pdf.cell(50, 5, cnpj)

    # Endereço -----------------------------------------------------------------------------------------------------------------------------------
    pdf.set_xy(10, 125)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(30, 5, "Endereço:")

    pdf.line(35, 129, 150, 129)

    # OS Nº --------------------------------------------------------------------------------------------------------------------------------------
    pdf.set_xy(150, 125)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(20, 5, "O.S Nº:")

    pdf.line(169, 129, 205, 129)

    # Dados solicitação --------------------------------------------------------------------------------------------------------------------------------------
    pdf.set_font("Arial", size=18, style='BU')
    pdf.set_xy(0, 135)  # y = posição vertical
    pdf.cell(pdf.w, 10, "INFO. SOLICITAÇÃO", align='C')

    
    col1 = 50
    col2 = 140
    row_h = 8

    campos = [
        ("Empresa/Revenda", f"{solicitacao['empresa']}.{solicitacao['revenda']}"),
        ("Usuário Solicitante", solicitacao['usuario_solicitante']),
        ("Departamento", f"{solicitacao['departamento_codigo']} - {solicitacao['departamento_descricao']}"),
        ("Origem", f"{solicitacao['origem_codigo']} - {solicitacao['origem_descricao']}"),
        ("Valor da Solicitação", f"R$ {str(solicitacao['valor']).replace('.', ',')}"),
        ("Valor do Orçamento", f"R$ {str(solicitacao['orcamento']).replace('.', ',')}"),
        ("Fornecedor", fornecedor['cliente']),
        ("CNPJ Fornecedor", cnpj)
    ]

    pdf.set_xy(10, 150)
    for campo, valor in campos:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(col1, row_h, campo, border=1)
        pdf.set_font("Arial", "", 10)
        pdf.cell(col2, row_h, str(valor), border=1, ln=True)

    pdf.ln(5)

    # --- descrição (célula expandida) ---
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, row_h, "Descrição", border=1, ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, row_h, solicitacao['descricao'], border=1)

    pdf.ln(5)

    # Local para assinatura
    pdf.set_xy(23, 270)
    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(30, 5, "Nome funcionário solicitante/Dpto")

    pdf.line(10, 270, 100, 270)

    pdf.set_xy(140, 270)
    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(30, 5, "Assinatura")

    pdf.line(110, 270, 200, 270)
    

    diretorio_atual = os.getcwd()
    base_dir = f"{diretorio_atual}/static/pdf/"
    os.makedirs(base_dir, exist_ok=True)
    pdf_path = os.path.join(base_dir, f"solicitacao_{solicitacao['id']}.pdf")
    pdf.output(pdf_path)
    return pdf_path