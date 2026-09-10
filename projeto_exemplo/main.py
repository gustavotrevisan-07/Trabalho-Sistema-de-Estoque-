from services.estoque_service import EstoqueService

def ler_inteiro(mensagem):
    valor = input(mensagem)
    return int(valor)

def ler_float(mensagem):
    valor = input(mensagem).replace(",", ".")
    return float(valor)

def pausar():
    input("\nPressione ENTER para continuar...")

def imprimir_registros(registros, mensagem_vazia):
    if len(registros) == 0:
        print(mensagem_vazia)
        return

    for registro in registros:
        print(registro)

def mostrar_menu():
    print("\n==============================")
    print("SISTEMA DE ESTOQUE E VENDAS")
    print("==============================")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Buscar cliente")
    print("4 - Remover cliente")
    print("5 - Cadastrar produto")
    print("6 - Listar produtos")
    print("7 - Buscar produto")
    print("8 - Atualizar estoque")
    print("9 - Remover produto")
    print("10 - Listar produtos em ordem inversa")
    print("11 - Listar produtos ordenados por ID")
    print("12 - Buscar produto por ID usando Busca Binaria")
    print("13 - Realizar venda simples de exemplo")
    print("14 - Visualizar fila de vendas")
    print("15 - Visualizar primeira venda da fila")
    print("16 - Exibir valor total do estoque")
    print("17 - Exibir valor total das vendas")
    print("18 - Exibir clientes e valores totais gastos")
    print("19 - Exibir cliente que mais gastou")
    print("20 - Exibir produto mais vendido")
    print("21 - Desfazer ultima operacao")
    print("0 - Sair")


def executar_opcao(opcao, service):
    if opcao == 1:
        nome = input("Nome do cliente: ")
        cliente = service.cadastrar_cliente(nome)
        print(f"Cliente cadastrado com sucesso: {cliente}")

    elif opcao == 2:
        imprimir_registros(service.listar_clientes(), "Nenhum cliente cadastrado.")

    elif opcao == 3:
        codigo = ler_inteiro("Codigo do cliente: ")
        cliente = service.buscar_cliente(codigo)
        if cliente:
            print(cliente)
        else:
            print("Cliente nao encontrado.")

    elif opcao == 4:
        codigo = ler_inteiro("Codigo do cliente a remover: ")
        cliente = service.remover_cliente(codigo)
        print(f"Cliente removido com sucesso: {cliente}")

    elif opcao == 5:
        nome = input("Nome do produto: ")
        preco = ler_float("Preco do produto: R$ ")
        quantidade = ler_inteiro("Quantidade inicial em estoque: ")
        produto = service.cadastrar_produto(nome, preco, quantidade)
        print(f"Produto cadastrado com sucesso: {produto}")

    elif opcao == 6:
        imprimir_registros(service.listar_produtos(), "Nenhum produto cadastrado.")

    elif opcao == 7:
        codigo = ler_inteiro("Codigo do produto: ")
        produto = service.buscar_produto(codigo)
        if produto:
            print(produto)
        else:
            print("Produto nao encontrado.")

    elif opcao == 8:
        codigo = ler_inteiro("Codigo do produto: ")
        nova_qtd = ler_inteiro("Nova quantidade em estoque: ")
        produto = service.atualizar_estoque(codigo, nova_qtd)
        print(f"Estoque atualizado: {produto}")

    elif opcao == 9:
        codigo = ler_inteiro("Codigo do produto a remover: ")
        produto = service.remover_produto(codigo)
        print(f"Produto removido com sucesso: {produto}")

    elif opcao == 10:
        imprimir_registros(service.listar_produtos_inverso(), "Nenhum produto cadastrado.")

    elif opcao == 11:
        imprimir_registros(service.listar_produtos_ordenados_por_id(), "Nenhum produto cadastrado.")

    elif opcao == 12:
        codigo = ler_inteiro("Codigo do produto (Busca Binaria): ")
        produto = service.buscar_produto_binario(codigo)
        if produto:
            print(produto)
        else:
            print("Produto nao encontrado.")

    elif opcao == 13:
        cod_cliente = ler_inteiro("Codigo do cliente: ")
        cod_produto = ler_inteiro("Codigo do produto: ")
        quantidade = ler_inteiro("Quantidade vendida: ")
        venda = service.realizar_venda_exemplo(cod_cliente, cod_produto, quantidade)
        print(f"Venda realizada com sucesso: {venda}")

    elif opcao == 14:
        imprimir_registros(service.listar_vendas(), "Nenhuma venda na fila.")

    elif opcao == 15:
        venda = service.primeira_venda()
        if venda:
            print(f"Primeira venda da fila: {venda}")
        else:
            print("Nenhuma venda na fila.")

    elif opcao == 16:
        total = service.valor_total_estoque()
        print(f"Valor total do estoque: R$ {total:.2f}")

    elif opcao == 17:
        total = service.valor_total_vendas()
        print(f"Valor total das vendas: R$ {total:.2f}")

    elif opcao == 18:
        totais = service.clientes_e_valores_totais_gastos()
        if not totais:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente, total in totais:
                print(f"Cliente: {cliente} | Total Gasto: R$ {total:.2f}")

    elif opcao == 19:
        resultado = service.cliente_que_mais_gastou()
        if resultado is None:
            print("Nenhum cliente ou venda registrada.")
        else:
            cliente, total = resultado
            print(f"Cliente que mais gastou: {cliente} | Total: R$ {total:.2f}")

    elif opcao == 20:
        resultado = service.produto_mais_vendido()
        if resultado is None:
            print("Nenhuma venda registrada.")
        else:
            produto, qtd = resultado
            print(f"Produto mais vendido: {produto} | Quantidade vendida: {qtd}")

    elif opcao == 21:
        mensagem = service.desfazer_ultima_operacao()
        print(mensagem)

    else:
        print("Opcao invalida. Tente novamente.")

def main():
    service = EstoqueService()

    while True:
        mostrar_menu()

        try:
            opcao = ler_inteiro("Escolha uma opcao: ")

            if opcao == 0:
                print("Sistema encerrado.")
                break

            executar_opcao(opcao, service)

        except ValueError as erro:
            print(f"Erro: {erro}")
        except IndexError as erro:
            print(f"Erro: {erro}")
        except NotImplementedError as erro:
            print(f"Funcionalidade para completar: {erro}")

        pausar()

if __name__ == "__main__":
    main()