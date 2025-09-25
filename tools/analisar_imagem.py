"""
Ferramenta para análise de imagens usando GPT-4 Vision.
"""

import os
import base64
from openai import OpenAI

def analisar_imagem(arquivo_imagem):
    """
    Analisa uma imagem e fornece descrição detalhada.
    
    Args:
        arquivo_imagem: Arquivo de imagem carregado
        
    Returns:
        str: Análise detalhada da imagem
    """
    
    try:
        # Inicializar cliente OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Converter imagem para base64
        image_data = arquivo_imagem.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Analisar imagem
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analise esta imagem detalhadamente. Descreva o que você vê, incluindo objetos, pessoas, cores, ambiente, emoções transmitidas e qualquer texto visível."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        analise = response.choices[0].message.content
        return f"🔍 **Análise da Imagem:**\n\n{analise}"
        
    except Exception as e:
        return f"❌ Erro ao analisar imagem: {str(e)}"