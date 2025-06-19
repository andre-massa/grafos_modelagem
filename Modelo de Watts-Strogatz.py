import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def gerar_rede_watts(n, k, p):

    G = nx.Graph()
    G.add_nodes_from(range(n))


    for node in range(n):
        for neighbor in range(1, k//2 + 1):
            G.add_edge(node, (node + neighbor) % n)


    for node in range(n):
        neighbors = list(range(node+1, node + k//2 + 1))

        for neighbor in neighbors:
            neighbor_mod = neighbor % n

            if random.random() < p:
                G.remove_edge(node, neighbor_mod)
                possible_nodes = set(range(n)) - {node} - set(G[node])

                if possible_nodes:
                    new_node = random.choice(list(possible_nodes))
                    G.add_edge(node, new_node)

    return G


n = int(input("Digite a quantidade de nós na rede: "))
k = int(input("Digite uma quantidade par de vizinhos: "))
p = float(input("Digite a probabilidade entre 0 e 1: "))

G = gerar_rede_watts(n, k, p)
nx.draw_circular(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
plt.title("Modelo Watts-Strogatz")
plt.show()


# Medidas descritivas

degrees = [degree for _, degree in G.degree()]

plt.hist(degrees, bins=range(0, max(degrees)+ 20), color='skyblue', edgecolor='black', align='left')
plt.title("Distribuição dos Graus")
plt.xlabel("Grau")
plt.ylabel("Frequencia")
plt.show()
nx.average_clustering(G)

print("Grau médio:", np.mean(degrees))
print("Desvio padrão dos graus:", np.std(degrees))
print("Densidade:", nx.density(G))
print("Coeficiente de Clustering:", nx.average_clustering(G))

if nx.is_connected(G):
    print("Caminho médio:", nx.average_shortest_path_length(G))
    print("Diâmetro:", nx.diameter(G))
else:
    print("O grafo não é conexo; não é possível calcular caminho médio e diâmetro.")