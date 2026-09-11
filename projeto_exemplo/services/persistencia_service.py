import csv
from pathlib import Path
from typing import Callable, List, Any

from models.cliente import cliente_from_csv_row
from models.produto import produto_from_csv_row
from models.venda import venda_from_csv_row

class PersistenciaService:
    CABECALHO_CLIENTES = ["codigo", "nome"]
    CABECALHO_PRODUTOS = ["codigo", "nome", "preco", "quantidade"]
    CABECALHO_VENDAS = ["codigo", "codigo_cliente", "itens", "valor_total"]

    def __init__(self, pasta_data: str | Path):
        self.pasta_data = Path(pasta_data)
        self.arquivo_clientes = self.pasta_data / "clientes.csv"
        self.arquivo_produtos = self.pasta_data / "produtos.csv"
        self.arquivo_vendas = self.pasta_data / "vendas.csv"
        self.garantir_arquivos()

    def garantir_arquivos(self) -> None:
        self.pasta_data.mkdir(parents=True, exist_ok=True)
        self._garantir_csv(self.arquivo_clientes, self.CABECALHO_CLIENTES)
        self._garantir_csv(self.arquivo_produtos, self.CABECALHO_PRODUTOS)
        self._garantir_csv(self.arquivo_vendas, self.CABECALHO_VENDAS)

    def _garantir_csv(self, caminho: Path, cabecalho: List[str]) -> None:
        if caminho.exists() and caminho.stat().st_size > 0:
            return

        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)

    def carregar_clientes(self) -> List[Any]:
        return self._carregar(self.arquivo_clientes, cliente_from_csv_row)

    def carregar_produtos(self) -> List[Any]:
        return self._carregar(self.arquivo_produtos, produto_from_csv_row)

    def carregar_vendas(self) -> List[Any]:
        return self._carregar(self.arquivo_vendas, venda_from_csv_row)

    def _carregar(self, caminho: Path, construtor: Callable[[dict], Any]) -> List[Any]:
        registros = []

        try:
            with open(caminho, "r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.DictReader(arquivo)

                for num_linha, row in enumerate(leitor, start=2):
                    try:
                        registros.append(construtor(row))
                    except (KeyError, TypeError, ValueError) as erro:
                        print(f"Aviso: linha {num_linha} invalida ignorada em '{caminho.name}': {erro}")
        except FileNotFoundError:
            self.garantir_arquivos()

        return registros

    def salvar_clientes(self, clientes: List[Any]) -> None:
        self._salvar(self.arquivo_clientes, self.CABECALHO_CLIENTES, clientes)

    def salvar_produtos(self, produtos: List[Any]) -> None:
        self._salvar(self.arquivo_produtos, self.CABECALHO_PRODUTOS, produtos)

    def salvar_vendas(self, vendas: List[Any]) -> None:
        self._salvar(self.arquivo_vendas, self.CABECALHO_VENDAS, vendas)

    def _salvar(self, caminho: Path, cabecalho: List[str], registros: List[Any]) -> None:
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)

            for registro in registros:
                escritor.writerow(registro.to_csv_row())