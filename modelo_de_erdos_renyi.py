import random
import networkx as nx
import matplotlib.pyplot as plt
import statistics


def generate_erdos_renyi_network(n, p):
    G = nx.Graph()

    G.add_nodes_from(range(n))

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G.add_edge(i, j)
    return G


try:
    n = int(input("Digite a quantidade de nós (ex: 100): "))
    p = float(input("Digite a probabilidade entre 0 e 1 (ex: 0.05): "))
    if not 0 <= p <= 1:
        raise ValueError("A probabilidade deve estar entre 0 e 1.")
except ValueError as e:
    print(f"Entrada inválida: {e}")
    exit()



G = generate_erdos_renyi_network(n, p)

print("\nGerando visualização do grafo...")
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 8))
nx.draw(G, pos, node_size=100, width=0.5, node_color='skyblue', edge_color='gray')
plt.title(f"Modelo de Erdös-Rényi (n={n}, p={p})", fontsize=16)
plt.show()

print("\n--- Medidas Descritivas ---")

degrees = [d for node, d in G.degree()]

print("\n-- Histograma de Graus --")
plt.figure(figsize=(10, 6))
plt.hist(degrees, bins=range(0, max(degrees) + 2), edgecolor='white', alpha=0.8, color='skyblue')
plt.title("Distribuição de Grau - Erdős-Rényi")
plt.xlabel("Grau")
plt.ylabel("Frequência (Nº de Nós)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


if degrees: 
    average_degree = statistics.mean(degrees)
    print(f"\nGrau médio: {average_degree:.2f}")
    
 
    if len(degrees) > 1:
        standard_deviation = statistics.stdev(degrees)
        print(f"Desvio padrão dos graus: {standard_deviation:.2f}")
    else:
        print("Desvio padrão dos graus: N/A (apenas um nó)")
else:
    print("\nGrafo não possui nós.")


print(f"\nDensidade da rede: {nx.density(G):.4f}")
print(f"Coeficiente de clustering médio: {nx.average_clustering(G):.4f}")


is_connected = nx.is_connected(G)
num_components = nx.number_connected_components(G)
print(f"\nA rede é conexa? {'Sim' if is_connected else 'Não'}")
print(f"Número de componentes conectados: {num_components}")


if not is_connected and n > 0:
   
    largest_cc_nodes = max(nx.connected_components(G), key=len)
  
    largest_cc_subgraph = G.subgraph(largest_cc_nodes)
    print(f"Tamanho do maior componente: {len(largest_cc_nodes)} nós ({len(largest_cc_nodes)/n:.2%})")
    
 
    avg_path = nx.average_shortest_path_length(largest_cc_subgraph)
    diameter = nx.diameter(largest_cc_subgraph)
    print(f"Caminho médio (maior componente): {avg_path:.2f}")
    print(f"Diâmetro (maior componente): {diameter}")
elif is_connected:
   
    print(f"Tamanho do maior componente: {n} nós (100.00%)")
    avg_path = nx.average_shortest_path_length(G)
    diameter = nx.diameter(G)
    print(f"Caminho médio: {avg_path:.2f}")
    print(f"Diâmetro: {diameter}")


print("\n--- Análise de Hubs ---")
if len(degrees) > 1:
  
    hub_threshold = average_degree + 2 * standard_deviation
    hubs = [node for node, degree in G.degree() if degree > hub_threshold]
    
    if hubs:
        print(f"Critério para hub: grau > {hub_threshold:.2f}")
        print(f"Nós identificados como hubs: {hubs}")
    else:
        print("Nenhum hub identificado com o critério (grau > média + 2 * desvio padrão).")
else:
    print("Análise de hubs não aplicável.")