"""
Ferramenta para classificar a intenção do usuário baseada na entrada de texto.
"""

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from .categorias import categorias_intencao, descricoes_categorias

def classificar_intencao(texto_usuario):
    """
    Classifica a intenção do usuário baseada no texto de entrada.
    
    Args:
        texto_usuario (str): Texto fornecido pelo usuário
        
    Returns:
        str: Categoria da intenção identificada
    """
    
    # Configurar o modelo
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Criar prompt para classificação
    prompt_template = """
    Você é um classificador de intenções especializado. Sua tarefa é analisar o texto do usuário 
    e determinar qual categoria melhor representa sua intenção.
    
    CATEGORIAS DISPONÍVEIS:
    {categorias}
    
    DESCRIÇÕES DAS CATEGORIAS:
    {descricoes}
    
    TEXTO DO USUÁRIO: "{texto}"
    
    INSTRUÇÕES:
    1. Analise cuidadosamente o texto do usuário
    2. Identifique palavras-chave e contexto
    3. Retorne APENAS o nome da categoria mais apropriada
    4. Se houver dúvida entre categorias, escolha a mais específica
    5. Use "busca_geral" apenas se não houver correspondência clara
    
    CATEGORIA:
    """
    
    # Preparar as categorias e descrições para o prompt
    categorias_str = ", ".join(categorias_intencao)
    descricoes_str = "\n".join([f"- {cat}: {desc.strip()}" for cat, desc in descricoes_categorias.items()])
    
    # Criar o prompt final
    prompt = prompt_template.format(
        categorias=categorias_str,
        descricoes=descricoes_str,
        texto=texto_usuario
    )
    
    try:
        # Fazer a classificação
        response = llm.invoke([HumanMessage(content=prompt)])
        categoria = response.content.strip().lower()
        
        # Validar se a categoria retornada é válida
        if categoria in categorias_intencao:
            return categoria
        else:
            # Se a categoria não for válida, tentar encontrar uma correspondência parcial
            for cat in categorias_intencao:
                if cat in categoria:
                    return cat
            
            # Se não encontrar correspondência, retornar busca_geral
            return "busca_geral"
            
    except Exception as e:
        print(f"Erro na classificação de intenção: {e}")
        return "busca_geral"