"""
Ferramenta para geração de imagens usando DALL-E.
"""

import os
from openai import OpenAI

def gerar_imagem(descricao):
    """
    Gera uma imagem baseada na descrição fornecida.
    
    Args:
        descricao (str): Descrição da imagem a ser gerada
        
    Returns:
        str: URL da imagem gerada ou mensagem de erro
    """
    
    try:
        # Inicializar cliente OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Gerar imagem
        response = client.images.generate(
            model="dall-e-3",
            prompt=descricao,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Retornar URL da imagem
        image_url = response.data[0].url
        return f"✅ Imagem gerada com sucesso!\n\n🖼️ **Descrição:** {descricao}\n\n🔗 **Link da imagem:** {image_url}"
        
    except Exception as e:
        return f"❌ Erro ao gerar imagem: {str(e)}"