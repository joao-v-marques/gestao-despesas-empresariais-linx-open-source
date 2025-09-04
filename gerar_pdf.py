import os
from datetime import datetime
from fpdf import FPDF

def gerar_pdf(solicitacao, fornecedor, cnpj, id, nome_revenda):
    pdf = FPDF()
    pdf.add_page()

    # Adiciona imagem de fundo (o formulário escaneado)
    pdf.image("static/img/Logo - Grupo Kato Preto.png", x=10, y=10, w=50)

    pdf.set_xy(150, 20)
    pdf.set_font("Arial", size=24, style="B") 
    pdf.cell(50, 5, f"Nro. {id}")

    pdf.set_text_color(0, 0, 0)

    # Info. Revendas
    pdf.set_font("Arial", size=10)
    pdf.set_xy(10, 40)
    pdf.cell(50, 5, "Valtra - Maringá/PR")
    pdf.set_xy(14, 45)
    pdf.cell(55, 5, "(44) 3220-5100")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(10, 55)
    pdf.cell(50, 5, "Valtra - Paranavai/PR")
    pdf.set_xy(14, 60)
    pdf.cell(55, 5, "(44) 3421-3141")

    pdf.line(48, 40, 48, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(55, 40)
    pdf.cell(50, 5, "Valtra/Fendt")
    pdf.set_xy(50, 45)
    pdf.cell(50, 5, "Campo Mourão/PR")
    pdf.set_xy(54, 50)
    pdf.cell(55, 5, "(44) 3016-7800")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(50, 56)
    pdf.cell(50, 5, "Kato - Goioerê/PR")
    pdf.set_xy(54, 61)
    pdf.cell(55, 5, "(44) 3521-8400")

    pdf.line(85, 40, 85, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(87, 40)
    pdf.cell(50, 5, "Valtra - Ubiratã/PR")
    pdf.set_xy(91, 45)
    pdf.cell(55, 5, "(44) 3543-4014")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(87, 55)
    pdf.cell(50, 5, "Valtra - Umuarama/PR")
    pdf.set_xy(91, 60)
    pdf.cell(55, 5, "(44) 3626-4300")

    pdf.line(125, 40, 125, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(131.5, 40)
    pdf.cell(50, 5, "Valtra/Fendt")
    pdf.set_xy(132, 44)
    pdf.cell(50, 5, "Londrina/PR")
    pdf.set_xy(130, 48)
    pdf.cell(55, 5, "(43) 3305-0880")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(137, 53)
    pdf.cell(50, 5, "Valtra")
    pdf.set_xy(127, 57)
    pdf.cell(50, 5, "Cornélio Procópio/PR")
    pdf.set_xy(131, 61)
    pdf.cell(55, 5, "(43) 3132-4040")

    pdf.line(165, 40, 165, 65)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(175, 40)
    pdf.cell(50, 5, "Valtra")
    pdf.set_xy(167, 44)
    pdf.cell(50, 5, "Jardim Alegre/PR")
    pdf.set_xy(168.5, 48)
    pdf.cell(50, 5, "(43) 3122-0050")

    pdf.set_font("Arial", size=10)
    pdf.set_xy(175, 53)
    pdf.cell(50, 5, "Valtra")
    pdf.set_xy(174, 57)
    pdf.cell(50, 5, "Irati/PR") 
    pdf.set_xy(168.5, 61)
    pdf.cell(55, 5, "(42) 3423-3400")


    # Requisição de compra
    pdf.set_font("Arial", size=18, style='BU')
    pdf.set_xy(0, 75)  # y = posição vertical
    pdf.cell(pdf.w, 10, "REQUISIÇÃO DE COMPRA", align='C')
    
    col1 = 50
    col2 = 140
    row_h = 8

    if solicitacao['nro_os'] == None:
        nro_os = ""
    else:
        nro_os = solicitacao['nro_os']

    campos = [
        ("Empresa/Revenda", f"{nome_revenda['empresa']}.{nome_revenda['revenda']} - {nome_revenda['nome_fantasia']}"),
        ("Solicitante", solicitacao['usuario_solicitante']),
        ("O.S da Solicitação", nro_os),
        ("Data da Solicitação", datetime.now().strftime("%d/%m/%Y")),
        ("Fornecedor", f"{fornecedor['cliente']} - {fornecedor['nome']}"),
        ("CNPJ Fornecedor", cnpj),
        ("Valor da Solicitação", f"R$ {str(solicitacao['valor']).replace('.', ',')}")
    ]

    pdf.set_xy(10, 85)
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
    pdf.multi_cell(0, row_h, "Teste gerar o PDF do lançamento de solicitação de despesas", border=1)

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