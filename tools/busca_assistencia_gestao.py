"""
Ferramenta especializada em gestão empresarial e estratégica.
"""

import os
import pickle
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

class GestaoKnowledgeBase:
    def __init__(self):
        self.cache_file = "cache_gestao.pkl"
        self.urls_gestao = [
            "https://sebrae.com.br/",
            "https://www.gov.br/empresas-e-negocios/pt-br",
            "https://www.bndes.gov.br/",
        ]
        self.vectorstore = None
        
    def load_or_create_knowledge_base(self):
        """Carrega ou cria a base de conhecimento."""
        faiss_path = self.cache_file.replace('.pkl', '_faiss')
        
        # Tentar carregar usando FAISS save_local primeiro
        if os.path.exists(faiss_path):
            try:
                embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
                self.vectorstore = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
                return
            except Exception as e:
                print(f"Erro ao carregar FAISS: {e}")
        
        # Fallback para pickle (compatibilidade)
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    self.vectorstore = pickle.load(f)
                return
            except Exception as e:
                print(f"Erro ao carregar pickle: {e}")
        
        # Criar nova base de conhecimento
        self._create_knowledge_base()
    
    def _create_knowledge_base(self):
        """Cria uma nova base de conhecimento."""
        try:
            # Carregar documentos
            loader = WebBaseLoader(self.urls_gestao)
            documents = loader.load()
            
            # Dividir em chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Criar embeddings
            embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Criar vectorstore
            self.vectorstore = FAISS.from_documents(texts, embeddings)
            
            # Salvar cache usando FAISS save_local
            try:
                self.vectorstore.save_local(self.cache_file.replace('.pkl', '_faiss'))
            except Exception as save_error:
                print(f"Aviso: Não foi possível salvar cache: {save_error}")
                
        except Exception as e:
            print(f"Erro ao criar base de conhecimento: {e}")
            self.vectorstore = None

def busca_assistencia_gestao(pergunta):
    """
    Busca informações especializadas em gestão empresarial.
    
    Args:
        pergunta (str): Pergunta sobre gestão
        
    Returns:
        str: Resposta especializada
    """
    
    # Configurar o modelo
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Inicializar base de conhecimento
    kb = GestaoKnowledgeBase()
    kb.load_or_create_knowledge_base()
    
    # Prompt especializado
    prompt_template = """
    Você é um especialista em gestão empresarial e estratégica com acesso a manuais de ERP.
    
    INSTRUÇÕES:
    - Forneça respostas práticas sobre gestão empresarial
    - Use a base de conhecimento para informações específicas sobre:
      * Relatórios de vendas
      * Controle de estoque
      * Indicadores de performance
      * Processos no ERP
    - Inclua exemplos práticos e KPIs relevantes
    - Sugira melhores práticas de gestão
    
    CONTEXTO DA BASE DE CONHECIMENTO:
    {context}
    
    PERGUNTA: {question}
    
    RESPOSTA ESPECIALIZADA:
    """
    
    try:
        if kb.vectorstore:
            # Usar RAG com base de conhecimento
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=kb.vectorstore.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={
                    "prompt": PromptTemplate(
                        template=prompt_template,
                        input_variables=["context", "question"]
                    )
                }
            )
            
            resposta = qa_chain.invoke({"query": pergunta})
            return resposta["result"]
        else:
            # Fallback sem base de conhecimento
            prompt_simples = f"""
            Como especialista em gestão empresarial, responda:
            
            {pergunta}
            
            Forneça uma resposta prática com foco em resultados.
            """
            
            response = llm.invoke([HumanMessage(content=prompt_simples)])
            return response.content
            
    except Exception as e:
        return f"Erro ao processar consulta de gestão: {str(e)}"