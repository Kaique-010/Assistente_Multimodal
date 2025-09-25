"""
Configuração centralizada para bases de conhecimento do assistente multimodal.
"""

# URLs para base de conhecimento de contabilidade
CONTABILIDADE_URLS = [
    "https://www.gov.br/receitafederal/pt-br",
    "https://www.cfc.org.br/",
    "https://www.sped.fazenda.gov.br/",
    "https://www.nfe.fazenda.gov.br/",
    "https://www.contabilizei.com.br/contabilidade-online/",
    "https://blog.sage.com/pt-br/",
]

# URLs para base de conhecimento de gestão
GESTAO_URLS = [
    "https://sebrae.com.br/",
    "https://www.gov.br/empresas-e-negocios/pt-br",
    "https://www.bndes.gov.br/",
    "https://endeavor.org.br/",
    "https://www.administradores.com.br/",
]

# Esquemas e relacionamentos de banco de dados
DATABASE_SCHEMAS = {
    "usuarios": {
        "campos": ["id (INT, PK)", "nome (VARCHAR)", "email (VARCHAR)", "created_at (TIMESTAMP)"],
        "relacionamentos": ["vendas.usuario_id → usuarios.id"]
    },
    "produtos": {
        "campos": ["id (INT, PK)", "nome (VARCHAR)", "preco (DECIMAL)", "categoria_id (INT, FK)", "estoque (INT)"],
        "relacionamentos": ["produtos.categoria_id → categorias.id", "vendas.produto_id → produtos.id"]
    },
    "categorias": {
        "campos": ["id (INT, PK)", "nome (VARCHAR)", "descricao (TEXT)"],
        "relacionamentos": ["produtos.categoria_id → categorias.id"]
    },
    "vendas": {
        "campos": ["id (INT, PK)", "usuario_id (INT, FK)", "produto_id (INT, FK)", "quantidade (INT)", "valor_total (DECIMAL)", "data_venda (TIMESTAMP)"],
        "relacionamentos": ["vendas.usuario_id → usuarios.id", "vendas.produto_id → produtos.id"]
    }
}

# Configurações de cache
CACHE_CONFIG = {
    "contabilidade": {
        "arquivo": "cache_contabilidade.pkl",
        "ttl": 86400  # 24 horas
    },
    "gestao": {
        "arquivo": "cache_gestao.pkl", 
        "ttl": 86400  # 24 horas
    },
    "database": {
        "arquivo": "cache_database.pkl",
        "ttl": 3600   # 1 hora
    }
}

def get_contabilidade_urls():
    """Retorna URLs para base de conhecimento de contabilidade."""
    return CONTABILIDADE_URLS

def get_gestao_urls():
    """Retorna URLs para base de conhecimento de gestão."""
    return GESTAO_URLS

def get_database_schemas():
    """Retorna esquemas de banco de dados."""
    return DATABASE_SCHEMAS

def add_contabilidade_url(url):
    """Adiciona nova URL à base de contabilidade."""
    if url not in CONTABILIDADE_URLS:
        CONTABILIDADE_URLS.append(url)
        return True
    return False

def add_gestao_url(url):
    """Adiciona nova URL à base de gestão."""
    if url not in GESTAO_URLS:
        GESTAO_URLS.append(url)
        return True
    return False

def get_cache_config(categoria):
    """Retorna configuração de cache para uma categoria."""
    return CACHE_CONFIG.get(categoria, {})

# Configurações específicas para manuais de ERP
ERP_MANUALS = {
    "contabilidade": {
        "totvs": "https://tdn.totvs.com/display/public/mp/RM",
        "sap": "https://help.sap.com/",
        "oracle": "https://docs.oracle.com/",
        "senior": "https://documentacao.senior.com.br/"
    },
    "gestao": {
        "totvs": "https://tdn.totvs.com/display/public/mp/Gestao",
        "sap": "https://help.sap.com/viewer/product/SAP_BUSINESS_ONE",
        "oracle": "https://docs.oracle.com/en/applications/",
        "senior": "https://documentacao.senior.com.br/gestao/"
    }
}

def get_erp_manuals(categoria):
    """Retorna manuais de ERP para uma categoria específica."""
    return ERP_MANUALS.get(categoria, {})