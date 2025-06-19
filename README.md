# Grafos Modelagem

Tratamos de modelos de geração e de crescimento de redes. Basicamente, vocês terão
que criar funções para gerar a estrutura da rede (lista de arestas ou matriz de adjacências) e utilizar algum software de
análise e visualização para comparar os modelos criados. Preferencialmente, as funções devem ser o mais parametrizadas
possível e cada item descrito abaixo deve incluir a análise de diferentes instâncias de acordo com algumas combinações
dos parâmetros. Para simplificar, vamos considerar apenas redes bidirecionais.
Para cada modelo de rede gerado nos próximos itens, vocês devem:

• Exibir uma visualização gráfica da rede, usando qualquer pacote disponível: o próprio Matlab, ou Gephi, ou
NetworkX do Python etc.

• Calcular a distribuição de graus da rede (cálculo e plotagem do histograma com os graus) e identificar padrões.

• Calcular, com um pacote computacional para tratamento de redes, as métricas descritivas das redes analisadas.

Comparem essas medidas e analisem as implicações das distinções em relação ao método de geração de cada
rede. Pesquisem a respeito dessas medidas e das diferenças encontradas nos modelos.

• As medidas descritivas sugeridas são as seguintes: distribuição de graus (histograma); grau médio, desvio padrão
dos graus e densidade; caminho médio, diâmetro; número de componentes conectados e tamanho do maior
componente; coeficiente de clustering (principalmente para avaliar as redes dos itens 2.2 e 2.3: redes de Watts-
Strogatz tendem a ter caminho médio pequeno e alto coeficiente de clustering, verifiquem!); modularidade
(principalmente para avaliar a rede do item 2.3); existência de hubs (podem ser percebidos quando a distribuição
de graus tem cauda longa) – eles tendem a ter alta centralidade de grau e muitas vezes também altas
centralidades de proximidade e intermediação (principalmente no caso de redes com comunidades); e,
especificamente no caso da rede do item 2.2, seria interessante avaliar como o parâmetro que controla o
redirecionamento de ligações afeta a transição para o regime de mundo pequeno – para isso, varie o valor do
parâmetro e observe (meça e plote) o coeficiente de clustering e o caminho médio, normalizando as medidas
considerando como base o modelo sem reconexão: você deve perceber que em um certo ponto o caminho
médio (normalizado) chega a valores muito menores que 1, enquanto o coeficiente de clustering ainda
permanece alto.

PARTE A

Na primeira parte, a ideia é, a partir de diferentes premissas, gerar três modelos distintos de redes e compará-los.
Item 2.1: Modelo de Erdös-Rényi (rede aleatória)
No escopo desse trabalho, vamos considerar, para a criação de uma rede de acordo com esse modelo, que a formação de
uma aresta entre dois nós está sujeita a uma probabilidade 𝑝.
Entradas: (i) a quantidade de nós; (ii) a probabilidade de estabelecimento de uma aresta entre dois nós quaisquer.
Item 2.2: Modelo de Watts-Strogatz (“mundo pequeno”)
Esse modelo começa com a construção de uma rede em anel, regular, em que cada nó se liga a 2𝑘 vizinhos, 𝑘 vizinhos de
cada lado. Em seguida, cada aresta é submetida a uma probabilidade de ser “redirecionada” para algum dos outros nós da
rede, formando uma rede que poderia ser ilustrada como na figura abaixo:

<img width="628" alt="Screenshot 2025-06-06 at 12 32 25" src="https://github.com/user-attachments/assets/beb80321-bfde-4921-87b3-b12ebfdba6fa" />

Entradas: (i) a quantidade de nós; (ii) quantidade de vizinhos (número par) e (iii) a probabilidade de redirecionamento de
uma aresta.
Item 2.3: Rede aleatória com comunidades
Esse modelo é muito parecido com o primeiro, porém ele inclui a existência de grupos de nós (comunidades): a
probabilidade de ligação entre dois nós de uma mesma comunidade é maior do que entre dois nós de comunidades
diferentes. Uma variação é quando o modelo permite que as probabilidades não sejam “simétricas”, ou seja, quando as
comunidades apresentam diferenças nas probabilidades de ligações de nós dentro e fora das comunidades às quais
pertencem. Por exemplo, num caso com três comunidades, é possível que a probabilidade de ligações entre nós da
comunidade A seja diferente de entre nós da comunidade B e da C, e que a probabilidade de ligações entre os nós da
comunidade A e B seja diferente de entre nós da A e C, e assim por diante. Para que esse modelo possa ser criado, então,
é necessário definir as comunidades às quais os nós pertencem, assim como essas probabilidades de ligações intra e entre
comunidades.

