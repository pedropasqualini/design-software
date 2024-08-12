import pandas as pd
import os
from datetime import datetime
import ast

class ListaDeFuncionarios:
    def __init__(self):
        self.path = "data/lista_funcionarios.csv"
        if not os.path.exists(self.path):
            pd.DataFrame(columns=["id"]).to_csv(self.path, index=False)
        df = pd.read_csv(self.path)
        self.funcionarios = [Funcionario(**dados) for dados in df.to_dict(orient='records')]

    def criarItem(self, dadosFuncionario):
        dadosFuncionario['id'] = self.gerarId()
        novoFuncionario = Funcionario(**dadosFuncionario)
        self.gravarItem(novoFuncionario)
        return dadosFuncionario['id']

    def gerarId(self):
        if len(self.funcionarios) == 0:
            return 0
        id = int(self.funcionarios[-1].getDadosFuncionario()['id'] + 1)
        return id
    
    def gravarItem(self, novoFuncionario):
        novosDados = pd.DataFrame([novoFuncionario.getDadosFuncionario()])
        dadosAntigos = pd.DataFrame([f.getDadosFuncionario() for f in self.funcionarios])
        dadosConcatenados = pd.concat([dadosAntigos, novosDados])
        dadosConcatenados.to_csv(self.path, index=False)

    def buscarId(self, id):
        for funcionario in self.funcionarios:
            dadosFuncionario = funcionario.getDadosFuncionario()
            if dadosFuncionario['id'] == id and dadosFuncionario['situacao'] == 'ativo':
                return dadosFuncionario
        return None

    def atualizarItem(self, dadosFuncionario):
        for funcionario in self.funcionarios:
            if funcionario.getDadosFuncionario()['id'] == dadosFuncionario['id']:
                sucesso = funcionario.atualizarDados(dadosFuncionario)
                dados = pd.DataFrame([f.getDadosFuncionario() for f in self.funcionarios])
                dados.to_csv(self.path, index=False)
                return sucesso
            
    def confirmarExclusao(self, id):
        for funcionario in self.funcionarios:
            dadosFuncionario = funcionario.getDadosFuncionario()
            if dadosFuncionario['id'] == id:
                dadosFuncionario['situacao'] = 'marcado'
                sucesso = funcionario.atualizarDados(dadosFuncionario)
                dados = pd.DataFrame([f.getDadosFuncionario() for f in self.funcionarios])
                dados.to_csv(self.path, index=False)
                return sucesso
    
    def getListaFuncionarios(self):
        return self.funcionarios

class Funcionario:
    def __init__(self, **dadosFuncionario):
        self.__dict__.update(dadosFuncionario)
        if 'tipoPagamento' not in self.__dict__.keys():
            self.tipoPagamento = "retirada"
        if 'situacao' not in self.__dict__.keys():
            self.situacao = "ativo"

    def getDadosFuncionario(self):
        return self.__dict__

    def atualizarDados(self, dadosFuncionario):
        self.__dict__.update(dadosFuncionario)
        return True

class ListaDeVendas:
    def __init__(self):
        self.path = "data/lista_vendas.csv"
        if not os.path.exists(self.path):
            pd.DataFrame(columns=["id"]).to_csv(self.path, index=False)
        df = pd.read_csv(self.path)
        self.vendas = [Venda(**dados) for dados in df.to_dict(orient='records')]

    def criarItem(self, dadosVenda):
        dadosVenda['id'] = self.gerarId()
        novaVenda = Venda(**dadosVenda)
        self.gravarItem(novaVenda)
        return dadosVenda['id']

    def gerarId(self):
        if len(self.vendas) == 0:
            return 0
        id = int(self.vendas[-1].getDadosVenda()['id'] + 1)
        return id
    
    def gravarItem(self, novaVenda):
        novosDados = pd.DataFrame([novaVenda.getDadosVenda()])
        dadosAntigos = pd.DataFrame([f.getDadosVenda() for f in self.vendas])
        dadosConcatenados = pd.concat([dadosAntigos, novosDados])
        dadosConcatenados.to_csv(self.path, index=False)

    def buscarId(self, id):
        for venda in self.vendas:
            dadosVenda = venda.getDadosVenda()
            if dadosVenda['id'] == id:
                return dadosVenda
        return None

    def atualizarItem(self, dadosVenda):
        for venda in self.vendas:
            if venda.getDadosVenda()['id'] == dadosVenda['id']:
                sucesso = venda.atualizarDados(dadosVenda)
                dados = pd.DataFrame([f.getDadosVenda() for f in self.vendas])
                dados.to_csv(self.path, index=False)
                return sucesso
            
    def confirmarExclusao(self, id):
        for venda in self.vendas:
            dadosVenda = venda.getDadosVenda()
            if dadosVenda['id'] == id:
                self.vendas.remove(venda)
                dados = pd.DataFrame([v.getDadosVenda() for v in self.vendas])
                if len(dados) == 0:
                    pd.DataFrame(columns=["id"]).to_csv(self.path, index=False)
                else:
                    dados.to_csv(self.path, index=False)
                return True

class Venda:
    def __init__(self, **dadosVenda):
        self.__dict__.update(dadosVenda)

    def getDadosVenda(self):
        return self.__dict__

    def atualizarDados(self, dadosVenda):
        self.__dict__.update(dadosVenda)
        return True

class ListaDeProjetos:
    def __init__(self):
        projeto1 = Projeto(**{"id": 0, "preco": 10})
        projeto2 = Projeto(**{"id": 1, "preco": 15})
        projeto3 = Projeto(**{"id": 2, "preco": 20})
        self.projetos = [projeto1, projeto2, projeto3]
    
    def getProjetos(self):
        return self.projetos

class Projeto:
    def __init__(self, **dadosProjeto):
        self.__dict__.update(dadosProjeto)

    def getDadosProjeto(self):
        return self.__dict__

class Pagamento:
    def __init__(self):
        self.dia = datetime.now().strftime("%d/%m/%Y")
        self.pagamento = 0
    
    def calcularPagamento(self, dadosFuncionario):
        listaProjetos = ListaDeProjetos()
        self.tipoPagamento = dadosFuncionario['tipoPagamento']
        self.nome = dadosFuncionario['nome']
        if dadosFuncionario['tipoFuncionario'] == 'assalariado':
            self.pagamento = dadosFuncionario['salario']
        elif dadosFuncionario['tipoFuncionario'] == 'hora':
            if 'cartelaPontos' not in dadosFuncionario.keys() or type(dadosFuncionario['cartelaPontos']) == float:
                print("Cartela de funcionários não criada.")
                return False
            self.pagamento = 0
            projetos = [p.getDadosProjeto() for p in listaProjetos.getProjetos()]
            if type(dadosFuncionario['cartelaPontos']) == str:
                dadosFuncionario['cartelaPontos'] = ast.literal_eval(dadosFuncionario['cartelaPontos'])
            for idProjeto, horas in dadosFuncionario['cartelaPontos']['projeto'].items():
                for projeto in projetos:
                    if projeto['id'] == idProjeto:
                        self.pagamento += projeto['preco'] * horas
        elif dadosFuncionario['tipoFuncionario'] == 'comissionado':
            pass

        self.pagamento *= (1 - (dadosFuncionario['deducoesFiscaisPadrao'] + dadosFuncionario['outrasDeducoes']))

    def getPagamento(self):
        return self.__dict__