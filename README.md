# Sistema de Estoque e Vendas - Mercado de Bairro

Projeto desenvolvido para o trabalho avaliativo de Estruturas de Dados. O sistema simula o controle de clientes, produtos, estoque e vendas de um pequeno mercado de bairro, utilizando Python e arquivos CSV como persistencia dos dados.

## Funcionalidades

- Cadastro, listagem, busca e remocao de clientes.
- Cadastro, listagem, busca e remocao de produtos.
- Atualizacao de quantidade em estoque.
- Listagem de produtos na ordem normal, inversa e ordenada por codigo.
- Busca de produto por Busca Binaria.
- Registro de venda simples com validacao de cliente, produto e estoque disponivel.
- Baixa automatica da quantidade vendida.
- Fila de vendas, mostrando as vendas na ordem em que foram realizadas.
- Relatorios de valor total do estoque, total de vendas, gastos por cliente, cliente que mais gastou e produto mais vendido.
- Desfazer a ultima operacao realizada durante a execucao.
- Salvamento automatico nos arquivos CSV apos cada alteracao valida.

## Tecnologias

- Python 3
- Apenas bibliotecas padrao do Python
- Execucao pelo terminal

## Como executar

Abra o terminal dentro da pasta `projeto_exemplo` e execute:

```bash
python main.py