**Projeto de implementação do DesafioUBC - link do repo:https://github.com/joaomarcelo81/DesafioUBC/tree/main**

**Descrição**
O desafio tem o intuito de através um dataset, chamar um script python para formatar esse dataset e fazer o envio para o Apache Solr

**Como rodar o projeto**
Temos duas maneiras de fazer isso, abaixo estará especificado.
- **Rodar tudo no terminal**
  1. Primeiro temos que criar uma instância do Solr no Docker:
  ```bash
  docker run -d -p 8983:8983 --name solr_instance -t solr
  ```

  2. Depois tem que criar o core que irá armazenar os dados:
  ```bash
  docker exec solr_instance solr create_core -c students
  ```

  3. Agora temos que instalar as dependências dos pacotes python:
  ```bash
  pip install -r requirements.txt
  ```

  4. E por último rodar o script python:
  ```bash
  python Scripts/script.py
  ```

- **Rodar pelo Docker-compose**
  1. Basta executar o seguinte comando para criar a instância e já rodar o script:
  ```bash
  docker compose up -d --build
  ```

  Obs: Pelo Docker compose está sendo criado um bind para uma pasta chama SolrData para não haver perca dos dados quando a instância for derrubada.