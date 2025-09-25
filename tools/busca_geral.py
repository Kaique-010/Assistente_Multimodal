"""
Ferramenta de busca geral para perguntas diversas.
"""

import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

def busca_geral(pergunta):
    """
    Busca informações gerais e responde perguntas diversas.
    
    Args:
        pergunta (str): Pergunta geral
        
    Returns:
        str: Resposta informativa
    """
    
    # Configurar o modelo
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Prompt para busca geral
    prompt = f"""
    Você é um assistente inteligente e prestativo. Responda à seguinte pergunta de forma 
    clara, informativa e útil:
    
    {pergunta}
    
    Forneça uma resposta completa e bem estruturada.
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
        
    except Exception as e:
        return f"Erro ao processar pergunta: {str(e)}"