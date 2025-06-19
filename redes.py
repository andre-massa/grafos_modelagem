import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def analisar_redes(nome_arquivo='redes.xlsx'):
    """
    Função principal para carregar redes de um arquivo Excel, calcular métricas
    de centralidade e gerar análises e visualizações.
    """
    try:
        xls = pd.ExcelFile(nome_arquivo)
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{nome_arquivo}' não foi encontrado.")
        print("Por favor, certifique-se de que ele está na mesma pasta que este script.")
        return

    nodes_of_interest = [1, 2, 5, 9, 17]
    
    networks = {}
    print("--- Carregando Redes ---")
    for sheet_name in xls.sheet_names:
        if 'arestas' in sheet_name.lower():
            print(f"Lendo a aba de arestas: {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            G = nx.from_pandas_edgelist(df, source=df.columns[0], target=df.columns[1])
            net_name_key = sheet_name.replace('arestas ', '').replace('rede-', 'Rede ').title()
            networks[net_name_key] = G
        else:
            print(f"Ignorando a aba: {sheet_name} (não é uma lista de arestas)")

    print("Redes carregadas com sucesso.\n")

    all_metrics = []
    network_stats = {} # Para análise intra-rede

    print("--- Calculando Métricas de Centralidade ---")
    for net_name, G in networks.items():
        print(f"Processando {net_name}...")
        
        degree = nx.degree_centrality(G)
        if not nx.is_connected(G):
            closeness = {}
            for component in nx.connected_components(G):
                subgraph = G.subgraph(component)
                closeness.update(nx.closeness_centrality(subgraph))
        else:
            closeness = nx.closeness_centrality(G)
        betweenness = nx.betweenness_centrality(G)
        pagerank = nx.pagerank(G)
        
        # Guarda as estatísticas de cada métrica para a rede inteira
        network_stats[net_name] = {
            'Grau': pd.Series(degree),
            'Proximidade': pd.Series(closeness),
            'Intermediação': pd.Series(betweenness),
            'PageRank': pd.Series(pagerank)
        }

        for node in G.nodes():
            all_metrics.append({
                'Rede': net_name, 'Nó': node, 'Grau': degree.get(node, 0),
                'Proximidade': closeness.get(node, 0), 'Intermediação': betweenness.get(node, 0),
                'PageRank': pagerank.get(node, 0)
            })
    print("Métricas calculadas para todas as redes.\n")

    metrics_df = pd.DataFrame(all_metrics)
    interest_df = metrics_df[metrics_df['Nó'].isin(nodes_of_interest)].copy()
    pivot_df = interest_df.pivot_table(
        index='Nó', columns='Rede',
        values=['Grau', 'Proximidade', 'Intermediação', 'PageRank']
    )
    pivot_df = pivot_df.reindex(columns=['Grau', 'Proximidade', 'Intermediação', 'PageRank'], level=0)
    
    # Ordena as colunas das redes para A, B, C, D
    col_order = [('Grau', 'Rede A'), ('Grau', 'Rede B'), ('Grau', 'Rede C'), ('Grau', 'Rede D'),
                 ('Proximidade', 'Rede A'), ('Proximidade', 'Rede B'), ('Proximidade', 'Rede C'), ('Proximidade', 'Rede D'),
                 ('Intermediação', 'Rede A'), ('Intermediação', 'Rede B'), ('Intermediação', 'Rede C'), ('Intermediação', 'Rede D'),
                 ('PageRank', 'Rede A'), ('PageRank', 'Rede B'), ('PageRank', 'Rede C'), ('PageRank', 'Rede D')]
    pivot_df = pivot_df.reindex(columns=col_order)

    print("--- Tabela Comparativa de Centralidades (Nós de Interesse) ---")
    print(pivot_df.round(4))

    # --- NOVO: Salva a tabela em um arquivo de texto ---
    try:
        with open('resultados.txt', 'w') as f:
            f.write("Tabela Comparativa de Centralidades (Nós de Interesse)\n\n")
            f.write(pivot_df.round(4).to_string())
        print("\n\n--- AVISO IMPORTANTE ---")
        print("A tabela também foi salva no arquivo 'resultados.txt'.")
        print("Para garantir que a formatação não seja perdida, por favor, abra este arquivo e copie e cole o seu conteúdo aqui.")
    except Exception as e:
        print(f"\nNão foi possível salvar o arquivo de resultados: {e}")
    
    # Salva também as estatísticas gerais para a análise
    writer = pd.ExcelWriter('estatisticas_redes.xlsx')
    for net_name, stats in network_stats.items():
        stats_df = pd.DataFrame({metric: s.describe() for metric, s in stats.items()}).round(4)
        stats_df.to_excel(writer, sheet_name=net_name)
    writer.close()

if __name__ == '__main__':
    analisar_redes()
    