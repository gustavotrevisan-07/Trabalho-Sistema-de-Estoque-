# Projeto Exemplo - Sistema de Estoque e Vendas

Este projeto e uma base de estudo para o trabalho avaliativo de Estrutura de Dados.
Ele nao e uma solucao pronta. A ideia e mostrar uma organizacao inicial do codigo,
deixar alguns arquivos importantes encaminhados e indicar onde os grupos devem completar
as regras do sistema.

O projeto usa Python puro e execucao pelo terminal.

## O que este projeto entrega

- arvore de pastas organizada;
- classes principais do dominio: `Cliente`, `Produto` e `Venda`;
- estruturas de dados separadas em arquivos proprios;
- persistencia em arquivos CSV;
- dados iniciais cadastrados em `data/`;
- contrato dos arquivos de banco;
- geracao de codigo sequencial;
- menu numerico com as opcoes esperadas no trabalho;
- metodos no `EstoqueService` preparados como ponto de partida.

## O que os alunos devem completar

O arquivo `services/estoque_service.py` esta propositalmente incompleto em varias
funcionalidades. Os metodos com `pass` indicam pontos que os grupos devem implementar.

Devem ser completados, entre outros:

- cadastro, listagem, busca, remocao e atualizacao usando as estruturas;
- regra completa de venda;
- venda com um ou mais produtos;
- baixa de estoque;
- insercao das vendas na Fila;
- uso da Pilha para desfazer operacoes;
- relatorios de estoque, vendas, cliente que mais gastou e produto mais vendido;
- salvamento automatico depois de cada alteracao valida.

## Como executar

Entre na pasta do projeto:

```bash
cd projeto_exemplo
```

Execute:

```bash
python3 main.py
```

O menu ja possui as opcoes do trabalho. Algumas opcoes podem nao funcionar totalmente
enquanto o `EstoqueService` nao for completado.

## Organizacao dos arquivos

```text
projeto_exemplo/
├── main.py
├── models/
│   ├── cliente.py
│   ├── produto.py
│   └── venda.py
├── estruturas/
│   ├── nodo.py
│   ├── dnodo.py
│   ├── lse.py
│   ├── lde.py
│   ├── fila.py
│   └── pilha.py
├── algoritmos/
│   ├── ordenacao.py
│   └── busca_binaria.py
├── services/
│   ├── estoque_service.py
│   └── persistencia_service.py
├── data/
│   ├── clientes.csv
│   ├── produtos.csv
│   └── vendas.csv
└── README.md
```

- `main.py`: contem o menu de terminal e chama os metodos do service.
- `models/`: contem as classes que representam os dados principais do sistema.
- `estruturas/`: contem as implementacoes das estruturas obrigatorias.
- `algoritmos/`: contem ordenacao manual e busca binaria.
- `services/`: contem a persistencia pronta e o service principal a completar.
- `data/`: contem os arquivos CSV que simulam o banco de dados.

## Estruturas de dados

As estruturas obrigatorias aparecem em `estruturas/`:

- `LSE`: deve armazenar os clientes.
- `LDE`: deve armazenar os produtos.
- `Fila`: deve armazenar as vendas na ordem em que aconteceram.
- `Pilha`: deve armazenar o historico usado para desfazer operacoes.

As listas nativas do Python podem aparecer como apoio, por exemplo para converter uma
estrutura antes de salvar em CSV ou antes de ordenar. Elas nao devem substituir as
estruturas obrigatorias.

## Codigos sequenciais

Os codigos de clientes, produtos e vendas devem ser sequenciais, iniciando em `1`.

O `EstoqueService` ja possui estes metodos de apoio:

```python
gerar_proximo_codigo_cliente()
gerar_proximo_codigo_produto()
gerar_proximo_codigo_venda()
```

Eles usam a mesma ideia: percorrem os registros ja carregados, encontram o maior codigo
existente e retornam o proximo numero.

Exemplo:

```text
maior codigo atual: 10
proximo codigo: 11
```

Assim, o usuario nao precisa digitar ID ao cadastrar um novo cliente, produto ou venda.

## Persistencia em CSV

A persistencia fica em `services/persistencia_service.py`.

Esse arquivo ja esta implementado e faz quatro tarefas principais:

- cria os CSVs se eles nao existirem;
- carrega clientes, produtos e vendas ao iniciar;
- transforma linhas do CSV em objetos Python;
- salva listas de objetos de volta nos arquivos.

Os arquivos ficam na pasta `data/`:

- `clientes.csv`
- `produtos.csv`
- `vendas.csv`

Se uma linha invalida for encontrada, o sistema mostra um aviso e continua executando.
Isso evita que um dado errado derrube todo o programa.

## Contrato dos arquivos CSV

