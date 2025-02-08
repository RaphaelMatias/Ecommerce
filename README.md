# Backend - E-commerce (Django)

Este repositório contém o backend de um projeto de e-commerce, construído com Django e Django Rest Framework (DRF). 
A aplicação oferece uma API RESTful para gerenciar produtos, pedidos, carrinho de compras e autenticação de usuários.

O objetivo deste projeto é servir como um exercício de aprendizado contínuo, focando em boas práticas de desenvolvimento e arquiteturas de APIs. 
Além de ser uma oportunidade para aprimorar minhas habilidades em Django e DRF,
o projeto também será utilizado como portfólio para demonstrar minha capacidade de trabalhar com backend em um contexto real.

## Índice
- [Configuração do Backend](#configuração-do-backend)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplo de Uso da API](#exemplo-de-uso-da-api)
- [Como Contribuir](#como-contribuir)

---

## Configuração do Backend

### 1. Clone o repositório:
```bash
git clone https://github.com/RaphaelMatias/Ecommerce.git
cd Ecommerce
```

### 2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Realize as migrações do banco de dados:
```bash
python manage.py migrate
```

### 5. Crie um superusuário para acessar o painel administrativo:
```bash
python manage.py createsuperuser
```

### 6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

A API estará disponível em http://127.0.0.1:8000/api/.

## Tecnologias
- Backend:
- Django
- Django Rest Framework (DRF)
- MySQL
- JWT (para autenticação)
- Bootstrap

## Estrutura do Projeto
O backend é composto pelos seguintes apps:
```
backend/ 
    │  
    ├── manage.py            # Utilitário de linha de comando do Django 
    ├── ecommerce/           # Pasta principal do projeto com configurações e URLs 
    │  ├── settings.py       # Configurações do Django 
    │  ├── urls.py           # URLs do projeto 
    │  └── wsgi.py           # Arquivo WSGI para o servidor
    ├── products/            # API de produtos (exibe, adiciona, edita e exclui produtos) 
    ├── cart/                # API do carrinho de compras (adiciona/remover itens) 
    ├── orders/              # API de pedidos (cria e lista pedidos) 
    ├── users/               # API de usuários (autenticação e gerenciamento de usuários) 
    └── requirements.txt     # Dependências do Python
```
    

## Exemplo de Uso da API
Aqui está um exemplo básico de como fazer uma requisição para listar produtos:

GET http://127.0.0.1:8000/api/products/

A resposta será um JSON com os dados dos produtos.

## Como Contribuir
1. Faça um fork deste repositório.
2. Crie uma branch para suas mudanças: git checkout -b minha-feature
3. Faça commit das suas alterações: git commit -m 'Adiciona nova feature'
4. Envie para o repositório remoto: git push origin minha-feature
5. Abra um Pull Request!

## Detalhamento dos Apps:

- products: Gerencia a exibição e manipulação dos produtos na loja (adicionar, editar, excluir).
- cart: Gerencia o carrinho de compras, permitindo adicionar e remover produtos.
- orders: Permite a criação de pedidos e visualização dos pedidos realizados.
- users: Gerencia o cadastro de usuários, autenticação via JWT e permissões para clientes e administradores.
