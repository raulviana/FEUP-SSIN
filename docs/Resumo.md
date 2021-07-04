# (1) Face-to-face pre-registration
The client knows:
- name
- security level
- password

server/register_app.py:
* client requests registration
* The server sends back:
    * username
    * one-time ID 

client/client.py:
* saves .env 
    * creates .env if not found
    * asks username and one-time ID
* env file is encrypted with a password
* tenta fazer registro no server(**2**)
* tenta fazer authentication(**3**)


---
# (2) Registration operation - client application 
the client has in the .env file:
em que ele consegue desincriptar através da password
- username
- one-time ID

The client application and server should generate/store the necessary cryptographic means to perform an automatic authentication of the client with the server for each session.

client_app/client.py:
- exchanging keys: (PUBLIC_KEY method)
    - (5) o client cria as o par de chaves <CLIENT_PRIVATE_KEY, CLIENT_PUBLIC_KEY>
    - o cliente pede a SERVER_PUBLIC_KEY ao server
    - o server dá a SERVER_PUBLIC_KEY
    - o cliente envia ao server, com o conteudo encriptado com a SERVER_PUBLIC_KEY:
        - (5) CLIENT_PUBLIC_KEY
        - username
        - one-time ID
        - SYMMETRIC_KEY
- exchange messages: (SYMMETRIC_KEY method)
    - o server devolve-lhe:
        - TOKEN_1 de signin
- o cliente fica com:
    - (5)<CLIENT_PRIVATE_KEY, CLIENT_PUBLIC_KEY>
    - SERVER_PUBLIC_KEY
    - SYMMETRIC_KEY
    - TOKEN_1 de signin
- o server fica na BD com:
    - <username/port? - TOKEN_1 - SYMMETRIC_KEY - (5)CLIENT_PUBLIC_KEY>

That instance of the client after registration always represents the same collaborator, from that point on.

(5 - terá de ser implementado mais tarde para ser usado na a troca de mensagens entre clientes)


---
# (3) Automatic authentication for each session - client application 

Quando do login da aplicação no servidor (em cada sessão), deverão escolher (pode ser o sistema operativo) um porto e comunica-lo ao servidor, permanecendo à escuta nesse porto.

The client application is responsible for identifying and authenticating the collaborator locally, and only authenticate with the server after this.

O cliente tenta fazer login e uma nova sessão começa:
- o token deve ser alterado a cada login, por isso pede um novo token ao servidor usando:
    - SYMMETRIC_KEY (para encriptar)
    - TOKEN_1
- o server devolve o novo token e atualiza a BD:
     - <username/port? - TOKEN_2 - SYMMETRIC_KEY - (5)...>
- o cliente no final fica com um novo token:
    - TOKEN_2


---
# (4) The client can invoke any service available on the server


---
# (5) A collaborator can send a message to another collaborator