Contrato significa: quais colunas cada arquivo precisa ter, em qual ordem elas aparecem
e que tipo de dado o sistema espera encontrar em cada coluna.

Todos os arquivos usam:

- primeira linha como cabecalho;
- virgula `,` como separador de colunas;
- uma linha para cada registro;
- numeros decimais com ponto, por exemplo `18.9`, e nao `18,9`.

### `clientes.csv`

Guarda os clientes.

```csv
codigo,nome
1,Ana Silva
```

| Coluna   | Tipo esperado | Regra                             |
| -------- | ------------- | --------------------------------- |
| `codigo` | inteiro       | sequencial, maior que zero        |
| `nome`   | texto         | obrigatorio, nao pode ficar vazio |

Ao carregar esse arquivo, cada linha valida deve virar um objeto `Cliente` e entrar na
`LSE`.

### `produtos.csv`

Guarda os produtos.

```csv
codigo,nome,preco,quantidade
1,Caneta azul,2.5,48
```

| Coluna       | Tipo esperado | Regra                             |
| ------------ | ------------- | --------------------------------- |
| `codigo`     | inteiro       | sequencial, maior que zero        |
| `nome`       | texto         | obrigatorio, nao pode ficar vazio |
| `preco`      | decimal       | deve ser maior que zero           |
| `quantidade` | inteiro       | deve ser zero ou maior            |

Ao carregar esse arquivo, cada linha valida deve virar um objeto `Produto` e entrar na
`LDE`.

### `vendas.csv`

Guarda as vendas.

```csv
codigo,codigo_cliente,itens,valor_total
1,1,1:2:2.5,5.0
2,2,2:1:18.9|4:3:1.2,22.5
```

| Coluna           | Tipo esperado     | Regra                                   |
| ---------------- | ----------------- | --------------------------------------- |
| `codigo`         | inteiro           | sequencial, maior que zero              |
| `codigo_cliente` | inteiro           | codigo do cliente da venda              |
| `itens`          | texto estruturado | produtos, quantidades e precos da venda |
| `valor_total`    | decimal           | total da venda                          |

O campo `itens` usa este formato:

```text
codigo_produto:quantidade:preco_unitario
```

Quando a venda possui mais de um produto, os itens ficam separados por `|`:

```text
2:1:18.9|4:3:1.2
```

Esse exemplo significa:

- produto `2`, quantidade `1`, preco unitario `18.9`;
- produto `4`, quantidade `3`, preco unitario `1.2`.

Ao carregar esse arquivo, cada linha valida deve virar um objeto `Venda` e entrar na
`Fila`.

## Algoritmos

O arquivo `algoritmos/ordenacao.py` implementa Insertion Sort para ordenar produtos por
ID, sem usar `sort()` ou `sorted()`.

O arquivo `algoritmos/busca_binaria.py` implementa Busca Binaria para localizar um
produto por ID depois que a colecao auxiliar estiver ordenada.

A `LDE` continua sendo a estrutura principal dos produtos. A colecao auxiliar serve
apenas para ordenar e buscar.

## Menu esperado

O menu do `main.py` ja apresenta as opcoes do trabalho:

```text
1  - Cadastrar cliente
2  - Listar clientes
3  - Buscar cliente
4  - Remover cliente
5  - Cadastrar produto
6  - Listar produtos
7  - Buscar produto
8  - Atualizar estoque
9  - Remover produto
10 - Listar produtos em ordem inversa
11 - Listar produtos ordenados por ID
12 - Buscar produto por ID usando Busca Binaria
13 - Realizar venda simples de exemplo
14 - Visualizar fila de vendas
15 - Visualizar primeira venda da fila
16 - Exibir valor total do estoque
17 - Exibir valor total das vendas
18 - Exibir clientes e valores totais gastos
19 - Exibir cliente que mais gastou
20 - Exibir produto mais vendido
21 - Desfazer ultima operacao
0  - Sair
```

O menu e apenas a entrada do sistema. A regra de cada opcao deve ficar organizada no
`EstoqueService`.

## Testes manuais recomendados

- iniciar o programa com os arquivos CSV ja preenchidos;
- listar clientes, produtos e vendas;
- cadastrar novo cliente e confirmar codigo sequencial;
- cadastrar novo produto e confirmar codigo sequencial;
- buscar cliente existente e inexistente;
- buscar produto existente e inexistente;
- tentar preco zero ou negativo;
- tentar quantidade negativa;
- ordenar produtos por ID;
- buscar produto por ID usando Busca Binaria;
- realizar venda valida;
- tentar venda com estoque insuficiente;
- reiniciar o programa e conferir se os dados foram carregados;
- testar desfazer com Pilha vazia;
- conferir se os arquivos CSV foram atualizados corretamente.
