import random

TAMANHO_GENOMA = 192
TAXA_MUTACAO = 0.01
TAXA_CRUZAMENTO = 0.8

class Individuo:
    
    def __init__(self):
        self.pool_genetico = []
        for i in range(TAMANHO_GENOMA):
            self.pool_genetico.append(0)
    
    def gerarGenes(self):
        for i in range(TAMANHO_GENOMA):
            self.pool_genetico[i] = random.randint(0, 1)
    
    def getAptidao(self, fn):
        return fn(self.pool_genetico)
    
    def cruzar(self, parceiro):
        ponto_cruzamento = random.randint(0, 191)
        filho = Individuo()
        flag = 0
        for i in range(TAMANHO_GENOMA):
            if flag == 0:
                filho.pool_genetico[i] = self.pool_genetico[i]
                if i == ponto_cruzamento:
                    flag = 1
            elif flag == 1:
                filho.pool_genetico[i] = parceiro.pool_genetico[i]
        return filho
    
    def mutar(self, taxa_mutacao):
        if taxa_mutacao < 0 or taxa_mutacao > 1:
            taxa_mutacao = 0
        for i in range(TAMANHO_GENOMA):
            x = random.randint(0, 100)
            if x < (taxa_mutacao * 100):
                self.pool_genetico[i] = 1 if self.pool_genetico[i] == 0 else 0

class Populacao:
    
    def __init__(self, fn):
        self.tamanho_populacao = 0
        self.individuos = []
        self.proxima_geracao = []
        self.funcao_aptidao = fn
    
    def inicializarPopulacao(self, p=10):
        self.tamanho_populacao = p
        for i in range(self.tamanho_populacao):
            self.individuos.append(Individuo())
            self.individuos[i].gerarGenes()
    
    def adicionarIndividuo(self, x):
        self.individuos.append(x)
        self.tamanho_populacao += 1
    
    def removerIndividuo(self, i):
        self.individuos.pop(i)
        self.tamanho_populacao -= 1
    
    def obterMelhorAptidao(self):
        melhor_valor = 0
        melhor_indice = 0
        for i in range(self.tamanho_populacao):
            valor_atual = self.individuos[i].getAptidao(self.funcao_aptidao)
            if valor_atual > melhor_valor:
                melhor_valor = valor_atual
                melhor_indice = i
        return self.individuos[melhor_indice], melhor_indice
    
    def selecaoTorneio(self, tamanho_amostra=3):
        if tamanho_amostra > self.tamanho_populacao:
            tamanho_amostra = 3
        torneio = Populacao(self.funcao_aptidao)
        for i in range(tamanho_amostra):
            torneio.adicionarIndividuo(self.individuos[random.randint(0, 9)])
        pai1, i = torneio.obterMelhorAptidao()
        torneio.removerIndividuo(i)
        pai2, i = torneio.obterMelhorAptidao()
        del torneio
        return pai1, pai2
    
    def cruzar(self, pai1, pai2):
        filho = pai1.cruzar(pai2)
        filho.mutar(TAXA_MUTACAO)
        return filho
    
    def gerarProximaGeracao(self, elite=1, alvo=-1):
        tamanho_nova_geracao = self.tamanho_populacao
        if elite == 1:
            tamanho_nova_geracao -= 1
            self.proxima_geracao.append(self.obterMelhorAptidao()[0])
        for i in range(self.tamanho_populacao):
            pai1, pai2 = self.selecaoTorneio()
            if random.randint(0, 99) < (TAXA_CRUZAMENTO * 100):
                self.proxima_geracao.append(self.cruzar(pai1, pai2))
            else:
                pai1.mutar(TAXA_MUTACAO)
                self.proxima_geracao.append(pai1)
        self.individuos = self.proxima_geracao.copy()
        self.proxima_geracao.clear()
        if self.obterMelhorAptidao()[0].getAptidao(self.funcao_aptidao) == alvo:
            return True
        return False

