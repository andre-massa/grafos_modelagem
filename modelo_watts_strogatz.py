import networkx as nx
import matplotlib.pyplot as plt
import random
import statistics
import community.community_louvain as community_louvain

def gerar_rede_watts(n, k, p):
    if k % 2 != 0:
        print("A quantidade de vizinhos (k) deve ser par.")
        return None

    G = nx.Graph()
    G.add_nodes_from(range(n))

    for node in range(n):
        for neighbor in range(1, k // 2 + 1):
            G.add_edge(node, (node + neighbor) % n)
            G.add_edge(node, (node - neighbor) % n)

    for node in range(n):
        for neighbor in range(1, k // 2 + 1):
            target = (node + neighbor) % n
            if G.has_edge(node, target) and random.random() < p:
                G.remove_edge(node, target)


            possible_nodes = set(range(n)) - {node} - set(G[node])
            if possible_nodes:
                new_target = random.choice(list(possible_nodes))
                G.add_edge(node, new_target)

    return G

n = int(input("Digite a quantidade de nós na rede: "))
k = int(input("Digite uma quantidade par de vizinhos: "))
p = float(input("Digite a probabilidade entre 0 e 1: "))

G = gerar_rede_watts(n, k, p)
nx.draw_circular(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
plt.title("Modelo Watts-Strogatz")
plt.show()

#Histograma de graus
print("\n-- Histograma -- ")
degree = [d for n, d in G.degree()]
plt.hist(degree, bins=range(0, max(degree) + 2), edgecolor='white')
plt.title("Distribuição de Graus - Watts-Strogatz")
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