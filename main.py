import streamlit as st
import os
from dotenv import load_dotenv
from agent_graph import AssistenteMultimodalGraph
from learning_system import LearningSystem

# Carregar variáveis de ambiente
load_dotenv()

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Assistente Multimodal Spartacus Sistemas",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado para estilo moderno
    st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #2C6582 0%, #557D87 100%);
    }
    
    /* Container principal */
    .main .block-container {
        background: #557D87;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: #557D87;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Input area */
    .stChatInput {
        border-radius: 25px;
        border: 2px solid #4facfe;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* File uploader */
    .stFileUploader {
        background:#557D87;
        border-radius: 10px;
        padding: 1rem;
        border: 2px dashed #4facfe;
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Title styling */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    st.markdown{
        text-align:center
    }
    /* Sidebar title */
    .sidebar h2 {
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    /*ToolBar*/
    .stAppToolbar {
        background: linear-gradient(120deg, #557D87 0%, #5cfe 100%);
    }
    /*stBottomBlockContainer*/
    .st-emotion-cache-1y34ygi  {
        background: linear-gradient(120deg, #557D87 0%, #5cfe 100%);
    }
    p{
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    

    st.title("Assistente Multimodal Spartacus Sistemas")
    st.markdown("Sistema inteligente baseado em grafos para assistência especializada")
    
    # Inicializar o sistema de grafos
    if 'agent_graph' not in st.session_state:
        st.session_state.agent_graph = AssistenteMultimodalGraph()
    
    # Inicializar sistema de aprendizado
    if 'learning_system' not in st.session_state:
        st.session_state.learning_system = LearningSystem()
    
    # Inicializar histórico de chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar com informações
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: white; margin-bottom: 0;">📊 Sistema</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">LangGraph + Memória Conversacional</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Container para métricas
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        
        # Estatísticas do sistema de aprendizado
        stats = st.session_state.learning_system.get_learning_insights()
        if stats.get('total_interactions', 0) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔄 Interações", stats['total_interactions'])
            with col2:
                if 'success_rate' in stats:
                    st.metric("✅ Sucesso", f"{stats['success_rate']:.1%}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Espaçamento
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão para limpar histórico com estilo
        st.markdown("""
        <div style="text-align: center;">
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Limpar Histórico", use_container_width=True):
            st.session_state.messages = []
            st.session_state.agent_graph.limpar_historico()  # Usar método do grafo
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Informações adicionais
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
            <h4 style="color: white; margin-bottom: 0.5rem;">🚀 Recursos</h4>
            <ul style="color: rgba(255,255,255,0.9); font-size: 0.85rem; margin: 0;">
                <li>Análise de imagens, áudio e vídeo</li>
                <li>Busca especializada em contabilidade</li>
                <li>Assistência em gestão empresarial</li>
                <li>Geração de conteúdo multimodal</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Área de upload de arquivos
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h3 style="color: #2c3e50; margin-bottom: 1rem;">📎 Upload de Arquivos</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Arraste e solte seus arquivos aqui ou clique para selecionar",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi', 'mov', 'txt'],
        help="Suporte para imagens, áudio, vídeo e texto"
    )
    
    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processar com o sistema de grafos
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                try:
                    # Executar o grafo
                    resultado = st.session_state.agent_graph.processar_mensagem(
                        prompt, 
                        uploaded_files
                    )
                    
                    resposta = resultado.get('resposta_final', 'Desculpe, não consegui processar sua solicitação.')
                    
                    # Registrar interação no sistema de aprendizado
                    st.session_state.learning_system.record_interaction(
                        user_input=prompt,
                        intent=resultado.get('intencao', 'desconhecido'),
                        model_used="gpt-4o"
                    )
                    
                    st.markdown(resposta)
                    
                    # Adicionar resposta ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    
                except Exception as e:
                    error_msg = f"Erro ao processar: {str(e)}"
                    st.error(error_msg)
                    
                    # Registrar erro no sistema de aprendizado
                    st.session_state.learning_system.record_interaction(
                        user_input=prompt,
                        intent="erro",
                        model_used="gpt-4o"
                    )

if __name__ == "__main__":
    main()