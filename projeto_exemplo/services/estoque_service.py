import os

from algoritmos.busca_binaria import buscar_produto_por_id
from algoritmos.ordenacao import ordenar_produtos_por_id
from estruturas.fila import Fila
from estruturas.lde import LDE
from estruturas.lse import LSE
from estruturas.pilha import Pilha
from models.cliente import Cliente
from models.produto import Produto
from models.venda import Venda
from services.persistencia_service import PersistenciaService


class EstoqueService:
    def __init__(self):
        pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pasta_data = os.path.join(pasta_raiz, "data")

        self.clientes = LSE()
        self.produtos = LDE()
        self.vendas = Fila()
        self.historico = Pilha()
        self.persistencia = PersistenciaService(pasta_data)

        self.carregar_dados()

    def carregar_dados(self):
        for cliente in self.persistencia.carregar_clientes():
            if self.clientes.buscar(cliente.codigo) is None:
                self.clientes.inserir_fim(cliente)

        for produto in self.persistencia.carregar_produtos():
            if self.produtos.buscar(produto.codigo) is None:
                self.produtos.inserir_fim(produto)

        for venda in self.persistencia.carregar_vendas():
            self.vendas.enqueue(venda)

    def _gerar_proximo_codigo(self, registros):
        maior_codigo = 0

        for registro in registros:
            if registro.codigo > maior_codigo:
                maior_codigo = registro.codigo

        return maior_codigo + 1

    def gerar_proximo_codigo_cliente(self):
        return self._gerar_proximo_codigo(self.clientes.listar())

    def gerar_proximo_codigo_produto(self):
        return self._gerar_proximo_codigo(self.produtos.listar())

    def gerar_proximo_codigo_venda(self):
        return self._gerar_proximo_codigo(self.vendas.listar())

    def cadastrar_cliente(self, nome):
        cliente = Cliente(self.gerar_proximo_codigo_cliente(), nome)
        self.clientes.inserir_fim(cliente)
        self.salvar_clientes()
        self.historico.push(("remover_cliente", cliente.codigo))
        return cliente

    def listar_clientes(self):
        return self.clientes.listar()

    def buscar_cliente(self, codigo):
        return self.clientes.buscar(int(codigo))

    def remover_cliente(self, codigo):
        codigo = int(codigo)

        if self.buscar_cliente(codigo) is None:
            raise ValueError("Cliente nao encontrado.")

        if any(venda.codigo_cliente == codigo for venda in self.vendas.listar()):
            raise ValueError("Nao e possivel remover um cliente que possui vendas.")

        cliente = self.clientes.remover(codigo)
        self.salvar_clientes()
        self.historico.push(("restaurar_cliente", cliente))
        return cliente

    def cadastrar_produto(self, nome, preco, quantidade):
        produto = Produto(
            self.gerar_proximo_codigo_produto(),
            nome,
            preco,
            quantidade,
        )
        self.produtos.inserir_fim(produto)
        self.salvar_produtos()
        self.historico.push(("remover_produto", produto.codigo))
        return produto

    def listar_produtos(self):
        return self.produtos.listar()

    def listar_produtos_inverso(self):
        return self.produtos.listar_inverso()

    def listar_produtos_ordenados_por_id(self):
        return ordenar_produtos_por_id(self.produtos.listar())

    def buscar_produto(self, codigo):
        return self.produtos.buscar(int(codigo))

    def buscar_produto_binario(self, codigo):
        return buscar_produto_por_id(
            self.listar_produtos_ordenados_por_id(),
            int(codigo),
        )

    def atualizar_estoque(self, codigo, nova_quantidade):
        produto = self.buscar_produto(codigo)

        if produto is None:
            raise ValueError("Produto nao encontrado.")

        quantidade_anterior = produto.quantidade
        produto.atualizar_estoque(nova_quantidade)

        self.salvar_produtos()
        self.historico.push(("estoque", produto.codigo, quantidade_anterior))
        return produto

    def remover_produto(self, codigo):
        codigo = int(codigo)

        if self.buscar_produto(codigo) is None:
            raise ValueError("Produto nao encontrado.")

        for venda in self.vendas.listar():
            for item in venda.itens:
                if item["codigo_produto"] == codigo:
                    raise ValueError(
                        "Nao e possivel remover um produto que possui vendas."
                    )

        produto = self.produtos.remover(codigo)
        self.salvar_produtos()
        self.historico.push(("restaurar_produto", produto))
        return produto

    def realizar_venda_exemplo(self, codigo_cliente, codigo_produto, quantidade):
        cliente = self.buscar_cliente(codigo_cliente)

        if cliente is None:
            raise ValueError("Cliente nao encontrado.")

        produto = self.buscar_produto(codigo_produto)

        if produto is None:
            raise ValueError("Produto nao encontrado.")

        quantidade = int(quantidade)

        if quantidade <= 0:
            raise ValueError("A quantidade da venda deve ser maior que zero.")

        if quantidade > produto.quantidade:
            raise ValueError("Estoque insuficiente para realizar a venda.")

        item = {
            "codigo_produto": produto.codigo,
            "quantidade": quantidade,
            "preco_unitario": produto.preco,
        }

        venda = Venda(
            self.gerar_proximo_codigo_venda(),
            cliente.codigo,
            [item],
        )

        produto.atualizar_estoque(produto.quantidade - quantidade)
        self.vendas.enqueue(venda)

        self.salvar_produtos()
        self.salvar_vendas()

        self.historico.push(("desfazer_venda", venda.codigo))
        return venda

    def listar_vendas(self):
        return self.vendas.listar()

    def primeira_venda(self):
        if self.vendas.is_empty():
            return None

        return self.vendas.front()

    def valor_total_estoque(self):
        return sum(
            produto.preco * produto.quantidade
            for produto in self.produtos.listar()
        )

    def valor_total_vendas(self):
        return sum(venda.valor_total for venda in self.vendas.listar())

    def clientes_e_valores_totais_gastos(self):
        totais = []

        for cliente in self.clientes.listar():
            total = sum(
                venda.valor_total
                for venda in self.vendas.listar()
                if venda.codigo_cliente == cliente.codigo
            )
            totais.append((cliente, total))

        return totais

    def cliente_que_mais_gastou(self):
        totais = self.clientes_e_valores_totais_gastos()

        if not totais:
            return None

        cliente, total = totais[0]

        for candidato, valor in totais[1:]:
            if valor > total:
                cliente, total = candidato, valor

        return cliente, total

    def produto_mais_vendido(self):
        quantidades = {}

        for venda in self.vendas.listar():
            for item in venda.itens:
                codigo = item["codigo_produto"]
                quantidades[codigo] = (
                    quantidades.get(codigo, 0) + item["quantidade"]
                )

        if not quantidades:
            return None

        codigo = max(quantidades, key=quantidades.get)
        return self.buscar_produto(codigo), quantidades[codigo]

    def desfazer_ultima_operacao(self):
        if self.historico.is_empty():
            raise ValueError("Nao ha operacoes para desfazer nesta execucao.")

        operacao = self.historico.pop()
        tipo = operacao[0]

        if tipo == "remover_cliente":
            self.clientes.remover(operacao[1])
            self.salvar_clientes()

        elif tipo == "restaurar_cliente":
            self.clientes.inserir_fim(operacao[1])
            self.salvar_clientes()

        elif tipo == "remover_produto":
            self.produtos.remover(operacao[1])
            self.salvar_produtos()

        elif tipo == "restaurar_produto":
            self.produtos.inserir_fim(operacao[1])
            self.salvar_produtos()

        elif tipo == "estoque":
            produto = self.buscar_produto(operacao[1])
            produto.atualizar_estoque(operacao[2])
            self.salvar_produtos()

        elif tipo == "desfazer_venda":
            venda = self.vendas.remover_por_codigo(operacao[1])

            for item in venda.itens:
                produto = self.buscar_produto(item["codigo_produto"])
                produto.atualizar_estoque(
                    produto.quantidade + item["quantidade"]
                )

            self.salvar_produtos()
            self.salvar_vendas()

        return "Operacao desfeita com sucesso."

    def salvar_clientes(self):
        self.persistencia.salvar_clientes(self.clientes.listar())

    def salvar_produtos(self):
        self.persistencia.salvar_produtos(self.produtos.listar())

    def salvar_vendas(self):
        self.persistencia.salvar_vendas(self.vendas.listar())