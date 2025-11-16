# Sistema de Gerenciamento de Estoque

Este é um sistema de console (CLI) para gerenciamento de estoque, desenvolvido em Python. Ele utiliza o **SQLite** para armazenamento de dados, **Pandas** para manipulação de dados e Matplotlib para visualização e geração de relatórios gráficos.



O sistema permite cadastrar produtos, controlar entradas e saídas, visualizar o estoque atual, excluir itens e analisar o histórico de movimentações, além de fornecer alertas visuais para produtos com estoque baixo.



#### Funcionalidades Principais

* **Cadastro de Produtos:** Adiciona novos itens ao banco de dados (Estoque e Movimentações).
* **Controle de Movimentação:** Registra entradas e saídas de itens, atualizando o estoque automaticamente.
* **Visualização de Estoque:** Lista todos os produtos, com destaque para itens com estoque baixo.
* **Busca de Itens:** Permite buscar produtos específicos por ID ou Nome.
* **Exclusão de Itens:** Remove um produto do estoque (e todo o seu histórico de movimentação).
* **Histórico de Movimentação:** Exibe todo o histórico de um produto (cadastro, entradas, saídas).
* **Alertas Automáticos:** Exibe um alerta no início do programa para todos os itens com 5 unidades ou menos.
* **Relatórios Gráficos:** Gera gráficos de pizza, barras e dispersão para análise do estoque.



#### Tecnologias e Dependências

O projeto foi construído com as seguintes tecnologias:



* **Python 3.x**
* **SQLite 3** (biblioteca nativa do Python sqlite3)
* **Pandas** (para processamento de dados e geração dos gráficos)
* **Matplotlib** (para plotagem dos gráficos)



#### **Instalação de Dependências**

Para executar este projeto, você precisará instalar as bibliotecas **pandas** e **matplotlib**.

`pip install pandas matplotlib`

### **Como Executar**
1. Clone este repositório:
    `git clone [URL_DO_SEU_REPOSITORIO]`
2. Navegue até o diretório do projeto:
    `cd [NOME_DA_PASTA]`
3. Instale as dependências (conforme a seção anterior).
4. Execute o script principal:
    `python nome_do_seu_arquivo.py`
5. O sistema será iniciado no seu console. O banco de dados **estoque.db** será criado automaticamente no mesmo diretório na primeira execução.

### **Estrutura do Banco de Dados**
O sistema utiliza um banco de dados SQLite (estoque.db) com duas tabelas principais:

1. Tabela estoque
Armazena os detalhes principais de cada item.

|Coluna   | Tipo | Descrição |
|:---: | :---: | :---: |
|id| INTEGER | Chave primária, autoincremento. |
|nome | TEXT | Nome do produto. |
|categoria | TEXT | Categoria do produto (ex: Limpeza, Alimentos). |
|valor_unit | REAL | Preço unitário do produto. |
|quantidade | INTEGER | Quantidade atual em estoque. |

**Nota**: A tabela **movimentos** usa `ON DELETE CASCADE`. Isso significa que, ao excluir um item da tabela **estoque**, todos os registros de movimentação associados a ele são automaticamente apagados.

### **Análise das Funções (Detalhes do Código)**
O código é estruturado em várias funções (**def**) que se comunicam com o banco de dados e um loop principal que serve como menu para o usuário.

-   `iniciar(conn, cursor)`
    -   **Função**: Inicializa o banco de dados.
    -   **O que faz**:
        1.  Cria a tabela **estoque** se não existir.
        2.  Cria a tabela **movimentos** se não existir, definindo a chave estrangeira (`FOREIGN KEY`) com `ON DELETE CASCADE`.

-   `cadastrar_item(conn, cursor, nome, categoria, valor_unit, quantidade)`
    -   **Função**: Adiciona um novo produto completo ao sistema.
    -   **O que faz**:
        1.  Insere o novo produto na tabela **estoque**.
        2.  Busca o **id** do produto recém-cadastrado.
        3.  Cria um registro inicial na tabela **movimentos** com o **tipo** "Cadastro", usando a data e hora atuais e a quantidade inicial.

-   `verificar_estoque(conn, cursor)`
    -   **Função**: Verifica se a tabela de estoque possui algum item.
    -   **O que faz**:
        1.  Conta o número total de linhas (`COUNT(*)`) na tabela **estoque**.
        2.  Retorna `0` se o estoque estiver vazio e `1` se houver itens.

