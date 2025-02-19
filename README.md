# Conferir Débito

Este projeto é uma ferramenta automatizada para consultar dados de clientes em dois sistemas diferentes: ERP e Conta Azul. Ele utiliza a biblioteca Playwright para automatizar a navegação e extração de dados das páginas web.

## Funcionalidades

- Fazer login no ERP e Conta Azul.
- Consultar dados de clientes no ERP.
- Verificar o status dos clientes no ERP.
- Consultar dados de clientes no Conta Azul.
- Salvar os resultados em um arquivo CSV.

## Requisitos

- Python 3.6 ou superior
- Poetry

## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/seu_usuario/conferir-debito.git
   cd conferir-debito
   ```

2. Crie um ambiente virtual e ative-o
    ```
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale o Poetry se ainda não estiver instalado:
    ```
    pip install poetry
    ```

4. Instale as dependências do projeto:
     ```
    poetry install
    ```
5. Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis de ambiente:
    ```
    ERP_USERNAME="seu_usuario_erp"
    ERP_PASSWORD="sua_senha_erp"
    CONTA_AZUL_USERNAME="seu_usuario_conta_azul"
    CONTA_AZUL_PASSWORD="sua_senha_conta_azul"
    ```

6. Crie um arquivo cpf.txt na raiz do projeto e adicione os CPFs a serem consultados, um CPF por linha. Exemplo:
    ```
    12345678900
    09876543211
    ```

7. Crie um arquivo update-endereco.csv na raiz do projeto. Este arquivo será usado para salvar os resultados. Você pode deixá-lo vazio inicialmente.

8. Para executar o script, use o seguinte comando:
    ```
    poetry run pytest
    poetry run python conferir_debito_play.py
    ```

## Estrutura do Projeto
Certifique-se de que a estrutura do seu projeto esteja organizada da seguinte forma:

Conferir-Debito/
├── .env
├── .gitignore
├── conferir_debito_play.py
├── cpf.txt
├── update-endereco.csv
├── test_conferir_debito.py
└── README.md