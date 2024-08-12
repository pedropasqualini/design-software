import os
from componentes_empresa import ListaDeFuncionarios, ListaDeVendas, ListaDeProjetos, Pagamento
from datetime import datetime
import ast

class Empresa:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.listaFuncionarios = ListaDeFuncionarios()
        self.listaVendas = ListaDeVendas()
        self.listaProjetos = ListaDeProjetos()
        self.executaSistema()

    def executaSistema(self):
        while 1:
            print("Bem vindo ao sistema das Organizações Tabajara.")
            print("Digite o número da opção que deseja acessar:")
            print("\t(1) Manter Informações dos Funcionários")
            print("\t(2) Manter Ordem de Compra")
            print("\t(3) Manter Cartão de Ponto")
            print("\t(4) Execute Folha de Pagamento")
            funcaoSistema = input()
            
            if funcaoSistema == "1":
                self.gerenciarFuncionario()
                funcaoGerenciaFuncionario = input()
                if funcaoGerenciaFuncionario == "1":
                    self.adicionarFuncionario()
                    id = self.cadastrarFuncionario()
                    print(f"O funcionário foi criado com id {id}")
                    break

                elif funcaoGerenciaFuncionario == "2":
                    self.atualizarFuncionario()
                    id = input()
                    dadosFuncionario = self.buscarId(id)
                    self.imprimeDadosFuncionario(dadosFuncionario)
                    if self.atualizarInfoFuncionario(dadosFuncionario):
                        print("Informações atualizadas com sucesso.")
                    break

                elif funcaoGerenciaFuncionario == "3":
                    self.excluirFuncionario()
                    id = input()
                    dadosFuncionario = self.buscarId(id)
                    self.imprimeDadosFuncionario(dadosFuncionario)
                    print("Confirma a exclusão? Responda 's' se confirmar")
                    resposta = input()
                    if resposta == "s" and self.confirmarExclusao(dadosFuncionario['id']):
                        print("Excluído com sucesso.")
                        break

                else:
                    print("Erro de input. Abortando.")
                    exit(1)

            elif funcaoSistema == "2":
                self.gerenciarVenda()
                funcaoVenda = input()
                if funcaoVenda == "1":
                    self.adicionarVenda()
                    id = self.cadastrarVenda()
                    print(f"A venda foi criada com id {id}")
                    break

                elif funcaoVenda == "2":
                    self.atualizarVenda()
                    id = input()
                    dadosVenda = self.buscarIdVenda(id)
                    self.imprimeDadosVenda(dadosVenda)
                    if self.atualizarInfoVenda(dadosVenda):
                        print("Informações atualizadas com sucesso.")
                    break

                elif funcaoVenda == "3":
                    self.excluirVenda()
                    id = input()
                    dadosVenda = self.buscarIdVenda(id)
                    self.imprimeDadosVenda(dadosVenda)
                    print("Confirma a exclusão? Responda 's' se confirmar")
                    resposta = input()
                    if resposta == "s" and self.confirmarExclusaoVenda(dadosVenda['id']):
                        print("Excluído com sucesso.")
                        break

                else:
                    print("Erro de input. Abortando.")
                    exit(1)

            elif funcaoSistema == "3":
                self.gerenciarCartaoPonto()
                id = int(input())
                dadosFuncionario = self.buscarId(id)
                if not dadosFuncionario:
                    print("Funcionário inválido")
                    exit(1)
                cartela = self.criaRecuperaCartela(dadosFuncionario)
                print(cartela)
                self.enviarCartela(cartela, dadosFuncionario)
                projetos = [p.getDadosProjeto() for p in self.listaProjetos.getProjetos()]
                print(projetos)
                self.editarHoras(cartela, dadosFuncionario)
                break

            elif funcaoSistema == "4":
                self.folhaPagamento()
                break

            else:
                print("Erro de input. Abortando.")
                exit(1)

    def gerenciarFuncionario(self):
        print("Você selecionou Manter Informações dos Funcionários.")
        print("Digite o número da operação desejada:")
        print("\t(1) Adicionar Funcionários")
        print("\t(2) Atualizar Funcionários")
        print("\t(3) Excluir Funcionários")
        
    def adicionarFuncionario(self):
        print("Digite as seguintes informações do funcionário:")

    def cadastrarFuncionario(self):
        dadosFuncionario = {}
        dadosFuncionario['nome'] = input("Nome:\n")
        dadosFuncionario['tipoFuncionario'] = input("Tipo de funcionário (hora, assalariado, comissionado):\n")
        dadosFuncionario['endereco'] = input("Endereço para correspondência:\n")
        dadosFuncionario['numeroSegurancaSocial'] = input("Número da Segurança Social:\n")
        dadosFuncionario['deducoesFiscaisPadrao'] = input("Deduções fiscais padrão (float):\n")
        dadosFuncionario['outrasDeducoes'] = input("Outras deduções (float):\n")
        dadosFuncionario['numeroTelefone'] = input("Número de telefone (string):\n")
        if dadosFuncionario['tipoFuncionario'] == 'hora':
            dadosFuncionario['taxaHoraria'] = input("Taxa horária (float):\n")
            dadosFuncionario['salario'] = None
            dadosFuncionario['taxaComissao'] = None
        elif dadosFuncionario['tipoFuncionario'] == 'assalariado':
            dadosFuncionario['taxaHoraria'] = None
            dadosFuncionario['salario'] = input("Salário:\n")
            dadosFuncionario['taxaComissao'] = None
        elif dadosFuncionario['tipoFuncionario'] == 'comissionado':
            dadosFuncionario['taxaHoraria'] = None
            dadosFuncionario['salario'] = input("Salário:\n")
            dadosFuncionario['taxaComissao'] = input("Taxa de comissão:\n")
        dadosFuncionario['limiteHoras'] = input("Limite de horas:\n")
        id = self.listaFuncionarios.criarItem(dadosFuncionario)
        return id

    def atualizarFuncionario(self):
        print("Digite a ID do funcionário:")
    
    def buscarId(self, id):
        dadosFuncionario = self.listaFuncionarios.buscarId(int(id))
        while (not dadosFuncionario):
            print("Id não encontrada, por favor digite outra. Digite s para sair.")
            id = input()
            if id == 's':
                exit(1)
            dadosFuncionario = self.listaFuncionarios.buscarId(int(id))
        return dadosFuncionario

    def buscarIdVenda(self, id):
        dadosVenda = self.listaVendas.buscarId(int(id))
        while (not dadosVenda):
            print("Id não encontrada, por favor digite outra. Digite s para sair.")
            id = input()
            if id == 's':
                exit(1)
            dadosVenda = self.listaVendas.buscarId(int(id))
        return dadosVenda

    def imprimeDadosFuncionario(self, funcionario):
        print("Os dados atuais do funcionario são:")
        [print(f"{key}: {value}") for key, value in funcionario.items()]

    def atualizarInfoFuncionario(self, dadosFuncionario):
        for key in dadosFuncionario.keys():
            if key == 'id':
                continue
            print(f"Escreva o novo valor para {key}. Se não quiser sobrescrever, deixe em branco.")
            new = input()
            if new:
                dadosFuncionario[key] = new
        return self.listaFuncionarios.atualizarItem(dadosFuncionario)

    def excluirFuncionario(self):
        print("Digite a ID do funcionário:")

    def confirmarExclusao(self, id):
        return self.listaFuncionarios.confirmarExclusao(id)

    def gerenciarVenda(self):
        print("Você selecionou Manter Ordem de Compra.")
        print("Digite o número da operação desejada:")
        print("\t(1) Adicionar Ordem de Compra")
        print("\t(2) Atualizar Ordem de Compra")
        print("\t(3) Excluir Ordem de Compra")

    def adicionarVenda(self):
        print("Digite as seguintes informações da venda:")

    def cadastrarVenda(self):
        dadosVenda = {}
        dadosVenda['pontoContatoCliente'] = input("Ponto de contato do cliente:\n")
        dadosVenda['enderecoCobranca'] = input("Endereço de cobrança do cliente:\n")
        dadosVenda['produtosAdquiridos'] = input("Produtos Adquiridos:\n")
        dadosVenda['data'] = input("Data:\n")
        id = self.listaVendas.criarItem(dadosVenda)
        return id
    
    def atualizarVenda(self):
        print("Digite a ID da venda:")
    
    def imprimeDadosVenda(self, venda):
        print("Os dados atuais da venda são:")
        [print(f"{key}: {value}") for key, value in venda.items()]

    def atualizarInfoVenda(self, dadosVenda):
        for key in dadosVenda.keys():
            if key == 'id':
                continue
            print(f"Escreva o novo valor para {key}. Se não quiser sobrescrever, deixe em branco.")
            new = input()
            if new:
                dadosVenda[key] = new
        return self.listaVendas.atualizarItem(dadosVenda)

    def excluirVenda(self):
        print("Digite a ID da venda:")

    def confirmarExclusaoVenda(self, id):
        return self.listaVendas.confirmarExclusao(id)

    def gerenciarCartaoPonto(self):
        print("Digite sua ID de funcionário:")

    def criaRecuperaCartela(self, dadosFuncionario):
        if 'cartelaPontos' not in dadosFuncionario.keys() or not dadosFuncionario['cartelaPontos'] or type(dadosFuncionario['cartelaPontos']) == float:
            now = datetime.now()
            nextMonth = datetime(now.year, now.month + 1, now.day)
            dadosFuncionario['cartelaPontos'] = {"dataInicio": now.strftime("%d/%m/%Y"), "dataFim": nextMonth.strftime("%d/%m/%Y"), "projeto": {}, "enviado": False}
            self.listaFuncionarios.atualizarItem(dadosFuncionario)
            return dadosFuncionario['cartelaPontos']
        else:
            return ast.literal_eval(dadosFuncionario['cartelaPontos'])

    def editarHoras(self, cartela, dadosFuncionario):
        if cartela['enviado']:
            print("Cartela enviada.")
            return
        print("Qual projeto gostaria de registrar na cartela?")
        idProjeto = int(input())
        print("Quantas horas gostaria de registrar?")
        horas = int(input())
        if idProjeto in cartela['projeto'].keys():
            cartela['projeto'][idProjeto] += horas
        else:
            cartela['projeto'][idProjeto] = horas
        dadosFuncionario['cartelaPontos'] = cartela
        self.listaFuncionarios.atualizarItem(dadosFuncionario)

    def enviarCartela(self, cartela, dadosFuncionario):
        if cartela['enviado']:
            return
        print("Você gostaria de enviar a cartela? s/n")
        resposta = input()
        if resposta == "s":
            cartela['enviado'] = True
            dadosFuncionario['cartelaPontos'] = cartela
            self.listaFuncionarios.atualizarItem(dadosFuncionario)

    def folhaPagamento(self):
        listaFuncionarios = self.listaFuncionarios.getListaFuncionarios()
        folha = []
        for funcionario in listaFuncionarios:
            dadosFuncionario = funcionario.getDadosFuncionario()
            pagamento = Pagamento()
            pagamento.calcularPagamento(dadosFuncionario)
            folha.append(pagamento)
        print([f.getPagamento() for f in folha])