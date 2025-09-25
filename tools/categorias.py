"""
Categorias e descrições para classificação de intenções do assistente multimodal.
"""

# Categorias de intenção disponíveis
categorias_intencao = [
    "contabilidade",
    "banco_de_dados", 
    "gestao",
    "gerar_imagem",
    "analisar_imagem",
    "gerar_audio",
    "analisar_audio",
    "gerar_video",
    "analisar_video",
    "busca_geral"
]

# Descrições detalhadas de cada categoria
descricoes_categorias = {
    "contabilidade": """
    Questões relacionadas à contabilidade, tributação brasileira, emissão de notas fiscais,
    lançamentos contábeis, impostos, DRE, balanço patrimonial, fluxo de caixa,
    obrigações acessórias, SPED, ECF, DCTF, e demais aspectos contábeis e fiscais.
    """,
    
    "banco_de_dados": """
    Consultas sobre estruturas de banco de dados, queries SQL, relacionamentos entre tabelas,
    otimização de consultas, modelagem de dados, índices, procedures, triggers,
    e administração de sistemas de banco de dados.
    """,
    
    "gestao": """
    Questões sobre gestão empresarial, relatórios gerenciais, controle de estoque,
    vendas, compras, fluxo de caixa, indicadores de performance (KPIs),
    planejamento estratégico, e processos administrativos.
    """,
    
    "gerar_imagem": """
    Solicitações para criar, gerar ou produzir imagens, ilustrações, gráficos,
    logos, designs, arte digital, ou qualquer conteúdo visual.
    Palavras-chave: criar imagem, gerar foto, fazer desenho, design, ilustração.
    """,
    
    "analisar_imagem": """
    Pedidos para analisar, descrever, interpretar ou extrair informações de imagens,
    fotos, gráficos, documentos visuais, ou qualquer conteúdo visual existente.
    Palavras-chave: analisar imagem, descrever foto, o que tem na imagem.
    """,
    
    "gerar_audio": """
    Solicitações para criar, gerar ou produzir áudio, música, narração,
    efeitos sonoros, ou converter texto em fala (TTS).
    Palavras-chave: criar áudio, gerar música, narrar texto, texto para fala.
    """,
    
    "analisar_audio": """
    Pedidos para analisar, transcrever, interpretar ou extrair informações de
    arquivos de áudio, música, gravações, ou converter fala em texto (STT).
    Palavras-chave: transcrever áudio, analisar música, o que diz no áudio.
    """,
    
    "gerar_video": """
    Solicitações para criar, gerar ou produzir vídeos, animações,
    apresentações visuais, ou conteúdo audiovisual.
    Palavras-chave: criar vídeo, gerar animação, fazer apresentação.
    """,
    
    "analisar_video": """
    Pedidos para analisar, descrever, interpretar ou extrair informações de
    vídeos, filmes, animações, ou qualquer conteúdo audiovisual existente.
    Palavras-chave: analisar vídeo, descrever filme, o que acontece no vídeo.
    """,
    
    "busca_geral": """
    Perguntas gerais, conversas casuais, dúvidas diversas que não se encaixam
    nas categorias específicas acima. Inclui conhecimento geral, curiosidades,
    explicações conceituais, e tópicos variados.
    """
}