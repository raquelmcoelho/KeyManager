Trabalho Echo Server - Gerenciador de chaves

Echo server "Key manager" que utiliza os métodos da classe 
Cofre e User para armazenar senhas, checar seu nível 
(utilizando regex tendo como base seus dados e informações
dos cofres), e salvar suas informações
num file json possibilitando seu acesso.
O cliente manuseia uma cópia do seu cofre e o servidor tem acesso e manuseia 
realmente os dados de todos os usuários.
