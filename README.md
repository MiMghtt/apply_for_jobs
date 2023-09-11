# Case TOTVS - Analista de Cloud I 
## Realizado por: Michelle Marighetti

![overview](https://github.com/MiMghtt/apply_for_jobs/assets/113615260/1b6d9851-c531-417a-878d-f6db53c09ced)

## Backend
1. Para a solução da parte do back-end do case técnico, realizei primeiramente um código em **Python**, seguindo a lógica solcitada em: https://github.com/totvscloud-seginf/apply_for_jobs

## Funções:

### 1. Função generate_password(complexity)

Esta função gera uma senha aleatória com base na complexidade especificada. Ela usa caracteres maiúsculos e dígitos e cria uma senha de 12 caracteres.
Atende ao requisito 

*** 1 - Usuário irá inserir uma senha ou solicitar ao Sistema para gerar senha aleatória baseada em políticas de complexidade (tipo de caracteres, números, letras, tamanho, etc); *** 

pois gera senhas aleatórias com base na complexidade. 

### 2. Função create_password(event, context)

Esta função é acionada quando o usuário solicita a criação de uma senha. Ela recebe parâmetros da solicitação, como complexidade, número de visualizações e dias de expiração.
Gera uma senha aleatória usando a função generate_password(complexity).
Cria uma entrada no banco de dados (DynamoDB) com informações sobre a senha, como ID, senha, número de visualizações restantes e tempo de expiração.
Gera uma URL que permite ao usuário visualizar a senha com base nos critérios de expiração.
Atende aos requisitos 

*** 1 - Usuário irá inserir uma senha ou solicitar ao Sistema para gerar senha aleatória baseada em políticas de complexidade (tipo de caracteres, números, letras, tamanho, etc); ***

*** 2 - Usuário irá especificar quantas vezes a senha gerada poderá ser vista e qual o tempo que a senha ficará válida; ***

*** 3 - O sistema irá gerar uma URL que dá acesso a visualização da senha, baseando-se nos critérios do item 02 ***

pois permite ao usuário criar senhas, especificar visualizações e tempo de expiração, e gera URLs para visualização.

### 3. Função get_password_from_dynamodb(password_id) ###

Esta função é usada para obter uma senha do banco de dados com base no ID da senha.
Verifica se a senha ainda está disponível com base nas visualizações e no tempo de expiração.
Atende aos requisitos

*** 1 - Usuário irá inserir uma senha ou solicitar ao Sistema para gerar senha aleatória baseada em políticas de complexidade (tipo de caracteres, números, letras, tamanho, etc); ***

*** 2 - Usuário irá especificar quantas vezes a senha gerada poderá ser vista e qual o tempo que a senha ficará válida; ***

*** 4 - Após atingir a quantidade de visualizações ou o tempo disponível, o sistema bloqueia/elimina a visualização da senha (expirado). A senha não deve ser armazenada após sua expiração ***

pois permite a recuperação da senha, verifica se a senha é válida com base nas visualizações e no tempo de expiração e impede o acesso após a expiração.

### 4. Função check_password_availability(event, context) ###

Esta função é acionada quando um usuário solicita visualizar uma senha com base em um ID de senha.
Verifica a disponibilidade da senha com base nas visualizações restantes.
Se a senha estiver disponível, atualiza o número de visualizações restantes e retorna a senha.
Se a senha não estiver disponível, retorna um erro.
Atende aos requisitos 

*** 2 - Usuário irá especificar quantas vezes a senha gerada poderá ser vista e qual o tempo que a senha ficará válida; ***

*** 4 - Após atingir a quantidade de visualizações ou o tempo disponível, o sistema bloqueia/elimina a visualização da senha (expirado). A senha não deve ser armazenada após sua expiração ***

pois permite que o usuário visualize senhas com base nas visualizações restantes e bloqueia o acesso após a expiração.


2. Após a criação do arquivo .py disponível nesse repositório na pasta "backend", foi gerado uma ```Lambda function``` na **AWS**. 

3. A ```Lambda function``` é integrada a ```API Gateway``` para execução do programa e criação dos. Endpoints HTTP 

**Exemplo de rotas sendo chamadas na API Gateway da AWS conectado na Lambda Function:**

![rotas](https://github.com/MiMghtt/apply_for_jobs/assets/113615260/3625de34-6521-4d79-bcc8-6bf71d78a462)


*** Teste para create_password: ***
{
  "body": "{\"complexity\": \"medium\", \"views\": 5, \"expiration_days\": 7}"
}

*** Response ***
{
  "ResponseMetadata": {
    "RequestId": "LCN91R8QICF353FQ3GF7FBT35JVV4KQNSO5AEMVJF66Q9ASUAAJG",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "server": "Server",
      "date": "Mon, 11 Sep 2023 05:29:16 GMT",
      "content-type": "application/x-amz-json-1.0",
      "content-length": "2",
      "connection": "keep-alive",
      "x-amzn-requestid": "LCN91R8QICF353FQ3GF7FBT35JVV4KQNSO5AEMVJF66Q9ASUAAJG",
      "x-amz-crc32": "2745614147"
    },
    "RetryAttempts": 0
  },
  "body": "{\"password_url\": \"http://localhost:3000/view/84fc0408-7e4d-4dfb-bab2-f3bd8bb7eb12\"}"
}

*** Teste para check_password_availability: ***
{
  "pathParameters": {
    "passwordId": "f7a2e4f9-1404-41a7-911e-8301661718d5"
  }
}


*** Teste para view_password: ***
{
  "pathParameters": {
    "passwordId": "f7a2e4f9-1404-41a7-911e-8301661718d5"
  }
}

4. É criado uma tabela de Senhas dentro do ```DynamoDB``` para o armazenamento temporário das senhas geradas pelo sistema. Foi necessário uma política dentro do ```Identity and Access Management (IAM)``` para que fosse possível a integração do ```DynamoDB``` com o restante do sistema.

*** Editor de políticas ***
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
            "Action": [
                        "dynamodb:DeleteItem",
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:Scan",
                        "dynamodb:UpdateItem",
                        "dynamodb:ConditionCheckItem"
            ],
			"Resource": "arn:aws:dynamodb:us-east-1:107887846702:table/Senhas"
		}
	]
}


