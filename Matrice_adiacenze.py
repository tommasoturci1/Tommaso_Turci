import pandas
import csv
import networkx as nx

nodes = set()
adiacenze = {}

# Lettura punti da csv e salvataggio in set
csv_coordinates = pandas.read_csv('Coordinate.csv')
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

# Scrittura risultati in file csv
with open('risultati.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for x in sorted(adiacenze):
        writer.writerow(x)
        for y in sorted(adiacenze[x]):
            data = [y, adiacenze[x][y]]
            writer.writerow(data)

# Ricerca dei punti "notevoli"
nodi = []
for x in sorted(adiacenze):
    for y in sorted(adiacenze[x]):
        if len(adiacenze[x]) == 1:
            nodi.append(x)
print(nodi)
# Verificare se tale lista di nodi si può ricavare da una funzione di nx

# Calcolo Floyd-Warshall
G = nx.Graph()
G.add_nodes_from(sorted(nodes))
for x in sorted(adiacenze):
    for y in sorted(adiacenze[x]):
        G.add_edge(x, y)
print(G)
print(list(G.nodes))
print(list(G.edges))
#Matrice
F_W = nx.floyd_warshall_numpy(G) 
#Dizionario
f_w = nx.floyd_warshall(G)

with open('distanze_matrice.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(F_W)

#Scrivo solo le distanze tra i punti "notevoli" della lista nodi
with open('distanze.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for x in f_w:
        if x in nodi:
            writer.writerow(x)
            for y in f_w[x]:
                if y in nodi:
                    data = [y, f_w[x][y]]
                    writer.writerow(data)
            
