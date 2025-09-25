"""
Ferramenta para geração de áudio usando TTS (Text-to-Speech).
"""

import os
from openai import OpenAI

def gerar_audio(texto):
    """
    Gera áudio a partir de texto usando TTS.
    
    Args:
        texto (str): Texto para converter em áudio
        
    Returns:
        str: Caminho do arquivo de áudio gerado ou mensagem de erro
    """
    
    try:
        # Inicializar cliente OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Gerar áudio
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=texto
        )
        
        # Salvar arquivo de áudio
        audio_filename = "audio_gerado.mp3"
        response.stream_to_file(audio_filename)
        
        return f"🎵 **Áudio gerado com sucesso!**\n\n📝 **Texto:** {texto}\n\n🎧 **Arquivo:** {audio_filename}"
        
    except Exception as e:
        return f"❌ Erro ao gerar áudio: {str(e)}"