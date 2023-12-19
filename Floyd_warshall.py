import json
import pandas as pd
import csv
import networkx as nx

def converti_chiavi(dic):
    if isinstance(dic, dict):
        return {str(k): converti_chiavi(v) for k, v in dic.items()}
    else:
        return dic

nodes = set()
adiacenze = {}

# Lettura punti da csv e salvataggio in set
csv_coordinates = pd.read_csv('Coordinate.csv')
for index, row in csv_coordinates.iterrows():
    nodes.update([(row['x'], row['y'])])

# Cicla sull'elenco dei punti letti dal csv
for node in nodes:
    punti_adiacenti = {}
    # Verifica adiacenza
    if (node[0]+1, node[1]) in nodes:
        item = (node[0]+1, node[1])
        punti_adiacenti.update({item: 1})  # Aggiungo al dictionary dei punti adiacenti esistenti
    if (node[0]-1, node[1]) in nodes:
        item = (node[0]-1, node[1])
        punti_adiacenti.update({item: 1})
    if (node[0], node[1]+1) in nodes:
        item = (node[0], node[1]+1)
        punti_adiacenti.update({item: 1})
    if (node[0], node[1]-1) in nodes:
        item = (node[0], node[1]-1)
        punti_adiacenti.update({item: 1})
    # Salvo punti adiacenti al punto analizzato
    adiacenze.update({node: punti_adiacenti})

# Ricerca dei punti "notevoli"
nodi = []
for x in sorted(adiacenze):
    for y in sorted(adiacenze[x]):
        if len(adiacenze[x]) == 1:
            nodi.append(x)
print(nodi)

# Calcolo Floyd-Warshall
G = nx.Graph()
G.add_nodes_from(sorted(nodes))
for x in sorted(adiacenze):
    for y in sorted(adiacenze[x]):
        G.add_edge(x, y)
print(G)
print(list(G.nodes))
print(list(G.edges))
f_w = nx.floyd_warshall(G)

# Filtra il risultato di Floyd-Warshall per includere solo i nodi in "nodi"
f_w_specializzato = {k: {kk: vv for kk, vv in v.items() if kk in nodi} for k, v in f_w.items() if k in nodi}

# Converti le chiavi del dizionario f_w_specializzato da tuple a stringhe in modo ricorsivo
f_w_specializzato_str_keys = converti_chiavi(f_w_specializzato)

# Scrivi il dizionario con chiavi convertite in un file JSON
with open("file_specializzato.json", "w") as file:
    json.dump(f_w_specializzato_str_keys, file, ensure_ascii=False, indent=15)
