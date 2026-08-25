import csv
import os

from models.cliente import cliente_from_csv_row
from models.produto import produto_from_csv_row
from models.venda import venda_from_csv_row

class PersistenciaService:
    def __init__(self, pasta_data):
        self.pasta_data = pasta_data
        self.arquivo_clientes = os.path.join(pasta_data, "clientes.csv")
        self.arquivo_produtos = os.path.join(pasta_data, "produtos.csv")
        self.arquivo_vendas = os.path.join(pasta_data, "vendas.csv")
        self.garantir_arquivos()

    def garantir_arquivos(self):
        os.makedirs(self.pasta_data, exist_ok=True)
        self._garantir_csv(self.arquivo_clientes, ["codigo", "nome"])
        self._garantir_csv(self.arquivo_produtos, ["codigo", "nome", "preco", "quantidade"])
        self._garantir_csv(
            self.arquivo_vendas,
            ["codigo", "codigo_cliente", "itens", "valor_total"],
        )

    def _garantir_csv(self, caminho, cabecalho):
        if os.path.exists(caminho) and os.path.getsize(caminho) > 0:
            return

        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)

    def carregar_clientes(self):
        return self._carregar(self.arquivo_clientes, cliente_from_csv_row)

    def carregar_produtos(self):
        return self._carregar(self.arquivo_produtos, produto_from_csv_row)

    def carregar_vendas(self):
        return self._carregar(self.arquivo_vendas, venda_from_csv_row)

    def _carregar(self, caminho, construtor):
        registros = []

        try:
            with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.DictReader(arquivo)

                for row in leitor:
                    try:
                        registros.append(construtor(row))
                    except (KeyError, TypeError, ValueError):
                        print(f"Aviso: uma linha invalida foi ignorada em {caminho}.")
        except FileNotFoundError:
            self.garantir_arquivos()

        return registros

    def salvar_clientes(self, clientes):
        self._salvar(
            self.arquivo_clientes,
            ["codigo", "nome"],
            clientes,
        )

    def salvar_produtos(self, produtos):
        self._salvar(
            self.arquivo_produtos,
            ["codigo", "nome", "preco", "quantidade"],
            produtos,
        )

    def salvar_vendas(self, vendas):
        self._salvar(
            self.arquivo_vendas,
            ["codigo", "codigo_cliente", "itens", "valor_total"],
            vendas,
        )

    def _salvar(self, caminho, cabecalho, registros):
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)

            for registro in registros:
                escritor.writerow(registro.to_csv_row())
