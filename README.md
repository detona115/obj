[![GitHub license](https://img.shields.io/badge/implemented%20by-Andy-blue)](https://www.linkedin.com/in/andy-kiaka-76a983110/)
# obj

### Pré-requisitos 📋

Ter a versão mais recente do docker e docker compose instalado
no computador a ser usado ou saber usar ambientes viruais com python

### Instalação e Execução 🔧

#### Após baixar , descompactar e acessar a pasta com os arquivos

N.B: Esta versão foi testada somente com Ubuntu, e deve funcionar perfeitamente em qualquer ambiente linux

- Escolhe uma das formas de executção

#### Executar no docker compose

- Em um terminal, execute o seguinte comando para construir as imagens e os containers   
- Antes da execução é necessário ter a porta 8000 desocupadas no computador para que o serviço possa funcionar e se comunicar normalmente.

```
docker-compose up --build
```

#### Executar sem docker

- Após descompactar ou clonar o projeto, crie e ative um ambiente virtual com a ferramenta da sua escolha.
- Instale as dependencias que estão no arquivo requirements.txt
- Em um terminal execute os seguintes comandos
```
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Arquitetura e Serviços
O sistema é composto de 1 serviço cujo,
1 api web com django e um banco de dados Sqlite

### Endpoints e utilidade

#### web_api
``` 
GET http://localhost:8000/conta?id=<int>
```
- Retorna a conta solicitada e o saldo
- Caso não for enncontrado retorna 404

```
POST localhost:8000/transacao

Payload: JSON {"forma_pagamento":"D", "conta_id": "1234", "valor":10}
```
- Efetua transações correspondente ao paramêtro 'forma_pagamento'
- Opções disponíveis: 'P' , 'C' e 'D'

## Autor ✒️

* **Andy Kiaka** - *Job Completo* - [detona115](https://github.com/detona115)

