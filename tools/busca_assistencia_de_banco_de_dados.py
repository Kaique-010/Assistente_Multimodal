"""
Ferramenta especializada em assistência de banco de dados e SQL.
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

def busca_assistencia_de_banco_de_dados(pergunta):
    """
    Fornece assistência especializada em banco de dados e SQL.
    
    Args:
        pergunta (str): Pergunta sobre banco de dados
        
    Returns:
        str: Resposta especializada
    """
    
    # Configurar o modelo
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Esquemas e relacionamentos do sistema
    database_schema = """
    ESTRUTURA DO BANCO DE DADOS:
    
    Tabela: usuarios
    - id (INT, PK)
    - nome (VARCHAR)
    - email (VARCHAR)
    - created_at (TIMESTAMP)
    
    Tabela: produtos
    - id (INT, PK)
    - nome (VARCHAR)
    - preco (DECIMAL)
    - categoria_id (INT, FK)
    - estoque (INT)
    
    Tabela: categorias
    - id (INT, PK)
    - nome (VARCHAR)
    - descricao (TEXT)
    
    Tabela: vendas
    - id (INT, PK)
    - usuario_id (INT, FK)
    - produto_id (INT, FK)
    - quantidade (INT)
    - valor_total (DECIMAL)
    - data_venda (TIMESTAMP)
    
    RELACIONAMENTOS:
    - produtos.categoria_id → categorias.id
    - vendas.usuario_id → usuarios.id
    - vendas.produto_id → produtos.id
    """
    
    # Prompt especializado
    prompt_template = """
    Você é um especialista em banco de dados e SQL com conhecimento completo da estrutura do sistema.
    
    ESTRUTURA DO SISTEMA:
    {schema}
    
    INSTRUÇÕES:
    - Forneça consultas SQL precisas e otimizadas
    - Explique a lógica por trás das consultas
    - Sugira índices quando apropriado
    - Considere performance e boas práticas
    - Use JOINs adequados baseados nos relacionamentos
    
    PERGUNTA: {pergunta}
    
    RESPOSTA ESPECIALIZADA:
    """
    
    try:
        # Criar o prompt final
        prompt = prompt_template.format(
            schema=database_schema,
            pergunta=pergunta
        )
        
        # Fazer a consulta
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
        
    except Exception as e:
        return f"Erro ao processar consulta de banco de dados: {str(e)}"