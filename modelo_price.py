import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import Union, Tuple
import statistics
import community.community_louvain as community_louvain

def modelo_price(
    rede_inicial: nx.Graph,
    quantidade_novos_nos: int,
    m_conexoes: Union[int, Tuple[int, int]],
    proporcao_preferencial: float
) -> nx.Graph:

    if not 0.0 <= proporcao_preferencial <= 1.0:
        raise ValueError("A proporção preferencial deve estar entre 0.0 e 1.0.")

    if isinstance(m_conexoes, int) and m_conexoes > len(rede_inicial.nodes):
         print(f"m_conexoes ({m_conexoes}) é maior que o número de nós iniciais ({len(rede_inicial.nodes)}). Será limitado ao número de nós disponíveis.")

    G = rede_inicial.copy()

    try:
        id_proximo_no = max(G.nodes()) + 1
    except (TypeError, ValueError):
        id_proximo_no = len(G.nodes())

    for i in range(quantidade_novos_nos):
        novo_no_id = id_proximo_no + i
        nos_existentes = list(G.nodes())

        if not nos_existentes:
            G.add_node(novo_no_id)
            continue

        G.add_node(novo_no_id)

        if isinstance(m_conexoes, int):
            conexoes_a_fazer = m_conexoes
        elif isinstance(m_conexoes, tuple) and len(m_conexoes) == 2:
            conexoes_a_fazer = random.randint(m_conexoes[0], m_conexoes[1])
        else:
            raise TypeError("m_conexoes deve ser um inteiro ou uma tupla (min, max).")

        conexoes_a_fazer = min(conexoes_a_fazer, len(nos_existentes))

        graus = [G.degree(n) + 1 for n in nos_existentes]
        alvos_ja_escolhidos = set()

        for _ in range(conexoes_a_fazer):
            alvo_selecionado = None
            while alvo_selecionado is None or alvo_selecionado in alvos_ja_escolhidos:
                if random.random() < proporcao_preferencial:
                    alvo_selecionado = random.choices(nos_existentes, weights=graus, k=1)[0]
                else:
                    alvo_selecionado = random.choice(nos_existentes)

            alvos_ja_escolhidos.add(alvo_selecionado)
            G.add_edge(novo_no_id, alvo_selecionado)

    return G



nos_iniciais = int(input("Digite a quantidade de nós para a rede inicial: "))
G_inicial = nx.complete_graph(nos_iniciais)

novos_nos = int(input("\nDigite a quantidade de novos nós a serem adicionados: "))
m_conexoes = int(input("Digite a quantidade de ligações que cada novo nó fará: "))
p_pref = float(input("Digite a proporção de anexação preferencial (entre 0 e 1): "))

G = modelo_price(
    rede_inicial=G_inicial,
    quantidade_novos_nos=novos_nos,
    m_conexoes=m_conexoes,
    proporcao_preferencial=p_pref
)


print("\n-- Grafo --")
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, node_size=50, with_labels=False)
plt.title("Modelo de Price")
plt.show()

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