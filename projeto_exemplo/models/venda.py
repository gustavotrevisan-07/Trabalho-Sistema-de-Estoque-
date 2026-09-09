class Venda:
    def __init__(self, codigo, codigo_cliente, itens, valor_total=None):
        self.codigo = int(codigo)
        self.codigo_cliente = int(codigo_cliente)
        self.itens = itens

        if self.codigo <= 0:
            raise ValueError("O ID da venda deve ser maior que zero.")

        if self.codigo_cliente <= 0:
            raise ValueError("O ID do cliente deve ser maior que zero.")

        if len(self.itens) == 0:
            raise ValueError("A venda deve possuir pelo menos um item.")

        if valor_total is None:
            self.valor_total = self.calcular_total()
        else:
            self.valor_total = float(valor_total)

    def calcular_total(self):
        total = 0.0

        for item in self.itens:
            quantidade = int(item["quantidade"])
            preco = float(item["preco_unitario"])

            if quantidade <= 0 or preco <= 0:
                raise ValueError(
                    "Os itens da venda devem ter quantidade e preco positivos."
                )

            total += quantidade * preco

        return total

    def itens_para_texto(self):
        partes = []

        for item in self.itens:
            partes.append(
                f"{item['codigo_produto']}:{item['quantidade']}:"
                f"{item['preco_unitario']}"
            )

        return "|".join(partes)

    def to_csv_row(self):
        return [
            self.codigo,
            self.codigo_cliente,
            self.itens_para_texto(),
            self.valor_total,
        ]

    def __str__(self):
        return (
            f"Venda {self.codigo} | Cliente {self.codigo_cliente} | "
            f"Total R$ {self.valor_total:.2f}"
        )


def itens_de_texto(texto):
    itens = []

    if texto.strip() == "":
        return itens

    for parte in texto.split("|"):
        codigo_produto, quantidade, preco_unitario = parte.split(":")

        itens.append(
            {
                "codigo_produto": int(codigo_produto),
                "quantidade": int(quantidade),
                "preco_unitario": float(preco_unitario),
            }
        )

    return itens


def venda_from_csv_row(row):
    return Venda(
        row["codigo"],
        row["codigo_cliente"],
        itens_de_texto(row["itens"]),
        row["valor_total"],
    )