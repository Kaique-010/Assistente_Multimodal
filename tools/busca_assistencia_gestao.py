"""
Ferramenta especializada em gestão empresarial e estratégica.
"""

import os
import pickle
import numpy as np
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Importar modelos Django
import setup_django
setup_django.setup_django()
from tools.models import ArtigoProcessado, ArtigosFonte

class GestaoKnowledgeBase:
    def __init__(self):
        self.cache_file = "cache_gestao.pkl"
        self.urls_gestao = [
            "https://sebrae.com.br/",
            "https://www.gov.br/empresas-e-negocios/pt-br",
            "https://www.bndes.gov.br/",
        ]
        self.vectorstore = None
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        
    def _get_database_content(self):
        """Busca conteúdo relevante do banco de dados por palavras-chave."""
        # Palavras-chave relacionadas à gestão
        keywords_gestao = [
            'gestao', 'gerencial', 'administra', 'vendas', 'compras', 'estoque',
            'producao', 'financeiro', 'fluxo de caixa', 'orcamento', 'planejamento',
            'relatorio', 'dashboard', 'indicadores', 'kpi', 'performance',
            'cliente', 'fornecedor', 'produto', 'servico', 'pedido', 'ordem',
            'cadastro', 'usuario', 'permissao', 'configuracao', 'parametros',
            'backup', 'seguranca', 'auditoria', 'log', 'historico'
        ]
        
        # Buscar artigos relacionados à gestão
        artigos_relevantes = []
        for keyword in keywords_gestao:
            # Buscar no título
            artigos_titulo = ArtigosFonte.objects.filter(titulo__icontains=keyword)
            # Buscar no menu
            artigos_menu = ArtigosFonte.objects.filter(menu__icontains=keyword)
            
            for artigo in artigos_titulo.union(artigos_menu):
                if artigo not in artigos_relevantes:
                    artigos_relevantes.append(artigo)
        
        return artigos_relevantes[:50]  # Limitar a 50 artigos mais relevantes
        
    def load_or_create_knowledge_base(self):
        """Carrega ou cria a base de conhecimento híbrida."""
        faiss_path = self.cache_file.replace('.pkl', '_faiss')
        
        # Tentar carregar usando FAISS save_local primeiro
        if os.path.exists(faiss_path):
            try:
                self.vectorstore = FAISS.load_local(faiss_path, self.embeddings, allow_dangerous_deserialization=True)
                # Adicionar conteúdo do banco de dados
                self._add_database_content()
                return
            except Exception as e:
                print(f"Erro ao carregar FAISS: {e}")
        
        # Criar nova base de conhecimento
        self._create_knowledge_base()
    
    def _add_database_content(self):
        """Adiciona conteúdo do banco de dados ao vectorstore existente."""
        try:
            artigos_relevantes = self._get_database_content()
            
            if not artigos_relevantes:
                return
                
            # Preparar textos dos artigos processados
            texts = []
            metadatas = []
            
            for artigo in artigos_relevantes:
                # Buscar trechos processados com embeddings
                trechos = ArtigoProcessado.objects.filter(fonte=artigo, embedding__isnull=False)
                
                for trecho in trechos:
                    texts.append(trecho.conteudo_limpo)
                    metadatas.append({
                        'source': f'Artigo ID: {artigo.artigo_id}',
                        'title': artigo.titulo,
                        'menu': artigo.menu,
                        'type': 'database'
                    })
            
            if texts:
                # Adicionar ao vectorstore existente
                self.vectorstore.add_texts(texts, metadatas=metadatas)
                
        except Exception as e:
            print(f"Erro ao adicionar conteúdo do banco: {e}")
    
    def _create_knowledge_base(self):
        """Cria uma nova base de conhecimento híbrida."""
        try:
            all_texts = []
            all_metadatas = []
            
            # 1. Carregar documentos das URLs
            try:
                loader = WebBaseLoader(self.urls_gestao)
                documents = loader.load()
                
                # Dividir em chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                url_texts = text_splitter.split_documents(documents)
                
                for doc in url_texts:
                    all_texts.append(doc.page_content)
                    all_metadatas.append({
                        'source': doc.metadata.get('source', 'URL'),
                        'type': 'web'
                    })
                    
            except Exception as e:
                print(f"Erro ao carregar URLs: {e}")
            
            # 2. Adicionar conteúdo do banco de dados
            artigos_relevantes = self._get_database_content()
            
            for artigo in artigos_relevantes:
                # Buscar trechos processados
                trechos = ArtigoProcessado.objects.filter(fonte=artigo)
                
                for trecho in trechos:
                    all_texts.append(trecho.conteudo_limpo)
                    all_metadatas.append({
                        'source': f'Artigo ID: {artigo.artigo_id}',
                        'title': artigo.titulo,
                        'menu': artigo.menu,
                        'type': 'database'
                    })
            
            if all_texts:
                # Criar vectorstore
                self.vectorstore = FAISS.from_texts(all_texts, self.embeddings, metadatas=all_metadatas)
                
                # Salvar cache
                try:
                    self.vectorstore.save_local(self.cache_file.replace('.pkl', '_faiss'))
                except Exception as save_error:
                    print(f"Aviso: Não foi possível salvar cache: {save_error}")
            else:
                print("Nenhum conteúdo encontrado para criar a base de conhecimento")
                
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
    Você é um especialista em gestão empresarial com acesso a manuais de ERP e base de conhecimento atualizada.
    
    INSTRUÇÕES:
    - Forneça respostas práticas sobre gestão empresarial
    - Use a base de conhecimento que inclui:
      * Manuais do ERP Spartacus processados
      * Informações de sites especializados
      * Procedimentos operacionais do sistema
    - Priorize informações dos manuais do ERP quando disponíveis
    - Inclua exemplos práticos e passo a passo
    - Cite a fonte quando relevante
    
    CONTEXTO DA BASE DE CONHECIMENTO:
    {context}
    
    PERGUNTA: {question}
    
    RESPOSTA ESPECIALIZADA:
    """
    
    try:
        if kb.vectorstore:
            # Usar RAG com base de conhecimento híbrida
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=kb.vectorstore.as_retriever(search_kwargs={"k": 5}),
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
            
            Forneça uma resposta prática e detalhada.
            """
            
            response = llm.invoke([HumanMessage(content=prompt_simples)])
            return response.content
            
    except Exception as e:
        return f"Erro ao processar consulta de gestão: {str(e)}"