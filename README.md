# McField's Soluções Agrícolas

## Projeto de website para publicação de conteúdos relacionados à Agronomia

[![Static Badge](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Static Badge](https://img.shields.io/badge/Django-5.0.2-green)](https://www.djangoproject.com/)
[![codecov](https://codecov.io/gh/fczanetti/mcfields/graph/badge.svg?token=XiQdJaQNse)](https://codecov.io/gh/fczanetti/mcfields)

Este projeto foi desenvolvido no sistema operacional Linux, através do Windows Subsystem for Linux (WSL).


## Instalação

O gerenciamento das dependências foi feito através do PIPENV. Para instalar as dependências necessárias devem ser
utilizados os seguintes comandos no terminal:

Criação do ambiente virtual e instalação das dependências listadas no Pipfile:
  - pipenv install

Caso o ambiente virtual não seja ativado automaticamente após o comando 'pipenv install', devemos ativá-lo através do
seguinte comando:
  - pipenv shell

O banco de dados utilizado localmente foi uma imagem do PostgreSQL configurado através do arquivo docker-compose.yml
que se encontra na pasta do projeto. Para utilizá-lo será necessário ter o Docker instalado. Após instalado, deve ser
executado o seguinte comando no terminal para que o banco de dados seja criado e entre em execução:
  - docker compose up -d

Para que o Django reconheça e se conecte com o banco de dados criado devemos criar um arquivo chamado .env e inserir
a variável de ambiente DATABASE_URL no formato mostrado a seguir. Note que os valores POSTGRES_USER, POSTGRES_PASSWORD,
PORT e POSTGRES_DB devem ser substituídos com os valores definidos no arquivo docker-compose.yml para que a conexão com
o banco aconteça com sucesso.
  - DATABASE_URL = postgres://POSTGRES_USER:POSTGRES_PASSWORD@localhost:PORT/POSTGRES_DB

Atentar que no arquivo 'env-sample' que se encontra dentro da pasta 'contrib' existe também uma variável de ambiente
DATABASE_URL, e esta não deve ser alterada pois é utilizada no funcionamento da integração contínua (GitHub Actions).

Devem ser definidas as seguintes variáveis de ambiente no arquivo .env:

  - DEBUG=True
  - SECRET_KEY=secret
  - CSRF_TRUSTED_ORIGINS= (esta não precisa ter um valor)


## Monitoramento de erros com Sentry SDK

Para funcionamento do monitoramento de erros através da plataforma Sentry SDK uma conta deve ser criada na plataforma.
Após a criação deve ser criado um projeto Django nesta conta, e a variável de nome 'dsn' fornecida no momento da criação
do projeto deve ser inserida no arquivo .env da seguinte forma:

  - SENTRY_DSN = valor-da-variavel-dsn


## Configurações arquivos estáticos

Este projeto foi pré configurado para enviar os arquivos estáticos e arquivos de mídia para Buckets S3 da AWS. Para
utilizar este recurso os seguintes passos devem ser seguidos:
- criar um usuário IAM na plataforma AWS e anexar a este uma política de permissão chamada AmazonS3FullAccess;
- criar uma secret key para este usuário. A secret key terá um ID e seu real valor, ambos serão utilizados;
- criar um bucket S3 para arquivos estáticos e anexar uma política de permissão que permita ao usuário IAM a ação
'PutObject' no bucket e em todas as suas pastas;
- criar outro bucket S3, agora para arquívos de mídia. Este ter a configuração 'Block all public access' desativada,
já que armazenará arquivos que deverão ser visíveis a quem acessar o site. Além desta configuração, a política de
acesso deverá permitir ao usuário IAM a ação 'PutObject' no bucket (e mais alguma outra se necessário), além de
conceder a todos (*) a ação 'GetObject' para o bucket e todas as suas pastas.
Após executadas as etapas listadas, podemos definir as variáveis de ambiente no arquivo .env da seguinte forma:

  - AWS_ACCESS_KEY_ID = valor-do-id-da-secret-key
  - AWS_SECRET_ACCESS_KEY = valor-da-secret-key (atentar que só pode ser visualizado uma vez pela plataforma AWS)
  - AWS_STORAGE_BUCKET_NAME = nome-do-bucket-S3-criado
  - AWS_STORAGE_BUCKET_NAME_MEDIA = nome-do-bucket-de-arquivos-de-midia

Feitas as configurações, ao rodar o comando 'python manage.py collectstatic', os arquivos estáticos serão enviados para
o bucket criado na AWS. Caso os valores das variáveis da AWS não sejam preenchidos, os arquivos estáticos serão copiados
para uma pasta chamada 'staticfiles' na pasta principal do projeto (configuração STATIC_ROOT no arquivo settings.py).


## Integração com SendGrid

Foi criada neste projeto uma integração com a plataforma de envio de emails SendGrid. Este recurso permite que emails
sejam enviados a pessoas cadastradas sempre que postarmos algum conteúdo (Single Sends). Para seu correto funcionamento
será necessário seguir as seguintes etapas:
- criar uma conta na plataforma SendGrid e acessá-la;
- na plataforma SendGrid, acessar a seção de 'API Keys' e criar uma chave;
- na plataforma SendGrid, na seção 'Marketing', acessar 'Contacts', criar uma lista e acessar. O ID desta lista estará
na URL, e devemos salvá-lo;
- na plataforma SendGrid, na seção Marketing, acessar 'Unsubscribe Groups' e criar um grupo. Este grupo será utilizado
para armazenar contatos que se descadastraram de nosso sistema de envio de emails. Na página de criação do grupo veremos
nosso grupo criado, e devemos salvar seu ID que estará a mostra.
- na plataforma SendGrid devemos fazer a verificação e autenticação do email utilizado como emissor. Após feita esta
verificação, consultar Settings > Sender Authentication > clicar no domínio de email verificado e clicar em editar. Na
URL aparecerá o ID deste emissor (Sender), devemos salvar este valor;
- Por último, ainda na plataforma SendGrid, devemos criar um 'Email Design' na seção 'Design Library'. Este design criado
também possuirá um ID listado em sua URL que devemos salvar;
- Após concluídas estas etapas devemos definir as seguintes variáveis de ambiente no arquivo .env:

  - SENDGRID_API_KEY = chave-api-criada-na-plataforma
  - SENDGRID_NEWSLETTER_LIST_ID = id-da-lista-de-email-criada
  - NEWSLETTER_SUPPRESSION_GROUP_ID = id-do-grupo-de-subscricao-criado (Unsubscribe Groups)
  - SENDER_ID = id-do-email-emissor-verificado
  - SENDGRID_NEWSLETTER_DESIGN_ID = id-do-design-de-email-criado

As variáveis listadas acima deverão ser cadastradas apenas em caso de uso do sistema de email. Porém, caso não seja
utilizado, no momento da publicação de algum conteúdo, sempre que tiver a opção 'Criar rascunho de email', esta deve ser
marcada como 'Não', caso contrário ocorrerá erro ao publicar por não ter as variáveis definidas. Caso alguma variável
seja definida incorretamente ou não seja definida também poderão ocorrer erros ao publicar.
