"""
Sistema de Agente Multimodal baseado em Grafos usando LangGraph.
"""

import os
import operator
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List

# LangChain e LangGraph
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langgraph.graph import END, StateGraph

# Importar ferramentas especializadas
from tools.categorias import categorias_intencao
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

# Carregar variáveis de ambiente
load_dotenv()

# Modelo de linguagem
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

# --- ESTADO DO AGENTE ---
class AgentState(TypedDict):
    """
    Define os estados do agente multimodal.
    """
    input: str
    intencao: str
    resposta_final: str
    arquivo_upload: str
    # Histórico que se acumula no LangGraph
    history: Annotated[List[BaseMessage], operator.add]

# --- NÓS DO GRAFO ---

def classificar_intencao(state: AgentState) -> dict:
    """
    Classifica a intenção do usuário usando o histórico para contexto.
    """
    print("--- 🧠 Classificando intenção ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um classificador de intenção para um assistente multimodal. 
        Analise a última mensagem do usuário e classifique em uma das categorias:
        {categorias}
        
        Considere o contexto da conversa. Responda APENAS com o nome da categoria."""),
        MessagesPlaceholder(variable_name="history"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    intencao_classificada = chain.invoke({
        "history": state['history'],
        "categorias": ", ".join(categorias_intencao)
    })
    
    print(f"Intenção classificada: {intencao_classificada}")
    return {"intencao": intencao_classificada.strip()}

def node_contabilidade(state: AgentState) -> dict:
    """Nó especializado em contabilidade."""
    print("--- 📊 Processando consulta contábil ---")
    resposta = busca_contabilidade(state['input'])
    return {"resposta_final": resposta}

def node_banco_dados(state: AgentState) -> dict:
    """Nó especializado em banco de dados."""
    print("--- 🗄️ Processando consulta de banco de dados ---")
    resposta = busca_assistencia_de_banco_de_dados(state['input'])
    return {"resposta_final": resposta}

def node_gestao(state: AgentState) -> dict:
    """Nó especializado em gestão."""
    print("--- 📈 Processando consulta de gestão ---")
    resposta = busca_assistencia_gestao(state['input'])
    return {"resposta_final": resposta}

def node_gerar_imagem(state: AgentState) -> dict:
    """Nó para geração de imagens."""
    print("--- 🎨 Gerando imagem ---")
    resposta = gerar_imagem(state['input'])
    return {"resposta_final": resposta}

def node_analisar_imagem(state: AgentState) -> dict:
    """Nó para análise de imagens."""
    print("--- 🔍 Analisando imagem ---")
    if state.get('arquivo_upload'):
        resposta = analisar_imagem(state['arquivo_upload'])
    else:
        resposta = "Por favor, faça upload de uma imagem para análise."
    return {"resposta_final": resposta}

def node_gerar_audio(state: AgentState) -> dict:
    """Nó para geração de áudio."""
    print("--- 🎵 Gerando áudio ---")
    resposta = gerar_audio(state['input'])
    return {"resposta_final": resposta}

def node_analisar_audio(state: AgentState) -> dict:
    """Nó para análise de áudio."""
    print("--- 🎧 Analisando áudio ---")
    if state.get('arquivo_upload'):
        resposta = analisar_audio(state['arquivo_upload'])
    else:
        resposta = "Por favor, faça upload de um arquivo de áudio para análise."
    return {"resposta_final": resposta}

def node_gerar_video(state: AgentState) -> dict:
    """Nó para geração de vídeo."""
    print("--- 🎬 Gerando vídeo ---")
    resposta = gerar_video(state['input'])
    return {"resposta_final": resposta}

def node_analisar_video(state: AgentState) -> dict:
    """Nó para análise de vídeo."""
    print("--- 📹 Analisando vídeo ---")
    if state.get('arquivo_upload'):
        resposta = analisar_video(state['arquivo_upload'])
    else:
        resposta = "Por favor, faça upload de um arquivo de vídeo para análise."
    return {"resposta_final": resposta}

def node_busca_geral(state: AgentState) -> dict:
    """Nó para busca geral."""
    print("--- 🔍 Processando busca geral ---")
    resposta = busca_geral(state['input'])
    return {"resposta_final": resposta}

# --- LÓGICA DE ROTEAMENTO ---
def decidir_proximo_passo(state: AgentState) -> str:
    """Decide qual nó executar baseado na intenção classificada."""
    intencao = state['intencao'].lower()
    print(f"--- 🛤️ Roteando para: {intencao} ---")
    
    roteamento = {
        "contabilidade": "node_contabilidade",
        "banco_de_dados": "node_banco_dados", 
        "gestao": "node_gestao",
        "gerar_imagem": "node_gerar_imagem",
        "analisar_imagem": "node_analisar_imagem",
        "gerar_audio": "node_gerar_audio",
        "analisar_audio": "node_analisar_audio",
        "gerar_video": "node_gerar_video",
        "analisar_video": "node_analisar_video",
        "busca_geral": "node_busca_geral"
    }
    
    return roteamento.get(intencao, "node_busca_geral")

# --- CONSTRUÇÃO DO GRAFO ---
def criar_grafo_assistente():
    """Cria e retorna o grafo do assistente multimodal."""
    
    graph = StateGraph(AgentState)
    
    # Adicionar nós
    graph.add_node('classificador', classificar_intencao)
    graph.add_node('node_contabilidade', node_contabilidade)
    graph.add_node('node_banco_dados', node_banco_dados)
    graph.add_node('node_gestao', node_gestao)
    graph.add_node('node_gerar_imagem', node_gerar_imagem)
    graph.add_node('node_analisar_imagem', node_analisar_imagem)
    graph.add_node('node_gerar_audio', node_gerar_audio)
    graph.add_node('node_analisar_audio', node_analisar_audio)
    graph.add_node('node_gerar_video', node_gerar_video)
    graph.add_node('node_analisar_video', node_analisar_video)
    graph.add_node('node_busca_geral', node_busca_geral)
    
    # Definir ponto de entrada
    graph.set_entry_point('classificador')
    
    # Adicionar arestas condicionais
    graph.add_conditional_edges(
        'classificador',
        decidir_proximo_passo,
        {
            "node_contabilidade": "node_contabilidade",
            "node_banco_dados": "node_banco_dados",
            "node_gestao": "node_gestao",
            "node_gerar_imagem": "node_gerar_imagem",
            "node_analisar_imagem": "node_analisar_imagem",
            "node_gerar_audio": "node_gerar_audio",
            "node_analisar_audio": "node_analisar_audio",
            "node_gerar_video": "node_gerar_video",
            "node_analisar_video": "node_analisar_video",
            "node_busca_geral": "node_busca_geral"
        }
    )
    
    # Adicionar arestas para o fim
    for node in ["node_contabilidade", "node_banco_dados", "node_gestao", 
                 "node_gerar_imagem", "node_analisar_imagem", "node_gerar_audio",
                 "node_analisar_audio", "node_gerar_video", "node_analisar_video",
                 "node_busca_geral"]:
        graph.add_edge(node, END)
    
    return graph.compile()

# --- CLASSE PRINCIPAL DO AGENTE ---
class AssistenteMultimodalGraph:
    """Classe principal do assistente baseado em grafos."""
    
    def __init__(self):
        self.app = criar_grafo_assistente()
        self.history = ChatMessageHistory()
    
    def processar_mensagem(self, input_usuario: str, arquivo_upload=None) -> dict:
        """
        Processa uma mensagem do usuário através do grafo.
        
        Args:
            input_usuario: Texto da mensagem do usuário
            arquivo_upload: Arquivo carregado (opcional)
            
        Returns:
            dict: Resultado com resposta_final e intencao
        """
        # Adicionar mensagem do usuário ao histórico
        self.history.add_user_message(input_usuario)
        
        # Preparar estado inicial
        estado_inicial = {
            "history": self.history.messages,
            "input": input_usuario,
            "arquivo_upload": arquivo_upload
        }
        
        # Executar o grafo
        resultado = self.app.invoke(estado_inicial)
        
        # Extrair resposta e intenção
        resposta_agente = resultado.get('resposta_final', 'Desculpe, não consegui processar sua solicitação.')
        intencao = resultado.get('intencao', 'desconhecido')
        
        # Adicionar resposta ao histórico
        self.history.add_ai_message(resposta_agente)
        
        return {
            'resposta_final': resposta_agente,
            'intencao': intencao
        }
    
    def limpar_historico(self):
        """Limpa o histórico da conversa."""
        self.history = ChatMessageHistory()

# --- FUNÇÃO PARA TESTE EM LINHA DE COMANDO ---
def main():
    """Função principal para teste em linha de comando."""
    assistente = AssistenteMultimodalGraph()
    
    print("🤖 Assistente Multimodal com LangGraph iniciado!")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        input_usuario = input("Você: ")
        if input_usuario.lower() in ['sair', 'exit']:
            break
        
        resposta = assistente.processar_mensagem(input_usuario)
        print(f"Assistente: {resposta['resposta_final']}\n")

if __name__ == "__main__":
    main()