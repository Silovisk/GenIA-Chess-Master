import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Image
from tqdm import tqdm  # Importe o módulo tqdm para a barra de progresso

def calcular_aptidao(cromossomo):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if cromossomo[i] == cromossomo[j] or abs(cromossomo[i] - cromossomo[j]) == j - i:
                conflitos += 1
    return conflitos

def criar_populacao(tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        cromossomo = list(range(8))
        random.shuffle(cromossomo)
        populacao.append(cromossomo)
    return populacao

def encontrar_solucoes(tamanho_populacao, geracoes, taxa_mutacao):
    solucoes_unicas = set()
    total_testes = 0

    for solucao_num in tqdm(range(1, 40320), unit="solução"):  # Barra de progresso
        populacao = criar_populacao(tamanho_populacao)
        for geracao in range(geracoes):
            populacao = sorted(populacao, key=lambda c: calcular_aptidao(c))
            if calcular_aptidao(populacao[0]) == 0:
                solucao = populacao[0]
                if tuple(solucao) not in solucoes_unicas:
                    solucoes_unicas.add(tuple(solucao))
                    total_testes += geracao
                break
            nova_populacao = []
            while len(nova_populacao) < tamanho_populacao:
                pai1, pai2 = random.choices(populacao, k=2)
                filho1, filho2 = cruzar_pais(pai1, pai2)
                filho1 = mutar_cromossomo(filho1, taxa_mutacao)
                filho2 = mutar_cromossomo(filho2, taxa_mutacao)
                nova_populacao.extend([filho1, filho2])
            populacao = nova_populacao
        else:
            total_testes += geracoes

    print(f"Total de soluções únicas: {len(solucoes_unicas)}")
    print(f"Total de testes: {total_testes}")
    return [list(solucao) for solucao in solucoes_unicas]

def cruzar_pais(pai1, pai2):
    ponto_corte = random.randint(1, 6)
    filho1 = pai1[:ponto_corte] + [gene for gene in pai2 if gene not in pai1[:ponto_corte]]
    filho2 = pai2[:ponto_corte] + [gene for gene in pai1 if gene not in pai2[:ponto_corte]]
    return filho1, filho2

def mutar_cromossomo(cromossomo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(8), 2)
        cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]
    return cromossomo

def gerar_pdf_com_solucoes(solucoes):
    doc = SimpleDocTemplate("rainha.pdf", pagesize=letter)
    elements = []

    for index, solucao in enumerate(solucoes):
        # Criar o tabuleiro
        tabuleiro = [[' ' for _ in range(8)] for _ in range(8)]
        for i, j in enumerate(solucao):
            tabuleiro[i][j] = 'Q'

        # Células do tabuleiro coloridas
        table_data = []
        for row in tabuleiro:
            row_data = []
            for item in row:
                if item == 'Q':
                    cell = Image("rainha.jpg", 1 * inch, 1 * inch)  # Substitua 'rainha.jpg' pelo caminho da imagem da rainha
                else:
                    cell = ''
                row_data.append(cell)
            table_data.append(row_data)

        table = Table(table_data, colWidths=1 * inch, rowHeights=1 * inch)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ]))

        elements.append(table)

        if index < len(solucoes) - 1:
            elements.append(PageBreak())

    doc.build(elements)

if __name__ == "__main__":
    tamanho_populacao = 100
    geracoes = 1000
    taxa_mutacao = 0.1

    solucoes = encontrar_solucoes(tamanho_populacao, geracoes, taxa_mutacao)
    gerar_pdf_com_solucoes(solucoes)
