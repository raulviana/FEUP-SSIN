# Flow
O nosso grupo deparou-se com algumas dúvidas em relação ao projeto e gostaríamos que o professor nos ajudasse para termos a certeza de que compreendemos tudo o que nos é pedido.

Pela nossa interpretação, o "flow" da Aplicação seria a seguinte: Um cliente é adicionado "diretamente" na base de dados do servidor na face-to-face registration sendo-lhe devolvido um  ID. Este ID será usado para o cliente se registar no seu "dispositivo" e a partir daqui o servidor irá sempre assumir que o cliente que fez log in neste dispositivo será o que realizou este registo, sendo por isso responsabilidade da aplicação client-side fazer a autenticação deste mesmo cliente.

Caso este breve resumo esteja correto, gostaríamos de colocar as seguintes questões:
1) Na aplicação do cliente, esta deverá ter interface gráfica (semelhante a um website) ou podemos simplesmente criar algo que funcione à base de introdução de comandos na linha de comandos?

2) Em relação à face-to-face pre-registration (no momento 1 do enunciado), a introdução de um novo utilizador deverá ser introduzida diretamente no servidor (recorrendo a uma thread por exemplo), ou criamos uma pequena (e terceira) aplicação que facilite este processo, em que apenas o "dono" do servidor tem acesso?

3) Como devemos distinguir diferentes utilizadores na app durante o desenvolvimento dado que os IPs serão iguais? Ou o servidor não deverá associar o ID dos utilizadores ao IP do seu dispositivo, mas recorrer a outra forma que não estejamos neste momento a pensar (ports por exemplo)?

# Resposta 

A interpretação do vosso ‘flow’ está correta. (Já agora uma questão de nomenclatura: quando nos referimos a aplicações que usam serviços externos dizemos ‘clientes’; as pessoas que usam esses ‘clientes’ são os ‘utilizadores’). Aqui cada cliente fica associado a um utilizador, como notam.

 

A interface não está especificada. Podem usar qualquer tipo desde que permita executar as operações
Novamente deverão tomar essa decisão (devem habituar-se a que os ‘stakeholders’ de um sistema ou aplicação geralmente emitem os requisitos de forma genérica e num nível mais elevado, competindo aos engenheiros decidirem e implementatrem a melhor forma de satisfazer esses requisitos …)
Se se desenvolvessem mesmo apps móveis o seu IP varia ao longo do tempo…  Compete às aplicações comunicarem-no ao servidor se houver essa necessidade. No nosso caso, em que para a prova de conceito e teste, estamos a usar várias instâncias de uma mesma aplicação num único PC, todas essas aplicações têm o mesmo IP, mas terão de ter portos diferentes. Assim aqui neste caso, quando do login da aplicação no servidor (em cada sessão), deverão escolher (pode ser o sistema operativo) um porto e comunica-lo ao servidor, permanecendo à escuta nesse porto.