import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

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

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
node_sizes = [G.degree(n) * 20 + 10 for n in G.nodes()]
node_colors = [G.degree(n) for n in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.viridis, 
        node_size=node_sizes, edge_color='gray', font_size=8)
plt.title(f"Modelo de Anexação Uniforme ({G.number_of_nodes()} nós)")
plt.show()

degrees = [degree for _, degree in G.degree()]
plt.figure(figsize=(8, 6))
plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2), color='skyblue', edgecolor='black', align='left')
plt.title("Distribuição dos Graus")
plt.xlabel("Grau")
plt.ylabel("Frequência")
plt.xticks(range(min(degrees), max(degrees) + 2))
plt.grid(axis='y', alpha=0.7)
plt.show()

# Medidas Descritivas

print(f"Número total de nós: {G.number_of_nodes()}")
print(f"Número total de arestas: {G.number_of_edges()}")
print(f"Grau médio: {np.mean(degrees):.2f}")
print(f"Desvio padrão dos graus: {np.std(degrees):.2f}")
print(f"Densidade: {nx.density(G):.4f}")

if nx.is_connected(G):
    print("A rede é conectada.")
    print(f"Caminho médio: {nx.average_shortest_path_length(G):.2f}")
    print(f"Diâmetro: {nx.diameter(G)}")
else:
    num_componentes = nx.number_connected_components(G)
    maior_componente = max(nx.connected_components(G), key=len)
    subgrafo_maior_comp = G.subgraph(maior_componente)
    
    print(f"A rede NÃO é conectada e possui {num_componentes} componentes.")
    print(f"O maior componente tem {subgrafo_maior_comp.number_of_nodes()} nós.")
    if subgrafo_maior_comp.number_of_nodes() > 1:
        caminho_medio_maior_comp = nx.average_shortest_path_length(subgrafo_maior_comp)
        diametro_maior_comp = nx.diameter(subgrafo_maior_comp)
        print(f"Caminho médio (maior componente): {caminho_medio_maior_comp:.2f}")
        print(f"Diâmetro (maior componente): {diametro_maior_comp}")