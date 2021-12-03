# gerenciamento-rural

Desenvolvimento de aplicação Flask para gerência de pequenas propriedades rurais.

## Dependências
O projeto depende de ambiente virtualizado em pipenv.
* Execute os códigos para instalação e verificação do pipenv:
  ```
  pip install pipenv
  pipenv --version
  ```
* Crie seu ambiente virtual e entre nele:
  ```
  pipenv --three
  pipenv shell
  ```
* Em seu terminal de preferência execute:
  ```
  pipenv install
  ```

* Realize as migrações de banco de dados:
  ```
  flask db init
  flask db migrate
  flask db upgrade
  ```

* Execute o projeto