Entradas: (i) a quantidade de nós em cada comunidade; (ii) as probabilidades de ligações (idealmente uma matriz 𝐶 × 𝐶,
onde 𝐶 é a quantidade de comunidades no modelo).

PARTE B

Nessa segunda parte, o propósito é analisar diferentes modelos de crescimento de redes. Para isso, vocês devem considerar
uma pequena rede inicial e criar funções para a inclusão de novos nós a essa rede. Uma sugestão metodológica é usar uma
rede pequena (10 nós) completamente conectada, para que todos os nós iniciais tenham a mesma probabilidade de receber
novas ligações. A diferença entre os modelos é a lógica para ligação dos novos nós.

Item 2.4: Modelo de anexação uniforme

Numa rede com anexação uniforme, todos os nós existentes têm a mesma probabilidade de receber ligações dos novos
nós. Ou seja, as ligações que serão definidas para o novo nó podem ser direcionadas para qualquer um dos nós
existentes, com igual probabilidade.

Entradas: (i) a rede inicial; (ii) quantidade de novos nós; e (iii) a quantidade de ligações que um novo nó estabelece com os
nós existentes ao entrar na rede (deve ser menor que a quantidade de nós existentes na rede inicial). Alternativamente
(seria muito legal se fizessem), a quantidade de ligações dos novos nós não precisa ser a mesma para todos: o parâmetro
informado pode ser usado para definir o critério para o sorteio da quantidade de ligações de cada novo nó.

Item 2.5: Modelo de Barabási-Albert (anexação preferencial)

Numa rede com anexação preferencial, a probabilidade de um nó existente receber a ligação de um novo nó, que esteja
entrando na rede, é proporcional à quantidade de ligações que ele já apresenta antes da entrada desse novo nó.
Entradas: (i) a rede inicial; (ii) quantidade de novos nós; e (iii) a quantidade de ligações que um novo nó estabelece com os
nós existentes ao entrar na rede (deve ser menor que a quantidade de nós existentes na rede inicial). Alternativamente
(seria muito legal se fizessem), a quantidade de ligações dos novos nós não precisa ser a mesma para todos: o parâmetro
informado pode ser usado para definir o critério para o sorteio da quantidade de ligações de cada novo nó.

Item 2.6: Modelo de Price (anexação preferencial e aleatória)

O modelo de Price é, basicamente, uma combinação dos modelos anteriores: parte das ligações de um novo nó seguirá a
anexação preferencial, parte delas seguirá a anexação uniforme. A proporção das ligações que vai seguir a anexação
preferencial é um parâmetro de entrada adicional.

Entradas: (i) a rede inicial; (ii) quantidade de novos nós; (iii) a quantidade de ligações que um novo nó estabelece com os
nós existentes ao entrar na rede (deve ser menor que a quantidade de nós existentes na rede inicial); e (iv) a proporção das
novas ligações que seguirá uma anexação preferencial. Também aqui, a quantidade de ligações dos novos nós não precisa
ser a mesma para todos: o parâmetro informado pode ser usado para definir o critério para o sorteio da quantidade de
ligações de cada novo nó.

Observação: vocês devem notar que as redes geradas pelo modelo de anexação uniforme seguem uma
distribuição exponencial de graus, enquanto as redes geradas pelos modelos de Barabási-Albert e de
Price são redes “livre de escala”, configuradas por leis de potência. Normalmente, o expoente da lei de
potência relativa a uma rede de anexação preferencial lei é 3, e o expoente de uma rede de Price pode
variar, dependendo do parâmetro que regula o comportamento das ligações. Façam testes.

As figuras a seguir apresentam quatro configurações de redes (Rede A, Rede B, C e Rede D) que guardam entre si algumas semelhanças. As listas de arestas estão disponíveis no arquivo redes.xlsx.

Sua tarefa é, utilizando alguma ferramenta de análise de redes de sua preferência (Gephi, Matlab, Python etc.), explicar as
diferenças observadas nos valores das medidas de centralidade (grau, closeness, betweenness e page rank) dos nós
1, 2, 5, 9 e 17, comparando cada um deles:
(a) com os demais nós das redes às quais eles pertencem (de maneira geral), em cada uma das quatro configurações
(b) com os nós correspondentes a eles nas outras configurações.

<img width="501" alt="Screenshot 2025-06-06 at 12 33 31" src="https://github.com/user-attachments/assets/6836d01e-6c24-41ae-92dc-5696d846669f" />

