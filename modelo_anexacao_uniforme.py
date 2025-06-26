import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import statistics
import community.community_louvain as community_louvain

def modelo_anexacao_uniforme(rede_inicial, num_novos_nos, criterio_ligacoes):

    g = rede_inicial.copy()
    proximo_no_id = max(g.nodes()) + 1 if g.nodes() else 0

    for i in range(num_novos_nos):
        novo_no_id = proximo_no_id + i
        nos_existentes = list(g.nodes())
        num_nos_existentes = len(nos_existentes)
        num_ligacoes = np.random.poisson(lam=criterio_ligacoes)
        num_ligacoes = max(1, min(num_ligacoes, num_nos_existentes))
        g.add_node(novo_no_id)

        if num_nos_existentes > 0:
            alvos = random.sample(nos_existentes, k=num_ligacoes)
            for alvo in alvos:
                g.add_edge(novo_no_id, alvo)

    return g

num_nos_iniciais = int(input("Digite a quantidade de nós na rede inicial: "))
num_novos_nos = int(input("Digite a quantidade de NOVOS nós para adicionar: "))
media_ligacoes = int(input("Digite a média de ligações que cada novo nó fará: "))


rede_inicial = nx.complete_graph(num_nos_iniciais)
G = modelo_anexacao_uniforme(rede_inicial, num_novos_nos, media_ligacoes)

print("\n-- Grafo --")
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, node_size=50, with_labels=False)
plt.title("Modelo de anexação uniforme")
plt.show()

# Medidas Descritivas

#Histograma de graus
print("\n-- Histograma -- ")
degree = [d for n, d in G.degree()]
plt.hist(degree, bins=range(0, max(degree) + 2), edgecolor='white')
plt.title("Distribuição dos Graus")
plt.xlabel("Grau")
plt.ylabel("Frequência")
plt.show()

#Grau médio
degree = [d for n, d in G.degree()]
average_degree = sum(degree) / len(degree)
print(f"Grau médio: {average_degree:.2f}")

#Desvio padrão
standard_deviation = statistics.stdev(degree)
print(f"Desvio padrão: {standard_deviation}")

#Densidade
density = nx.density(G)
print(f"Densidade da rede: {density:.4f}")

#Caminho médio
if nx.is_connected(G):
  average_path_length= nx.average_shortest_path_length(G)
  print(f"Caminho médio: {average_path_length:.2f}")

else:
  largest_component = max(nx.connected_components(G), key=len)
  subgraph = G.subgraph(largest_component)
  average_path_length= nx.average_shortest_path_length(subgraph)
  print(f"Rede não conexa. Caminho médio do maior componente: {average_path_length:.2f}")

#Diâmetro
if nx.is_connected(G):
  diameter = nx.diameter(G)
  print(f"Diâmetro: {diameter}")

else:
  largest_component = max(nx.connected_components(G), key=len)
  subgraph = G.subgraph(largest_component)
  diameter = nx.diameter(subgraph)
  print(f"Rede não conexa. Diâmetro do maior componente: {diameter}")

#Número de componentes conectados e tamanho do maior componente
if nx.is_connected(G):
  print(f"Rede conexa. Número de componentes conectados: {nx.number_connected_components(G)}")
  largest_component = max(nx.connected_components(G), key=len)
  print(f"Rede conexa. Tamanho do maior componente:{len(largest_component)}")

else:
  print(f"Rede não conexa. Número de componentes conectados: {nx.number_connected_components(G)}")
  largest_component = max(nx.connected_components(G), key=len)
  print(f"Rede não conexa. Tamanho do maior componente: {len(largest_component)}")

#Coeficiente de clustering
average_clustering = nx.average_clustering(G)
print(f"Coeficiente de clustering: {average_clustering}")

#Existência de hubs
avg_degree = statistics.mean(degree)
std_degree = statistics.stdev(degree)
threshold = avg_degree + 2 * std_degree

hubs = [n for n, d in G.degree() if d > threshold]

print(f"Hubs encontrados: {hubs}")
print(f"Número de hubs: {len(hubs)}")

#Modularidade
partition = community_louvain.best_partition(G)  # {nó: comunidade_id}
modularity = community_louvain.modularity(partition, G)

print(f"Modularidade: {modularity:.4f}")