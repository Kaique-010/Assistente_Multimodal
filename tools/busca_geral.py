import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
)

#criar o Prompt para o o sistema
system_prompt = SystemMessage(content="Você é um assistente multimodal capaz de responder perguntas diversas usando a ferramenta de 'busca' na internet.")

@tool("busca")
def busca_geral(pergunta: str) -> str:
    """
    Busca informações atualizadas na internet baseadas na pergunta.
    
    Args:
        pergunta (str): A pergunta ou consulta a ser realizada na internet.
    
    Returns:
        str: A resposta obtida da busca na internet, Ou uma mensagem de quem não houve resultados;
    """
    search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2)
    resultados = search.invoke({"query": pergunta})
    return resultados[0]["content"] if resultados else "Nenhum resultado encontrado."
