"""
Ferramenta para análise de áudio usando Whisper (Speech-to-Text).
"""

import os
from openai import OpenAI

def analisar_audio(arquivo_audio):
    """
    Analisa um arquivo de áudio e fornece transcrição.
    
    Args:
        arquivo_audio: Arquivo de áudio carregado
        
    Returns:
        str: Transcrição do áudio
    """
    
    try:
        # Inicializar cliente OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Transcrever áudio
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=arquivo_audio
        )
        
        transcricao = transcript.text
        return f"🎤 **Transcrição do Áudio:**\n\n{transcricao}"
        
    except Exception as e:
        return f"❌ Erro ao analisar áudio: {str(e)}"