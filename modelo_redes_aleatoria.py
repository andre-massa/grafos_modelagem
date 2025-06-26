import networkx as nx
import matplotlib.pyplot as plt
import random
import statistics
import community.community_louvain as community_louvain


number_of_communities = int(input("Digite o número de comunidades: "))

nodes = []

for i in range(number_of_communities):
  nodesloop = int(input(f"Digite a quantidade de nós na comunidade {i + 1}: "))
  nodes.append(nodesloop)

probabilities = []

for i in range(number_of_communities):
  temp = []
  for j in range(number_of_communities):
    probabilitiesloop = float(input(f"Digite a probabilidade entre a comunidade {i + 1} e {j + 1}: "))
    temp.append(probabilitiesloop)
  probabilities.append(temp)

G = nx.Graph()
communities = []
node_index = 0

for community_id, size in enumerate(nodes):
    for _ in range(size):
        G.add_node(node_index)
        communities.append(community_id)
        node_index += 1

total_nodes = len(communities)

#Medidas descritivas


for l in range(total_nodes):
    for c in range(l + 1, total_nodes):
        com_l = communities[l]
        com_c = communities[c]
        p = probabilities[com_l][com_c]

        if random.random() < p:
            G.add_edge(l, c)

#Grafo
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, node_size=50, with_labels=False)
plt.title("Rede aleatória com comunidades")
plt.show()

#Histograma de graus
degree = [x for y, x in G.degree()]
print("\n-- Histograma -- ")
plt.hist(degree, bins=range(0, max(degree)), edgecolor='white')
plt.title("Distribuição de Graus - Rede aleatória com comunidades")
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
partition = community_louvain.best_partition(G)
modularity = community_louvain.modularity(partition, G)

print(f"Modularidade: {modularity:.4f}")