class TabuleiroCavalo:
    @staticmethod
    def posicaoParaTabuleiro(pos):
        bpos = [(pos[1] - 1), 0]
        if pos[0] == "A":
            bpos[1] = 0
        elif pos[0] == "B":
            bpos[1] = 1
        elif pos[0] == "C":
            bpos[1] = 2
        elif pos[0] == "D":
            bpos[1] = 3
        elif pos[0] == 'E':
            bpos[1] = 4
        elif pos[0] == "F":
            bpos[1] = 5
        elif pos[0] == "G":
            bpos[1] = 6
        elif pos[0] == "H":
            bpos[1] = 7
        return bpos
    
    def __init__(self, kpos=["E4"]):
        self.posicao_cavalo = self.posicaoParaTabuleiro([kpos[0], int(kpos[1])])
        self.posicao_original = self.posicao_cavalo.copy()
        self.tabuleiro = [0] * 8
        for i in range(8):
            self.tabuleiro[i] = [0] * 8
        self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
    
    def reset(self):
        self.posicao_cavalo = self.posicao_original
        for i in range(8):
            self.tabuleiro[i] = [0] * 8
        self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
    
    def foiVisitado(self, pos):
        return self.tabuleiro[pos[0]][pos[1]] == 1
    
    @staticmethod
    def decodificarMovimento(enc_mv):
        return (enc_mv[0] * 4 + enc_mv[1] * 2 + enc_mv[2])
    
    @staticmethod
    def codificarMovimento(mv):
        if mv == 0:
            return [0, 0, 0]
        elif mv == 1:
            return [0, 0, 1]
        elif mv == 2:
            return [0, 1, 0]
        elif mv == 3:
            return [0, 1, 1]
        elif mv == 4:
            return [1, 0, 0]
        elif mv == 5:
            return [1, 0, 1]
        elif mv == 6:
            return [1, 1, 0]
        elif mv == 7:
            return [1, 1, 1]
    
    def mover(self, enc_mv):
        mv = self.decodificarMovimento(enc_mv)
        if mv == 0:
            if self.posicao_cavalo[0] >= 2 and self.posicao_cavalo[1] <= 6:
                if self.foiVisitado([self.posicao_cavalo[0] - 2, self.posicao_cavalo[1] + 1]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] - 2, self.posicao_cavalo[1] + 1]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 1:
            if self.posicao_cavalo[0] >= 1 and self.posicao_cavalo[1] <= 5:
                if self.foiVisitado([self.posicao_cavalo[0] - 1, self.posicao_cavalo[1] + 2]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] - 1, self.posicao_cavalo[1] + 2]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 2:
            if self.posicao_cavalo[0] <= 6 and self.posicao_cavalo[1] <= 5:
                if self.foiVisitado([self.posicao_cavalo[0] + 1, self.posicao_cavalo[1] + 2]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] + 1, self.posicao_cavalo[1] + 2]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 3:
            if self.posicao_cavalo[0] <= 5 and self.posicao_cavalo[1] <= 6:
                if self.foiVisitado([self.posicao_cavalo[0] + 2, self.posicao_cavalo[1] + 1]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] + 2, self.posicao_cavalo[1] + 1]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 4:
            if self.posicao_cavalo[0] <= 5 and self.posicao_cavalo[1] >= 1:
                if self.foiVisitado([self.posicao_cavalo[0] + 2, self.posicao_cavalo[1] - 1]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] + 2, self.posicao_cavalo[1] - 1]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 5:
            if self.posicao_cavalo[0] <= 6 and self.posicao_cavalo[1] >= 2:
                if self.foiVisitado([self.posicao_cavalo[0] + 1, self.posicao_cavalo[1] - 2]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] + 1, self.posicao_cavalo[1] - 2]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 6:
            if self.posicao_cavalo[0] >= 1 and self.posicao_cavalo[1] >= 2:
                if self.foiVisitado([self.posicao_cavalo[0] - 1, self.posicao_cavalo[1] - 2]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] - 1, self.posicao_cavalo[1] - 2]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
        elif mv == 7:
            if self.posicao_cavalo[0] >= 2 and self.posicao_cavalo[1] >= 1:
                if self.foiVisitado([self.posicao_cavalo[0] - 2, self.posicao_cavalo[1] - 1]):
                    return False
                self.posicao_cavalo = [self.posicao_cavalo[0] - 2, self.posicao_cavalo[1] - 1]
                self.tabuleiro[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 1
                return True
            return False
    
    def tentarReparar(self, lista_movimentos, indice):
        movimento_original = self.decodificarMovimento(lista_movimentos[indice * 3:(indice + 1) * 3])
        for i in range(8):
            if i != movimento_original:
                movimento_encodificado = self.codificarMovimento(i)
                if self.mover(movimento_encodificado):
                    lista_movimentos[indice * 3] = movimento_encodificado[0]
                    lista_movimentos[indice * 3 + 1] = movimento_encodificado[1]
                    lista_movimentos[indice * 3 + 2] = movimento_encodificado[2]
                    return True
        return False
    
    def obterMovimentosValidos(self, lista_movimentos):
        self.reset()
        num_movimentos = len(lista_movimentos) // 3
        assert len(lista_movimentos) % 3 == 0
        contador = 0
        for i in range(num_movimentos):
            if not (self.mover(lista_movimentos[i * 3:(i + 1) * 3])):
                if not (self.tentarReparar(lista_movimentos, i)):
                    break
            contador += 1
        return contador
    
    def mostrarMovimentos(self, lista_movimentos):
        self.reset()
        num_movimentos = len(lista_movimentos) // 3
        assert len(lista_movimentos) % 3 == 0
        matriz_movimentos = [-1] * 8
        for i in range(8):
            matriz_movimentos[i] = [-1] * 8
        matriz_movimentos[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = 0
        for i in range(num_movimentos):
            if not (self.mover(lista_movimentos[i * 3:(i + 1) * 3])):
                break
            matriz_movimentos[self.posicao_cavalo[0]][self.posicao_cavalo[1]] = i + 1
        print("----- Matriz de Movimentos -----")
        for i in reversed(range(8)):
            print(matriz_movimentos[i])
        return

while True:
    c = input("Informe a posição do cavalo no xadrez (ex: A7): ")
    
    if (c[0].isalpha()) and (c[0].upper() >= 'A' and c[0].upper() <= 'H') and (c[1].isdigit()) and (int(c[1]) > 0 and int(c[1]) < 9):
        cs = [str(c[0].upper()), int(c[1])]
        break
    print("Tente Novamente")

tabuleiro_cavalo = TabuleiroCavalo([cs[0], int(cs[1])])
populacao_cavalo = Populacao(tabuleiro_cavalo.obterMovimentosValidos)
populacao_cavalo.inicializarPopulacao(50)

for i in range(2000):
    if i % 350 == 0:
        TAXA_MUTACAO = 0.1
    if i % 350 == 50:
        TAXA_MUTACAO = 0.01
        
    if (populacao_cavalo.gerarProximaGeracao(1, 63)):
        print("Encontrado na Geração: ", i)
        break
    
x, _ = populacao_cavalo.obterMelhorAptidao()
if (x.getAptidao(tabuleiro_cavalo.obterMovimentosValidos)) != 63:
    print("Não foi possível encontrar um caminho em 2000 gerações")
    print("Aptidão final: ", x.getAptidao(tabuleiro_cavalo.obterMovimentosValidos))
tabuleiro_cavalo.mostrarMovimentos(x.pool_genetico)
