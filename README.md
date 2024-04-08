# McField's Soluções Agrícolas

## Projeto de website para publicação de conteúdos relacionados à Agronomia

[![Static Badge](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Static Badge](https://img.shields.io/badge/Django-5.0.3-green)](https://www.djangoproject.com/)
[![codecov](https://codecov.io/gh/fczanetti/mcfields/graph/badge.svg?token=XiQdJaQNse)](https://codecov.io/gh/fczanetti/mcfields)

Este projeto foi desenvolvido no sistema operacional Linux, através do Windows Subsystem for Linux (WSL).


# Conteúdo

- [Instalação](https://github.com/fczanetti/mcfields?tab=readme-ov-file#instala%C3%A7%C3%A3o)
- [Monitoramento de erros com Sentry SDK](https://github.com/fczanetti/mcfields?tab=readme-ov-file#monitoramento-de-erros-com-sentry-sdk)
- [Configurações arquivos estáticos](https://github.com/fczanetti/mcfields?tab=readme-ov-file#configura%C3%A7%C3%B5es-arquivos-est%C3%A1ticos)
- [Integração com SendGrid](https://github.com/fczanetti/mcfields?tab=readme-ov-file#integra%C3%A7%C3%A3o-com-sendgrid)
- [Modelos](https://github.com/fczanetti/mcfields?tab=readme-ov-file#modelos)
- [Permissões](https://github.com/fczanetti/mcfields?tab=readme-ov-file#permiss%C3%B5es)


## Instalação

Este projeto foi configurado para que possa ser instalado de duas maneiras, com o aplicativo (backend e frontend) em
um conteiner Docker e o banco de dados PostgreSQL em outro, ou então com apenas o banco de dados em conteiner.

### Para instalar com o aplicativo e banco de dados em conteiners deve-se seguir os seguintes passos:

  - clonar o projeto;
  - criar um arquivo chamado .env na raiz do projeto;
  - copiar todo o conteúdo do arquivo env-sample, que se encontra na pasta 'contrib', para dentro do arquivo .env;
  - definir um valor para a variável POSTGRES_DB (nome do banco de dados);
  - definir um valor para a variável POSTGRES_USER (algum nome de usuário para conexão com o banco de dados);
  - definir um valor para a variável POSTGRES_PASSWORD (senha de conexão com o banco de dados);
  - ajustar valor da variável DATABASE_URL para o seguinte formato: postgres://POSTGRES_USER:POSTGRES_PASSWORD@localhost:5436/POSTGRES_DB.
  Note que os valores definidos para as variáveis de ambiente do banco de dados devem ser substituídos na variável
  DATABASE_URL;
  - no arquivo docker-compose.yml, que se encontra na raiz do projeto, ajustar o valor da variável de ambiente
  DATABASE_URL da seguinte forma: postgres://POSTGRES_USER:POSTGRES_PASSWORD@database:5432/POSTGRES_DB;
  - deve ser mantido um valor numérico inteiro para as variáveis SUPPRESSION_GROUP_ID e SENDER_ID, mesmo que as
  configurações de envio de email com SendGrid não sejam utilizadas;
  - deve ser mantido algum valor qualquer na variável de ambiente SECRET_KEY;
  - ajustar valor da variável DEBUG para True;
  - executar comando 'docker compose up -d';

Após executadas as etapas listadas acima, o projeto deve estar acessível no endereço https://127.0.0.1:8000.


### Para instalar com apenas o banco de dados em conteiner Docker:

O gerenciamento das dependências foi feito através do PIPENV.

  - clonar o projeto;
  - executar o comando 'pipenv install -d' (criação de ambiente virtual e instalação das dependências listadas no
  Pipfile);
  - executar o comando 'pipenv shell' para ativar o ambiente virtual;
  - criar um arquivo chamado .env na raiz do projeto;
  - copiar todo o conteúdo do arquivo env-sample, que se encontra na pasta 'contrib', para dentro do arquivo .env;
  - definir um valor para a variável POSTGRES_DB (nome do banco de dados);
  - definir um valor para a variável POSTGRES_USER (algum nome de usuário para conexão com o banco de dados);
  - definir um valor para a variável POSTGRES_PASSWORD (senha de conexão com o banco de dados);
  - ajustar valor da variável DATABASE_URL para o seguinte formato: postgres://POSTGRES_USER:POSTGRES_PASSWORD@localhost:5436/POSTGRES_DB.
  Note que os valores definidos para as variáveis de ambiente do banco de dados devem ser substituídos na variável
  DATABASE_URL;
  - ajustar valor da variável DEBUG para True;
  - deve ser mantido algum valor qualquer na variável de ambiente SECRET_KEY;
  - deve ser mantido um valor numérico inteiro para as variáveis SUPPRESSION_GROUP_ID e SENDER_ID, mesmo que as
  configurações de envio de email com SendGrid não sejam utilizadas;
  - rodar o comando 'docker compose up -d database' para que seja criado e executado o conteiner do banco de dados;
  - rodar migrações através do comando 'python manage.py migrate';
  - rodar o comando 'python manage.py runserver' para iniciar o aplicativo.

Após executadas as etapas listadas teremos um conteiner com uma imagem do PostgreSQL em execução, e poderemos acessar
o aplicativo no endereço https://127.0.0.1:8000.

Atentar que no arquivo 'env-sample' que se encontra dentro da pasta 'contrib' existe também uma variável de ambiente
DATABASE_URL, e esta não deve ser alterada pois é utilizada no funcionamento da integração contínua (GitHub Actions).


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
- criar outro bucket S3, agora para arquívos de mídia. Este terá a configuração 'Block all public access' desativada,
já que armazenará arquivos que deverão ser visíveis a quem acessar o site. Além desta configuração, a política de
acesso deverá permitir ao usuário IAM a ação 'PutObject' no bucket (e mais alguma outra se necessário), além de
conceder a todos (*) a ação 'GetObject' para o bucket e todas as suas pastas.
Após executadas as etapas listadas, podemos definir as variáveis de ambiente no arquivo .env da seguinte forma:

  - AWS_ACCESS_KEY_ID = valor-do-id-da-secret-key
  - AWS_SECRET_ACCESS_KEY = valor-da-secret-key (atentar que só pode ser visualizado uma vez pela plataforma AWS)
  - AWS_STORAGE_BUCKET_NAME = nome-do-bucket-S3-criado
  - AWS_STORAGE_BUCKET_NAME_MEDIA = nome-do-bucket-de-arquivos-de-midia

Feitas as configurações, ao rodar o comando 'python manage.py collectstatic', os arquivos estáticos serão enviados para
o bucket criado na AWS. Caso os valores das variáveis da AWS não sejam preenchidos (especialmente o valor da variável
AWS_ACCESS_KEY_ID), os arquivos estáticos serão copiados para uma pasta chamada 'staticfiles' na pasta principal do
projeto (configuração STATIC_ROOT no arquivo settings.py). Se esta pasta não existir ela será criada automaticamente.


## Integração com SendGrid

Foi criada neste projeto uma integração com a plataforma de envio de emails SendGrid. Este recurso permite que emails
sejam enviados a pessoas cadastradas sempre que postarmos algum conteúdo (Single Sends). Para seu correto funcionamento
será necessário seguir as seguintes etapas:
- criar uma conta na plataforma SendGrid e acessá-la;
- na plataforma SendGrid, acessar a seção de 'API Keys' e criar uma chave;
- na plataforma SendGrid, na seção 'Marketing', acessar 'Contacts', criar uma lista e acessar. O ID desta lista estará
na URL, e devemos salvá-lo. Esta será a lista onde os contatos serão cadastrados para recebimento de emails;
- na plataforma SendGrid, na seção Marketing, acessar 'Unsubscribe Groups' e criar um grupo. Este grupo será utilizado
para armazenar contatos que se descadastraram de nosso sistema de envio de emails. Na página de criação do grupo veremos
nosso grupo criado, e devemos salvar seu ID que estará a mostra.
- na plataforma SendGrid devemos fazer a verificação e autenticação do email utilizado como emissor. Após feita esta
verificação, consultar Settings > Sender Authentication > clicar no domínio de email verificado e clicar em editar. Na
URL aparecerá o ID deste emissor (Sender), devemos salvar este valor;
- Ainda na plataforma SendGrid, devemos criar dois 'Email Design' na seção 'Design Library'. Estes designs criados também
possuirão ID's listados em suas URL's que devemos salvar. Um design será para publicações de newsletters, e o outro para
publicações de vídeos;
- Após concluídas estas etapas devemos definir as seguintes variáveis de ambiente no arquivo .env:

  - SENDGRID_API_KEY = chave-api-criada-na-plataforma
  - SENDGRID_LIST_ID = id-da-lista-de-email-criada
  - SUPPRESSION_GROUP_ID = id-do-grupo-de-subscricao-criado (Unsubscribe Groups)
  - SENDER_ID = id-do-email-emissor-verificado (Email principal)
  - SENDGRID_NEWSLETTER_DESIGN_ID = id-do-design-de-email-criado-para-newsletters
  - SENDGRID_VIDEO_DESIGN_ID = id-do-design-de-email-criado-para-videos

As variáveis listadas acima deverão ser cadastradas apenas em caso de uso do sistema de email. Porém, caso não seja
utilizado, no momento da publicação de algum conteúdo, sempre que tiver a opção 'Criar rascunho de email', esta deve ser
marcada como 'Não', caso contrário ocorrerá erro ao publicar por não ter as variáveis definidas. Caso alguma variável
seja definida incorretamente ou não seja definida também poderão ocorrer erros ao publicar.

Para o funcionamento do envio de mensagens via formulário de contato devemos cadastrar mais duas variáveis de ambiente:

  - FROM_EMAIL = email cadastrado e verificado no SendGrid, que será utilizado para envio de emails (Email secundário)
  - TO_EMAIL = email que será utilizado para receber e responder as mensagens enviadas

Note que serão necessários dois emails para que a integração com o SendGrid funcione por completo. Um será o email principal,
que será utilizado para envio de newsletters e aviso de novas publicações, e o outro será utilizado para envio de mensagens
para o email principal através do formulário de contato.


## Modelos

Este projeto possui, atualmente, 6 modelos:
- User: usuário padrão do Django com pequenas customizações. Para a criação de novos usuários devemos informar os campos
email, primeiro nome (first_name) e password. O campo email é único, portanto não pode se repetir e precisa ser informado
no momento do login;

- Subject: este modelo, também chamado de 'assunto', foi criado para que os conteúdos publicados no site sejam separados
de alguma forma. Neste caso, alguns conteúdos terão relacionamento de 1 - N com este modelo, o que possibilitará filtragem
e separação dos conteúdos por assunto. É interessante, no início, cadastrar um assunto chamado 'Assuntos gerais', para
que permita a inserção de conteúdos diversos sem a necessidade da criação de vários assuntos distintos. Não será possível
cadastrar Newsletters ou Vídeos sem que antes tenha sido cadastrado um assunto para ser relacionado;

- Service: este modelo permite que sejam inseridos os serviços prestados pelo consultor. O campo 'intro' deve ser uma
breve introdução que aparecerá na home page, na seção de Serviços. Além da 'intro', os campos 'title' e 'home_picture'
também estarão presentes na home page, ao lado de um link responsável por direcionar o usuário à pagina de detalhes do
serviço prestado, onde poderá visualizar um texto mais detalhado. Este modelo não tem relacionamento com o modelo Subject;

- Newsletter: serão textos publicados conforme necessidade do consultor. Este modelo possui relacionamento com o modelo
Subject, portanto em toda publicação de newsletters deverá ser informado um assunto já criado anteriormente. Existe, aqui,
a possibilidade de inserção de textos ricos, com letras formatadas e também fotos. É possível, também, ao adicionar uma
nova newsletter, assinalar a opção 'Criar rascunho de email'. Esta opção, se assinalada, fará com que um rascunho de
email seja criado na plataforma do SendGrid (Single Sends), sendo necessários pequenos complementos para o envio aos
integrantes da lista de emails cadastrados. O design para a montagem do email será o mesmo que criamos ao definir a
variável de ambiente SENDGRID_NEWSLETTER_DESIGN_ID;

- Video: este modelo permite a inserção de vídeos no site. Para publicar um vídeo devemos, primeiramente, publicar este
no YouTube. Após publicado, o vídeo terá um ID que aparecerá na URL do site do YouTube, e este deve ser salvo para que
seja informado no campo 'ID da plataforma' no momento da postagem neste website. Este modelo possui um relacionamento
com o modelo Subject, portanto em toda postagem de vídeo deverá ser informado um assunto já criado anteriormente. Existe,
também, a possibilidade de envio de emails a cada novo vídeo postado, bastando assinalar a opção 'Criar rascunho de email'
no momento da postagem. O design utilizado para a montagem do email será o mesmo que criamos no momento da definição
da variável de ambiente SENDGRID_VIDEO_DESIGN_ID.

- Contact: este modelo serve para salvar mensagens que são enviadas ao consultor através do formulário de contato. Sempre
que um contato é feito uma mensagem é enviada, e são salvos o nome, email, assunto, conteúdo e data de envio desta.
As mensagens recebidas são listadas na página de índice de mensagens, que pode ser acessada através do link 'Mensagens'
que se encontra na navbar, porém disponível apenas para quem tem permissão de visualização. Além de salvar as mensagens
no banco de dados, estas são também enviadas por email, por onde o consultor poderá dar continuidade no assunto com o
usuário que iniciou a conversa através do formulário de contato. Após finalizado o contato, se desejar, o consultor poderá
remover a mensagem do banco de dados através do botão de remoção que se encontra na página de detalhes da mensagem.


## Permissões

Para que seja possível postar, editar e deletar conteúdos do site é necessário ter um usuário cadastrado, logado e com
as devidas permissões concedidas. Para cada modelo (Video, Newsletter etc.) existe um conjunto de permissões que pode
ser concedido ao usuário, o que pode ser customizado conforme a necessidade.

Existem 4 tipos de permissões, são elas: visualização, edição, remoção e adição. Cada uma delas pode ser concedida
separadamente. Se, por exemplo, for acordado que o usuário "X" terá permissão de apenas Editar Video, poderá ser
concedida apenas esta permissão, e tanto o link para adiçao quanto o link para remoção não estarão disponíveis para este
usuário. O acesso às páginas de adição e remoção também será bloqueado para este usuário.

Atualmente todo usuário, logado ou não, tem permissão de visualização de qualquer conteúdo, exceto a página de Assuntos
(Subject) que precisa de um usuário logado e com permissão de visualização de Subject. O link de acesso desta página
estará na navbar do website, e será visível apenas para quem tem permissão de visualização de Subject.

Recomenda-se, sempre que for concedida permissão de adição, remoção ou edição de Subject para algum usuário, que seja
também concedida a permissão de visualização, já que os links de cancelamento de edição ou adição de Subject direcionarão
o usuário para a página de visualização/índice de Subject(Assuntos). Neste caso, se a permissão de visualização não for
concedida, o usuário será direcionado para a página de acesso negado. Serve também para o modelo Contact.
