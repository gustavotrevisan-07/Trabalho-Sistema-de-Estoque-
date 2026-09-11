class Fila:
    def __init__(self):
        self._lista_de_valores = []

    def enqueue(self, item):
        self._lista_de_valores.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Nao ha dados para remover da fila.")

        return self._lista_de_valores.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("Nao ha dados na fila.")

        return self._lista_de_valores[0]

    def remover_por_codigo(self, codigo):
        for indice, item in enumerate(self._lista_de_valores):
            if item.codigo == codigo:
                return self._lista_de_valores.pop (indice)

    def is_empty(self):
        return len(self._lista_de_valores) == 0

    def listar(self):
        return list(self._lista_de_valores)

    def __len__(self):
        return len(self._lista_de_valores)
