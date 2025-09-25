Assistente Multimodal

Assistente Especialista em:

Leitura da documentação dos sistemas, por meio de urls dos manuais de procedimento 
buscas na web com contexto nos temas dos sistemas de gestão 
prompts em LLM estruturados para apenas responder sobre os temas propostos 


Fluxo do Assistente:

Recebe a Pergunta do Usuário --> Processa a pergunta identificando a intenção -->
Se a intenção for leitura de documentação, busca a url na documentação e retorna o conteúdo
Se a intenção for busca na web, busca a pergunta na web e retorna os resultados
Se a intenção for prompt estruturado, envia a pergunta para o LLM e retorna a resposta

Retorna a resposta ao usuário com streaming em chunks para melhor experiencia 

Guarda na memória com Redis para reuso das sessões com a memória persistente


Inicio do Assitente:
Prompt para a identificação da intenção baseado nas categorias:
- leitura de documentação
- busca na web
- prompt estruturado
