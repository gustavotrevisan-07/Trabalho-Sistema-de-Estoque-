def ordenar_produtos_por_id(produtos):
    produtos_ordenados = list(produtos)

    for i in range(1, len(produtos_ordenados)):
        produto_atual = produtos_ordenados[i]
        j = i - 1

        while j >= 0 and produtos_ordenados[j].codigo > produto_atual.codigo:
            produtos_ordenados[j + 1] = produtos_ordenados[j]
            j -= 1

        produtos_ordenados[j + 1] = produto_atual

    return produtos_ordenados
