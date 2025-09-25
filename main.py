import streamlit as st
import os
from dotenv import load_dotenv
from tools.classificar_intencao import classificar_intencao
from tools.busca_contabilidade import busca_contabilidade
from tools.busca_assistencia_de_banco_de_dados import busca_assistencia_de_banco_de_dados
from tools.busca_assistencia_gestao import busca_assistencia_gestao
from tools.busca_geral import busca_geral
from tools.gerar_imagem import gerar_imagem
from tools.analisar_imagem import analisar_imagem
from tools.gerar_audio import gerar_audio
from tools.analisar_audio import analisar_audio
from tools.gerar_video import gerar_video
from tools.analisar_video import analisar_video
from learning_system import LearningSystem

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Assistente Multimodal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar sistema de aprendizado
learning_system = LearningSystem()

# Título principal
st.title("🤖 Assistente Multimodal Inteligente")
st.markdown("---")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seleção de modelo
    modelo_selecionado = st.selectbox(
        "Modelo de IA:",
        ["OpenAI GPT-4", "Google Gemini", "Anthropic Claude"],
        index=0
    )
    
    # Configurações de temperatura
    temperatura = st.slider(
        "Criatividade (Temperatura):",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    st.markdown("---")
    st.markdown("### 📊 Estatísticas")
    
    # Mostrar estatísticas do sistema de aprendizado
    stats = learning_system.get_learning_insights()
    st.metric("Total de Interações", stats.get('total_interactions', 0))
    st.metric("Consultas Frequentes", len(stats.get('frequent_queries', [])))

# Interface principal
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Conversa")
    
    # Área de entrada do usuário
    user_input = st.text_area(
        "Digite sua pergunta ou solicitação:",
        height=100,
        placeholder="Ex: Como fazer uma nota fiscal? Crie uma imagem de um gato..."
    )
    
    # Upload de arquivos
    uploaded_file = st.file_uploader(
        "Ou faça upload de um arquivo:",
        type=['png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4', 'avi', 'mov']
    )
    
    # Botão de envio
    if st.button("🚀 Enviar", type="primary"):
        if user_input or uploaded_file:
            with st.spinner("Processando..."):
                try:
                    # Classificar intenção
                    intencao = classificar_intencao(user_input if user_input else "Analisar arquivo")
                    
                    # Registrar interação
                    learning_system.record_interaction(
                        user_input if user_input else "Upload de arquivo",
                        intencao,
                        modelo_selecionado
                    )
                    
                    # Processar baseado na intenção
                    if intencao == "contabilidade":
                        resposta = busca_contabilidade(user_input)
                    elif intencao == "banco_de_dados":
                        resposta = busca_assistencia_de_banco_de_dados(user_input)
                    elif intencao == "gestao":
                        resposta = busca_assistencia_gestao(user_input)
                    elif intencao == "gerar_imagem":
                        resposta = gerar_imagem(user_input)
                    elif intencao == "analisar_imagem" and uploaded_file:
                        resposta = analisar_imagem(uploaded_file)
                    elif intencao == "gerar_audio":
                        resposta = gerar_audio(user_input)
                    elif intencao == "analisar_audio" and uploaded_file:
                        resposta = analisar_audio(uploaded_file)
                    elif intencao == "gerar_video":
                        resposta = gerar_video(user_input)
                    elif intencao == "analisar_video" and uploaded_file:
                        resposta = analisar_video(uploaded_file)
                    else:
                        resposta = busca_geral(user_input)
                    
                    # Exibir resposta
                    st.success("✅ Processado com sucesso!")
                    st.markdown("### 📝 Resposta:")
                    st.markdown(resposta)
                    
                    # Registrar feedback positivo (assumindo sucesso)
                    learning_system.record_feedback(
                        user_input if user_input else "Upload de arquivo",
                        resposta,
                        "positive"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Erro ao processar: {str(e)}")
                    # Registrar feedback negativo
                    learning_system.record_feedback(
                        user_input if user_input else "Upload de arquivo",
                        str(e),
                        "negative"
                    )
        else:
            st.warning("⚠️ Por favor, digite uma pergunta ou faça upload de um arquivo.")

with col2:
    st.header("🎯 Intenções Detectadas")
    
    # Mostrar exemplos de intenções
    st.markdown("""
    **Contabilidade:**
    - Como emitir nota fiscal?
    - Fazer lançamento contábil
    
    **Banco de Dados:**
    - Consulta SQL
    - Estrutura de tabelas
    
    **Gestão:**
    - Relatórios gerenciais
    - Controle de estoque
    
    **Multimodal:**
    - Gerar/analisar imagens
    - Processar áudio/vídeo
    """)
    
    st.markdown("---")
    st.header("📈 Consultas Frequentes")
    
    # Mostrar consultas mais frequentes
    insights = learning_system.get_learning_insights()
    frequent_queries = insights.get('frequent_queries', [])
    
    for i, query in enumerate(frequent_queries[:5], 1):
        st.markdown(f"{i}. {query}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🚀 Assistente Multimodal Inteligente | Desenvolvido com Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)