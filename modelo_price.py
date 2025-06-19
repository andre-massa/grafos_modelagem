import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from typing import Union, Tuple

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

print(f"Rede inicial (Grafo Completo) criada com {G_inicial.number_of_nodes()} nós e {G_inicial.number_of_edges()} arestas.")

novos_nos = int(input("\nDigite a quantidade de novos nós a serem adicionados: "))
m_conexoes = int(input("Digite a quantidade de ligações que cada novo nó fará: "))
p_pref = float(input("Digite a proporção de anexação preferencial (entre 0 e 1): "))

G_final = modelo_price(
    rede_inicial=G_inicial,
    quantidade_novos_nos=novos_nos,
    m_conexoes=m_conexoes,
    proporcao_preferencial=p_pref
)


plt.figure(figsize=(10, 10))
cores_nos = ['red' if no in G_inicial.nodes() else 'skyblue' for no in G_final.nodes()]
tamanho_nos = [250 if no in G_inicial.nodes() else 50 for no in G_final.nodes()]
pos = nx.spring_layout(G_final, seed=42)
nx.draw(G_final, pos, with_labels=False, node_color=cores_nos, node_size=tamanho_nos, width=0.5)
plt.title(f"Modelo de Price (p={p_pref}, m={m_conexoes})")
plt.show()


degrees = [degree for _, degree in G_final.degree()]
plt.figure(figsize=(8, 6))
plt.hist(degrees, bins=range(0, max(degrees) + 2), color='skyblue', edgecolor='black', align='left')
plt.title("Distribuição dos Graus")
plt.xlabel("Grau")
plt.ylabel("Frequência")
plt.show()

print(f"Grau médio: {np.mean(degrees):.4f}")
print(f"Desvio padrão dos graus: {np.std(degrees):.4f}")
print(f"Densidade da rede: {nx.density(G_final):.4f}")
print(f"Coeficiente de Clustering médio: {nx.average_clustering(G_final):.4f}")

if nx.is_connected(G_final):
    print(f"Caminho médio mínimo: {nx.average_shortest_path_length(G_final):.4f}")
    print(f"Diâmetro da rede: {nx.diameter(G_final)}")
else:
    print("\nO grafo não é conexo.")
    componentes = sorted(nx.connected_components(G_final), key=len, reverse=True)
    maior_componente = G_final.subgraph(componentes[0])
    print(f"Analisando o maior componente conectado ({maior_componente.number_of_nodes()} nós)...")
    if maior_componente.number_of_nodes() > 1:
        print(f"  - Caminho médio mínimo: {nx.average_shortest_path_length(maior_componente):.4f}")
        print(f"  - Diâmetro: {nx.diameter(maior_componente)}")