### Frontend
Para realização do frontend da aplicação, foi utilizado o framework React.js e o código encontra-se disponível na pasta "frontend" deste repositório. 

*** Requisito 1: Usuário insere ou solicita senha aleatória ***

Para permitir que o usuário insira uma senha manualmente ou solicite uma senha aleatória com base em políticas de complexidade, você pode criar campos de entrada em seu site. Por exemplo, você pode ter um campo de entrada de texto para que o usuário insira uma senha ou um botão "Gerar Senha Aleatória". Ao clicar no botão, você pode usar JavaScript para chamar uma função que gera uma senha aleatória com base nas políticas de complexidade.

*** Requisito 2: Especificar quantas vezes a senha pode ser vista e tempo de validade ***

Para permitir que o usuário especifique quantas vezes a senha pode ser vista e o tempo de validade, você pode adicionar campos adicionais ao formulário. Por exemplo, campos de entrada numérica para a quantidade de visualizações e a duração da validade. Esses valores seriam enviados ao backend juntamente com a senha.

*** Requisito 3: Gerar URL de acesso à senha ***

Após criar a senha com base nos critérios fornecidos pelo usuário, você pode gerar uma URL única que dará acesso à visualização da senha. Essa URL deve conter informações, como um token ou ID exclusivo, que o backend pode usar para verificar a senha associada.

*** Requisito 4: Bloquear/eliminar visualizações após expiração ***

Para implementar esse requisito, você precisa configurar uma lógica no backend (sua função Lambda) que rastreia o número de visualizações permitidas e a duração de validade. Quando alguém acessa a URL da senha, o backend deve verificar esses critérios e, se a senha atingir o limite de visualizações ou o tempo de validade expirar, o backend pode retornar uma resposta indicando que a senha não está mais disponível. Você também pode considerar a remoção da senha da sua base de dados nesse ponto, para evitar futuros acessos.

### Controles de segurança

*** Controle de Acesso *** 
Autenticação de multifator (MFA)

*** Auditoria e logging ***
Registrar todas as atividades do sistema como tentativas de login, ações de usuários, operações de adm, etc. Monitoramente desses logs

*** Segurança API ***
Não permitir acesso não autorizado

*** Segurança em nuvem ***
Seguir as boas práticas de segurança em nuvem como as configurações adequadas de rede e gerenciamento de identidade.

*** Testes de segurança *** 
Testar invasão buscando identificar e corrigir as vulnerabilidades do sistema

### Melhorias

*** Amazon SES ***
Ao invés do gerador de senha mostrar diretamente na página web, enviar a senha por email seria melhor para não expor o usuário. Existe a funcionalidade ```Amazon SES``` que permite configurar o envio de emails de maneira automatizada.

*** Amazon CloudWatch ***
Seria uma maneira de configurar alarmes, como por exemplo, se o limite de visualizações das senhas atingir o limite, é possível integra-lo a ```Lambda Function```. Também é possível por ele fazer o acompanhamento dos logs da aplicação.

*** Amazon S3 - Bucket ***
Criação de um bucket para armazenar o Front-End. Para isso seria necessário incluir toda a pasta build/ da minha aplicação front-end em React.js, ir em propriedades e configurar o bucket para hospedar um site estático, permitir acesso publico e configurar para que a página seja o arquivo index.html. 





