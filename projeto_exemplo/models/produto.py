class Produto:
    def __init__(self, codigo, nome, preco, quantidade):
        self.codigo = int(codigo)
        self.nome = nome.strip()
        self.preco = float(preco)
        self.quantidade = int(quantidade)

        if self.codigo <= 0:
            raise ValueError("O ID do produto deve ser maior que zero.")

        if self.nome == "":
            raise ValueError("O nome do produto e obrigatorio.")

        if self.preco <= 0:
            raise ValueError("O preco do produto deve ser maior que zero.")

        if self.quantidade < 0:
            raise ValueError("A quantidade nao pode ser negativa.")

    def get_identificador_unico(self):
        return self.codigo

    def atualizar_estoque(self, nova_quantidade):
        pass

    def to_csv_row(self):
        return [self.codigo, self.nome, self.preco, self.quantidade]

    def __str__(self):
        preco_formatado = f"{self.preco:.2f}"
        return f"Produto {self.codigo} - {self.nome} | R$ {preco_formatado} | Estoque: {self.quantidade}"

def produto_from_csv_row(row):
    return Produto(row["codigo"], row["nome"], row["preco"], row["quantidade"])