-   `alerta_estoque(conn, cursor)`
    -   **Função**: Cria um alerta visual para produtos com estoque baixo.
    -   **O que faz**:
        1.  Utiliza `verificar_estoque` para checar se o estoque não está vazio.
        2.  Busca todos os produtos onde a **quantidade** é menor ou igual a **5**.
        3.  Imprime um **ALERTA** formatado para cada produto encontrado.

-   `visualizar_estoque(conn, cursor)`
    -   **Função**: Exibe todos os itens cadastrados no estoque.
    -   **O que faz**:
        1.  Exibe os produtos com estoque considerado "normal" (**quantidade >= 5**).
        2.  Separa e exibe em destaque os produtos com **ESTOQUE BAIXO** (**quantidade < 5**).

-   `buscar_item(conn, cursor, buscar)`
    -   **Função**: Localiza um item específico por nome ou ID.
    -   **O que faz**:
        1.  Executa uma consulta que busca na tabela **estoque** pelo `nome` OU `id`.
        2.  Imprime o produto encontrado.
        3.  Retorna o item (como `sqlite3.Row`) ou `None` se não for encontrado.

-   `movimentar_item(conn, cursor, buscar, opcao)`
    -   **Função**: Processa a entrada ou saída de unidades de um produto.
    -   **O que faz**:
        1.  Usa `buscar_item()` para identificar o produto.
        2.  Se `opcao == 1` (**Entrada**): Soma a quantidade ao estoque.
        3.  Se `opcao == 2` (**Saída**): Verifica se há estoque suficiente e subtrai a quantidade.
        4.  Atualiza a quantidade na tabela **estoque**.
        5.  Registra a transação (`Entrada` ou `Saída`) na tabela **movimentos**, com a quantidade movimentada e a quantidade final.

-   `excluir_item(conn, cursor, buscar)`
    -   **Função**: Remove um item permanentemente.
    -   **O que faz**:
        1.  Usa `buscar_item()` para encontrar o produto.
        2.  Solicita uma confirmação do usuário.
        3.  Se confirmado, executa `DELETE` na tabela **estoque**.
        4.  Graças ao `ON DELETE CASCADE` na definição da tabela, todos os registros de movimentação relacionados são excluídos automaticamente.

-   `buscar_registros(conn, cursor, buscar)`
    -   **Função**: Exibe todo o histórico de movimentação de um produto.
    -   **O que faz**:
        1.  Usa `buscar_item()` para obter o `id` do produto.
        2.  Busca e imprime todas as entradas da tabela **movimentos** onde o `item_id` corresponde ao produto.

-   `graficos(conn)`
    -   **Função**: Gera relatórios gráficos de análise do estoque.
    -   **O que faz**:
        1.  Apresenta um submenu para seleção de gráficos.
        2.  **Opção 1 (Pizza)**: Gera um gráfico do valor total em estoque por **categoria**.
        3.  **Opção 2 (Barras)**: Gera um gráfico da **quantidade** de cada **produto** em estoque.
        4.  **Opção 3 (Dispersão)**: Gera um gráfico de correlação entre a quantidade total e o valor total acumulado por produto.
        5.  Utiliza **Pandas** para ler os dados do SQL e **Matplotlib** para plotar as visualizações.

### **Loop Principal (Menu de Execução)**

O bloco de código final é responsável por iniciar o sistema, conectar-se ao banco de dados e controlar o fluxo de interação com o usuário.

-   **Conexão e Configuração**
    -   A conexão com o banco de dados (`estoque.db`) é estabelecida usando `sqlite3.connect()`.
    -   É configurado o `conn.row_factory = sqlite3.Row`, o que permite que os dados recuperados do banco sejam acessados como um dicionário (pelo nome da coluna, ex.: `produto['nome']`), e não apenas por índice.
    -   A função `iniciar(conn, cursor)` é chamada para garantir que as tabelas existam.

-   **Fluxo de Operação**
    -   O programa entra em um loop infinito (`while True`).
    -   A função `alerta_estoque()` é chamada a **cada ciclo do loop**, garantindo que o usuário seja alertado imediatamente sobre itens com baixo estoque.
    -   O **menu principal** é exibido, permitindo que o usuário escolha a operação (1 a 8).
    -   Cada escolha válida (1 a 7) invoca a função correspondente, solicitando as entradas necessárias (nome, ID, quantidade, etc.).
    -   Há tratamento de erros básico (`try...except ValueError`) para garantir que o usuário digite números inteiros ou flutuantes quando necessário.

-   **Opções de Saída**
    -   Ao escolher a opção **8 (Sair do sistema)**, a conexão com o banco de dados é encerrada (`conn.close()`) e o loop é interrompido, finalizando o script.
