import random
import networkx as nx
import matplotlib.pyplot as plt
import statistics
import community.community_louvain as community_louvain

old_nodes = int(input("Digite a quantidade de nós existentes: "))
G = nx.complete_graph(old_nodes)

new_nodes = int(input("Digite a quantidade de novos nós: "))

for each_new_node in range(new_nodes):
  degree_per_node = [G.degree(node) for node in G.nodes()]
  sum_of_degrees = sum(degree_per_node)
  fame_of_node = [node/sum_of_degrees for node in degree_per_node]
  connection = int(input(f"Digite a quantidade de conexões do nó {each_new_node}: "))
  targets = random.choices(population = list(G.nodes()), weights = fame_of_node, k = connection)
  new_id = max(G.nodes()) + 1
  G.add_node(new_id)
  for target in targets:
      if not G.has_edge(new_id, target):
        G.add_edge(new_id, target)

#Grafo
print("\n-- Grafo --")
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, node_size=50, with_labels=False)
plt.title("Modelo Barabási-Albert")
plt.show()

#Histograma de graus
print("\n-- Histograma -- ")
degree = [d for n, d in G.degree()]
plt.hist(degree, bins=range(0, max(degree) + 2), edgecolor='white')
plt.title("Distribuição dos Graus - Barabási-Albert")
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
1
hubs = [n for n, d in G.degree() if d > threshold]

print(f"Hubs encontrados: {hubs}")
print(f"Número de hubs: {len(hubs)}")

#Modularidade
partition = community_louvain.best_partition(G)  # {nó: comunidade_id}
modularity = community_louvain.modularity(partition, G)

print(f"Modularidade: {modularity:.4f}")